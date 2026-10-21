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

            messages = [{
                "role": "user",
                "content": "Use word_count to count the words in this exact text: MCP tools connect agents with external functions."
            }]

            response = ollama.chat(
                model=MODEL, messages=messages, tools=TOOLS
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
                        item.text for item in result.content
                        if hasattr(item, "text")
                    )
                    print("MCP TOOL RESULT:", result_text)

                    messages.append({
                        "role": "tool",
                        "tool_name": name,
                        "content": result_text
                    })

                response = ollama.chat(
                    model=MODEL, messages=messages, tools=TOOLS
                )

            print("\nFINAL ANSWER:", response.message.content)

asyncio.run(main())

