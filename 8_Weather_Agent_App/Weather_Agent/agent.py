import json

from Weather_Agent.client import get_client_and_model
from Weather_Agent.prompts import build_system_prompt
from Weather_Agent.tools import TOOL_FUNCTIONS
from Weather_Agent.schemas import TOOL_MENU
from Weather_Agent.config import MAX_TURNS
from Weather_Agent.config import MAX_TOKENS


def run_agent_turns(messages: list, max_turns: int = MAX_TURNS) -> str:
    client, model, provider = get_client_and_model()

    working = [
        {
            "role": "system",
            "content": build_system_prompt(),
        },
        *messages
    ]
    
    for _ in range(max_turns):
        response = client.chat.completions.create(
            model=model,
            messages=working,
            tools=TOOL_MENU,
            max_tokens=MAX_TOKENS
        )
        
        message = response.choices[0].message
        
        if not message.tool_calls:
            answer = message.content or ""
            messages.append(
                {
                    "role":"assistant",
                    "content":answer
                }
            )
            return answer
        
        working.append(
            {
                "role":"assistant",
                "content":message.content,
                "tool_calls":[
                    {
                        "id":call.id,
                        "type":"function",
                        "function":{
                            "name":call.function.name,
                            "arguments":json.dumps(call.function.arguments),
                        }
                    } for call in message.tool_calls
                ] 
            }
        )
        
        # make actual tool calls
        for call in message.tool_calls:
            name = call.function.name

            if name not in TOOL_FUNCTIONS:
                result = f"Unknown tool: {name}"
            else:
                arguments = json.loads(call.function.arguments)
                tool_result = TOOL_FUNCTIONS[name](**arguments)  

            working.append(
                {
                "role": "tool", 
                "content": str(tool_result),  
                "tool_call_id": call.id,
                }
            )
            
    fallback = "Stopped after hitting max_turns without a final answer"   
    messages.append(
        {
            "role":"assistant",
            "content":fallback
        }
    )

    return fallback