import asyncio
from claude_agent_sdk import query


async def main():
    prompt = "What is 2 + 2? Give a short answer."

    async for message in query(prompt=prompt):
        print(message)


if __name__ == "__main__":
    asyncio.run(main())