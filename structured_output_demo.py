import ollama
from pydantic import BaseModel, Field

class EmployeeResponse(BaseModel):
    employee_id: str = Field(description="Employee ID")
    name: str = Field(description="Employee name")
    department: str = Field(description="Employee department")

prompt = """
Return the employee information in the required structured format:
employee_id: E102
name: Diya
department: Testing
"""

response = ollama.chat(
    model="qwen2.5:3b",
    messages=[{"role": "user", "content": prompt}],
    format=EmployeeResponse.model_json_schema(),
)

print("RAW MODEL OUTPUT:")
print(response.message.content)

employee = EmployeeResponse.model_validate_json(response.message.content)

print("\nVALIDATED PYDANTIC OBJECT:")
print(employee)

print("\nVALIDATION SUCCESSFUL:", employee.model_dump())
