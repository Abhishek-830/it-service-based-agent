import asyncio

from src.agent.agent import run_agent


async def main():

    question = (
        "Please check the status of my support ticket "
        "TKT-D8FBB2C3."
    )

    print("\n--- USER QUESTION ---")
    print(question)

    print("\n--- AI AGENT RESPONSE ---")

    answer = await run_agent(question)

    print(answer)


if __name__ == "__main__":
    asyncio.run(main())