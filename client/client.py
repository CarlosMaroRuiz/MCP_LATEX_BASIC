from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP
from dotenv import load_dotenv
import asyncio
load_dotenv()
server = MCPServerStreamableHTTP('http://localhost:8000/mcp')  
agent = Agent('deepseek:deepseek-chat', toolsets=[server])  

async def main():
    async with agent:  
        result = await agent.run('realiza un codigo latex para un documento de 2 paginas')
    print(result.output)


if __name__ == "__main__":
    asyncio.run(main())