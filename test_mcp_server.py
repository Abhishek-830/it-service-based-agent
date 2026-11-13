import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "src.mcp_server.server"]
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            # Check available MCP tools
            tools = await session.list_tools()

            print("\n--- AVAILABLE MCP TOOLS ---")

            for tool in tools.tools:
                print(tool.name)

            # Create a support ticket
            print("\n--- CREATE SUPPORT TICKET ---")

            result = await session.call_tool(
                "create_support_ticket",
                arguments={
                    "title": "Laptop Not Working",
                    "description": "Laptop is not starting.",
                    "requester_name": "Abhishek",
                    "requester_email": "abhishek@example.com",
                    "category": "Hardware",
                    "priority": "High"
                }
            )

            print(result.content[0].text)


asyncio.run(main())