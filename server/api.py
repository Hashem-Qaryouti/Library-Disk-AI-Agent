from fastapi import FastAPI
from pydantic import BaseModel
from server.api_helper_functions import store_message,store_tool_call,call_agent
from server.db import query_db

app = FastAPI()

# Request model
class QueryRequest(BaseModel):
    session_id: str
    query: str

# Health check endpoint
@app.get("/")
def root():
    return {"message": "Library Desk Agent API running."}

# Chat endpoint
@app.post("/chat")
def chat(req: QueryRequest):
    session_id = req.session_id
    user_query = req.query
    
    # 1. Store user message
    store_message(session_id, "user", user_query)

    # 2. Send message to LLM (LangChain)
    prompt_messages = [{"role": "user", "content": user_query}]

    # 3. Call the agent
    executed_tools = call_agent(user_query)

    final_response = ""
    for tool in executed_tools:
        # Store each tool execution in TOOL_CALLS table
        store_tool_call(session_id, tool["tool_name"], tool["args"], tool["output"])
        final_response += f"{tool['tool_name']}: {tool['output']}\n"

    # 4. Store agent final response
    store_message(session_id, "agent", final_response)

    # 5. Return the response
    return {"response": final_response.strip()}
    
@app.get("/history")
def get_session_history(session_id: str):
    print("Relaoding previous history")
    rows = query_db(
        "SELECT role, context FROM messages WHERE session_id = ? ORDER BY id ASC",
        (session_id,)
    )

    messages = [{"role": r["role"], "context": r["context"]} for r in rows]

    return {"session_id": session_id, "messages": messages}