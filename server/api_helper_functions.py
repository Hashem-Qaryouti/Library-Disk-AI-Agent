from server.db import execute_db
import json
from server.agent import SYSTEM_PROMPT, llm,external_tools

def store_message(session_id: str, role: str, content: str):
    execute_db(
        "INSERT INTO messages (session_id, role, context) VALUES (?, ?, ?)",
        (session_id, role, content)
    )

def store_tool_call(session_id: str, name: str, args: dict, result: dict):
    execute_db(
        "INSERT INTO tool_calls (session_id, name, args_json, result_json) VALUES (?, ?, ?, ?)",
        (session_id, name, json.dumps(args), json.dumps(result))
    )

def call_agent(user_query: str):
    messages = [
        ("system", SYSTEM_PROMPT),
        ("human", user_query)
    ]
    result = llm.invoke(messages)
    print(result.tool_calls)
    executed_tools = []

    if hasattr(result, "tool_calls") and result.tool_calls:
        for call in result.tool_calls:
            tool_name = call["name"]
            args = call["args"]

            # Execute the corresponding tool
            output = None
            for t in external_tools:
                if t.name == tool_name:
                    output = t.func(**args)
                    print("Tool executed:", output)
                    break

            # Store in TOOL_CALLS table
            executed_tools.append({
                "tool_name": tool_name,
                "args": args,
                "output": output
            })
    else:
        # No tool calls executed, then log a pseudo-tool call
        print("No tool calls were executed.")
        executed_tools.append({
            "tool_name": "LLM_Response",
            "args": {},
            "output": getattr(result, "content", "No response from agent")
        })

    return executed_tools

    