from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq

import os
from dotenv import load_dotenv
load_dotenv()

import asyncio

async def main():
    client=MultiServerMCPClient(
        {
            "math":{
                "command":"python",
                "args":[r"D:\GenAI\10_Langgraph\MCP\mathserver.py"],   ## absolute path
                "transport":"stdio"
            },
            "weather":{
                "url":"http://127.0.0.1:8000/mcp",
                "transport":"streamable_http"
            }
        }
    )
    os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
    tools = await client.get_tools()
    model = ChatGroq(model="openai/gpt-oss-120b")
    agent = create_react_agent(model,tools)

    math_response = await agent.ainvoke(
        {"messages":[{"role":"user","content":"What is (3+5)*12"}]}
    )
    print("Math response:",math_response['messages'][-1].content)

    math_response = await agent.ainvoke(
        {"messages":[{"role":"user","content":"What is the weather in London"}]}
    )
    print("Weather response:",math_response['messages'][-1].content)
asyncio.run(main())