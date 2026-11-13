import asyncio

from src.agent.mcp_client import connect_to_mcp_server


async def main():

    async with connect_to_mcp_server() as session:

        # Get available tools
        tools = await session.list_tools()

        print("\n--- MCP CLIENT CONNECTED ---")

        print("\nAvailable Tools:")

        for tool in tools.tools:
            print("-", tool.name)

        # Call MCP tool
        print("\n--- CHECKING TICKET ---")

        result = await session.call_tool(
            "get_support_ticket",
            arguments={
                "ticket_number": "TKT-D8FBB2C3"
            }
        )

        for content in result.content:
            if hasattr(content, "text"):
                print(content.text)


if __name__ == "__main__":
    asyncio.run(main())