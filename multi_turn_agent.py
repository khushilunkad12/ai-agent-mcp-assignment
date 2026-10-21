import asyncio
import ollama
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

MODEL = "qwen2.5:3b"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "word_count",
            "description": "Count the words in a given text.",
            "parameters": {
                "type": "object",
                "properties": {"text": {"type": "string"}},
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_employee",
            "description": "Look up an employee's name and department by employee ID.",
            "parameters": {
                "type": "object",
                "properties": {"employee_id": {"type": "string"}},
                "required": ["employee_id"]
            }
        }
    }
]


async def main():
    server = StdioServerParameters(
        command="python",
        args=["word_count_server.py"]
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            available = await session.list_tools()
            print("MCP tools discovered:", [t.name for t in available.tools])
            print("\nMulti-turn MCP agent ready. Type 'exit' to stop.")

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant. Use lookup_employee "
                        "when employee information is needed. Remember the "
                        "conversation context when answering follow-up questions. "
                        "Do not invent employee details."
                    )
                }
            ]

            while True:
                user_input = input("\nYou: ").strip()

                if user_input.lower() in {"exit", "quit"}:
                    print("Goodbye!")
                    break

                if not user_input:
                    continue

                messages.append({"role": "user", "content": user_input})

                response = ollama.chat(
                    model=MODEL,
                    messages=messages,
                    tools=TOOLS
                )

                while response.message.tool_calls:
                    messages.append(response.message)

                    for call in response.message.tool_calls:
                        name = call.function.name
                        args = call.function.arguments

                        print(f"\nMODEL REQUESTED TOOL: {name}")
                        print("Arguments:", args)

                        result = await session.call_tool(name, args)
                        result_text = "\n".join(
                            item.text
                            for item in result.content
                            if hasattr(item, "text")
                        )

                        print("MCP TOOL RESULT:", result_text)

                        messages.append({
                            "role": "tool",
                            "tool_name": name,
                            "content": result_text
                        })

                    response = ollama.chat(
                        model=MODEL,
                        messages=messages,
                        tools=TOOLS
                    )

                messages.append(response.message)
                print("\nAssistant:", response.message.content)


if __name__ == "__main__":
    asyncio.run(main())
