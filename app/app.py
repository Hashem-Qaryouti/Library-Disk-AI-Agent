import streamlit as st
import requests
import json

# Backend API URL
API_URL = "http://localhost:8000/chat"


# Session Management
if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# Sidebar: Session Selector
st.sidebar.title("Library Desk Agent")
session_option = st.sidebar.radio("Select Session:", ["New Session", "Load Session"])

if session_option == "New Session":
    st.session_state.session_id = st.sidebar.text_input("Enter a session name", value="session1")
    if st.sidebar.button("Start New Session"):
        st.session_state.messages = []
        st.success(f"Started new session: {st.session_state.session_id}")

elif session_option == "Load Session":
    st.session_state.session_id = st.sidebar.text_input("Enter session to load", value="session1")

    if st.sidebar.button("Load Session"):
        if not st.session_state.session_id:
            st.warning("Please enter a session ID.")
        else:
            try:
                # Call backend to fetch message history
                resp = requests.get(
                    f"http://localhost:8000/history",
                    params={"session_id": st.session_state.session_id}
                )

                if resp.status_code == 200:
                    data = resp.json()

                    # Load messages into Streamlit memory
                    st.session_state.messages = data.get("messages", [])

                    st.success(f"Loaded session: {st.session_state.session_id}")

                else:
                    st.error("Failed to load session from backend.")

            except Exception as e:
                st.error(f"Error connecting to backend: {e}")


# Main Chat Area
st.title("Library Desk Agent Chat")

# Display chat messages
for msg in st.session_state.messages:
    text = msg.get("content") or msg.get("context") or ""
    if msg["role"] == "user":
        st.markdown(f"**You:** {text}")
    else:
        st.markdown(f"**Agent:** {text}")

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here:")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call backend API
    payload = {"session_id": st.session_state.session_id, "query": user_input}
    try:
        response = requests.post(API_URL, json=payload)
        agent_reply = response.json().get("response", "No response from agent.")
    except Exception as e:
        agent_reply = f"Error connecting to backend: {e}"

    # Add agent response
    st.session_state.messages.append({"role": "agent", "content": agent_reply})