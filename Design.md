# Agentic AI Capstone – HR Policy Assistant

## 1. Project Overview

**Use case:** Build an AI-powered HR assistant that retrieves information from an HR leave policy PDF, looks up employee and manager details, prepares a policy summary or email draft, and saves the final output only after receiving explicit user approval.

**Example user request:**

"Summarize the leave policy and prepare an email for the manager of employee E102 explaining the key points."

The agent will understand the request, create a plan, select appropriate tools, execute the required steps, handle errors, and request human approval before saving the final output.

## 2. Agent Workflow

1. Receive and understand the user's request.
2. Create a task plan.
3. Search the uploaded HR policy using the existing RAG pipeline.
4. Look up employee and manager information using MCP.
5. Prepare a summary using the retrieved information.
6. Display the prepared summary to the user.
7. Request explicit user approval before saving.
8. Save the approved summary to a local outbox file.

**Execution limit:** Maximum 8 steps per task.

## 3. Tool Definitions

| Tool | Description | Permission |
|---|---|---|
| `document_search` | Searches the HR policy document using the existing RAG pipeline and returns relevant context. | Read-only |
| `employee_lookup` | Retrieves employee and manager information using an employee ID through MCP. | Read-only |
| `draft_summary` | Prepares a policy summary or email draft using retrieved employee and policy information. | Draft-only |
| `save_summary` | Saves the approved summary or email draft to a local outbox file. | Approval required |

The existing RAG pipeline will be reused for document retrieval. A separate document reader tool is not required.

## 4. Human Approval Mechanism

The `save_summary` tool is the approval-gated operation.

**Approval rules:**

- The agent can retrieve information and prepare drafts without approval.
- Before saving, the agent must display the complete proposed content.
- The agent must request explicit user approval.
- The `save_summary` tool must never be called before explicit approval.
- If approval is denied, the tool must not execute.
- If approval is not provided, the operation remains pending.
- The execution log must record whether approval was granted or denied.
- The agent must never claim that a summary was saved unless the tool confirms successful execution.

The save operation will use a local mock outbox file rather than sending a real email.

## 5. Memory Approach

The agent will maintain two types of memory.

### A. Conversation History

- Stores messages exchanged during the current task.
- Maintains context for follow-up questions.
- Allows the agent to understand references to earlier messages.
- Is cleared when the task ends.

### B. Task Scratchpad

Stores temporary information required for task execution:

- Current task and user objective.
- Planned execution steps.
- Completed steps.
- Tool calls and their results.
- Errors and retry information.
- Current approval status.

The scratchpad is task-scoped and cleared when the task ends.

## 6. Execution Logging and Step Limit

Every execution step will be recorded with:

- Step number.
- Agent reasoning summary.
- Selected tool.
- Tool input.
- Tool result.
- Execution status.
- Approval status, where applicable.

The execution trace will follow:

`Plan → Tool Selection → Tool Execution → Result → Next Step`

The agent will enforce a maximum of 8 execution steps per task to prevent uncontrolled loops.

## 7. Error Handling

The agent should handle:

- Invalid employee IDs, such as E999.
- Missing or unavailable policy information.
- Empty retrieval results.
- Tool execution failures.
- Incomplete employee information.
- Rejected or missing user approval.
- Maximum execution-step limit reached.

The agent must not invent employee details, manager information, or HR policy information.

## 8. Evaluation Strategy

A JSON-based evaluation dataset will contain 16 test cases across four categories:

- **6 normal execution cases:** Successful document retrieval, employee lookup, and summary preparation.
- **4 tool failure cases:** Invalid employee IDs, unavailable tools, and save failures.
- **3 missing-information or clarification cases:** Incomplete requests and unavailable information.
- **3 approval-related cases:** Approval granted, approval denied, and approval required before saving.

Each evaluation case will contain:

- `input`
- `expected_tools`
- `expected_outcome`
- `needs_approval`

Approval-related cases will additionally use:

- `must_not_call_before_approval`

Evaluation will verify:

- Correct tool selection and execution order.
- Accuracy of retrieved information.
- Appropriate error handling.
- Human approval enforcement.
- No fabricated information.
- Compliance with the maximum 8-step execution limit.
- No invocation of `save_summary` before approval.

## 9. Implementation Plan

### Phase 1 – Individual Tool Development

- Connect the existing RAG pipeline as `document_search`.
- Implement `employee_lookup` using MCP.
- Implement `draft_summary`.
- Implement approval-gated `save_summary`.
- Write and run a separate test for each tool before integration.

### Phase 2 – Agent Development

- Implement agent planning and tool selection.
- Integrate conversation history and task scratchpad.
- Implement the 8-step execution limit.
- Add execution logging and error handling.

### Phase 3 – Approval and Evaluation

- Implement the human approval workflow.
- Ensure saving is blocked until explicit approval.
- Create and validate the 16 JSON evaluation cases.
- Run test scenarios and document results.
- Verify the execution traces and evaluation outcomes.

## 10. Expected Outcome

A working HR Policy Assistant that can:

- Understand and plan multi-step user requests.
- Retrieve relevant HR policy information using RAG.
- Retrieve employee and manager information through MCP.
- Prepare accurate summaries or email drafts.
- Request human approval before saving.
- Save approved content to a local outbox file.
- Handle errors without fabricating information.
- Maintain task memory and execution logs.
- Complete tasks within the maximum 8-step limit.

The project will demonstrate tool integration, planning, task-scoped memory, error handling, human-in-the-loop approval, and systematic evaluation of an agentic AI workflow.