import warnings
warnings.filterwarnings("ignore")

import json
from groq import Groq
import os
from yahoo_finance import get_stock_price
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

TOOL_DEFINITION = [
    {
        "type":"function",
        "function":{
            "name":"get_stock_price",
            "description":"Get the current price of a stock given it's ticker symbol.",
            "parameters":{
                "type":"object",
                "properties":{
                    "ticker_symbol":{
                        "type":"string",
                        "description":"The ticker symbol of the stock to get the price of e.g. AAPL, TSLA."
                    }
                },
                "required":["ticker_symbol"]
            }
        }
    }
]

SYSTEM_PROMPT = """
You are a helpful stock market assistant. When the user asks about a stock price,
think step-by-step about what you need to do, then call the get_stock_price tool
with the correct symbol. After recieving the result, present the information in a 
clear, and friendly manner.

IMPORTANT-> SHOULD BE STRICTLY FOLLOWED: Always call the get_stock_price tool with the correct ticker symbol. Dont't 
pick up the price from our old conversations, as the price keeps on changing. Do not assume
the price from conversations. Always whenever a price for a stock is asked, we need to call 
the relevant tool again.

Always reason out loud before acting so the user can follow your chain os thought.
"""

FEW_SHOT_EXAMPLES = [
    # Example 1: Single stock lookup
    {
        "role":"user",
        "content":"How much is Apple stock right now?"
    },
    {
        "role":"assistant",
        "content":
            """
            The user is asking about Apple's stock price. Apple's ticker symbol is AAPL.
            Let me fetch the current price of Apple stock.
            """,
        "tool_calls":[
            {
                "id":"tool_call_01",
                "type":"function",
                "function":{
                    "name":"get_stock_price",
                    "arguments":json.dumps({
                        "ticker_symbol":"AAPL"
                    })
                }
            }
        ]
    },
    {
        "role":"tool",
        "tool_call_id":"calll_01",
        "content":json.dumps({
            "ticker":"AAPL",
            "price":200.3,
            "curreny":"USD"
        })
    },
    {
        "role":"assistant",
        "content":(
            "Apple (AAPL) is currentlly trading at $200.30 per share in USD."
            "Keep in mind that this is the last traded price and may shift slightly by the time you check again."
        )
    },
    # Example 2: Multi stock comparison 
    {
        "role": "user",
        "content": "Compare the stock prices of Google and Microsoft"
    },
    {
        "role": "assistant",
        "content": (
            "The user wants to compare two stocks. Google's parent company "
            "Alphabet trades under the ticker symbol GOOGL, and Microsoft trades "
            "under the ticker symbol MSFT.\n"
            "Let me fetch the current prices of both stocks."
        ),
        "tool_calls": [
            {
                "id": "tool_call_02",
                "type": "function",
                "function": {
                    "name": "get_stock_price",
                    "arguments": json.dumps({"ticker_symbol":"GOOGL"})
                }
            },
            {
                "id": "tool_call_03",
                "type": "function",
                "function": {
                    "name": "get_stock_price",
                    "arguments": json.dumps({"ticker_symbol": "MSFT"})
                }
            }
        ]
    },
    {
        "role": "tool",
        "tool_call_id": "tool_call_02",
        "content": json.dumps({
            "ticker": "GOOGL",
            "price": 280.12,
            "currency": "USD"
        }),
    },
    {
        "role": "tool",
        "tool_call_id": "tool_call_03",
        "content": json.dumps({
            "ticker": "MSFT",
            "price": 235.77,
            "currency": "USD"
        }),
    },
    {
        "role": "assistant",
        "content": (
            "Here's the comparison:\n\n"
            "- Alphabet/Google (GOOGL) is trading at $280.12 per share in USD.\n"
            "- Microsoft (MSFT) is trading at $235.77 per share in USD.\n\n"
            "Microsoft's stock is currently cheaper than Google's."
        )
    }
]

AVAILABLE_TOOLS={
    "get_stock_price":get_stock_price
}
def run_agent(user_query:str)->None:
    """Single turn agentic loop with chain of thought reasoning"""
    
    messages = [
        {
            "role":"system",
            "content":SYSTEM_PROMPT
        },
        *FEW_SHOT_EXAMPLES,
        {
            "role":"user",
            "content":user_query
        }
    ]
    print(f"\n{'='*60}")
    print(f"User: {user_query}")
    print(f"{'='*60}")
    
    while True:
        response = client.chat.completions.create(
            model = "openai/gpt-oss-120b",
            messages=messages,
            tools=TOOL_DEFINITION,
        )
        choice = response.choices[0]
        assistant_msg = choice.message
        
        messages.append(assistant_msg)
        # print(assistant_msg)
        
        if assistant_msg.content:
            print(f"Assistant (thinking): {assistant_msg.content}\n")
            
        if choice.finish_reason=="stop":
            break
        
        if not assistant_msg.tool_calls:
            break
        
        for tool_call in assistant_msg.tool_calls:
            fn_name = tool_call.function.name
            fn_args = json.loads(tool_call.function.arguments)

            print(f" [Tool Call] {fn_name}({fn_args})")

            fn = AVAILABLE_TOOLS[fn_name]
            result = fn(**fn_args)

            print(f" [Tool Result] {result}\n")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })
            
         
    return None
        

def main():
    print("-"*45)
    print("Stock price agent (type 'quit' to exit)")
    print("-"*45)
    
    while True:
        query = input("\nYou: ").strip()
        if not query:
            continue
        if query.lower() in ("quit","exit","q"):
            print("Goodbye!")
            break
        
        run_agent(query)
        
        
if __name__ =="__main__":
    main()