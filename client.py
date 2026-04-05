from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_groq import ChatGroq
import asyncio

from dotenv import load_dotenv
load_dotenv()


async def main():
    client = MultiServerMCPClient(
    {
        "math":{
            "command":"python",
        "args":["mathserver.py"], 
        "transport":"stdio"
        },

         "weather":{
        "url":"http://localhost:8000/mcp",
        "transport":"streamable-http"
        }
    }

    )
    import os
    # Verify GROQ API key is set
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set")
    
    tools = await client.get_tools()
    model = ChatGroq(model="llama-3.1-8b-instant")
    agent = create_agent(
        model, tools
    )
    
    # Ask the agent to solve the math problem step by step
    math_response = await agent.ainvoke(
        {"messages":[{"role":"user","content":"Calculate: (3+5) multiplied by 23. First add 3 and 5, then multiply the result by 23."}]}
    )
    print("Math response", math_response["messages"][-1].content)


    weather_response = await agent.ainvoke(
        {"messages":[{"role":"user","content":"Use the get_weather tool to find the weather for Hyderabad location"}]}
    )
    print("Weather response", weather_response["messages"][-1].content)

asyncio.run(main())