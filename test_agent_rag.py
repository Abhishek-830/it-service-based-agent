import asyncio

from src.agent.agent import run_agent


async def test_agent_rag():

    question = (
        "My laptop is not connecting to office Wi-Fi. "
        "How can I fix it?"
    )

    print("\n========== USER QUESTION ==========")
    print(question)

    print("\nRunning AI Agent...")

    answer = await run_agent(question)

    print("\n========== AI AGENT RESPONSE ==========")
    print(answer)

    print("\nAI Agent RAG Integration Test Successful!")


if __name__ == "__main__":
    asyncio.run(test_agent_rag())