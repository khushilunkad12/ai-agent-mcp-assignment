from mcp.server.fastmcp import FastMCP

mcp = FastMCP("practice-agent-server")

EMPLOYEES = {
    "E101": {"name": "Aarav", "department": "Engineering"},
    "E102": {"name": "Diya", "department": "Testing"},
    "E103": {"name": "Rohan", "department": "Data"},
}

@mcp.tool()
def word_count(text: str) -> int:
    """Count the words in the given text."""
    return len(text.split())

@mcp.tool()
def lookup_employee(employee_id: str) -> dict:
    """Look up an employee's name and department using their employee ID."""
    normalized_id = employee_id.strip().upper()
    if normalized_id.isdigit():
        normalized_id = "E" + normalized_id

    employee = EMPLOYEES.get(normalized_id)
    if employee is None:
        return {"error": "Employee not found"}
    return {"employee_id": normalized_id, **employee}

if __name__ == "__main__":
    mcp.run()
