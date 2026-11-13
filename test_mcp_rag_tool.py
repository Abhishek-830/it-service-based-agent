import asyncio
import json

from src.agent.mcp_client import connect_to_mcp_server


async def test_rag_mcp_tool():

    async with connect_to_mcp_server() as session:

        print("\n========== AVAILABLE MCP TOOLS ==========")

        tools = await session.list_tools()

        for tool in tools.tools:
            print(tool.name)

        print("\n========== TESTING RAG MCP TOOL ==========")

        result = await session.call_tool(
            "search_knowledge_base",
            arguments={
                "query": "My laptop is not connecting to office Wi-Fi.",
                "top_k": 3
            }
        )

        for block in result.content:
            if hasattr(block, "text"):

                data = json.loads(block.text)

                print("\n========== SEARCH RESULTS ==========")
                print(json.dumps(
                    data,
                    indent=4,
                    ensure_ascii=False
                ))


if __name__ == "__main__":
    asyncio.run(test_rag_mcp_tool())