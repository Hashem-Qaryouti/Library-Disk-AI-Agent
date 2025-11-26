 # Library-Disk-AI-Agent

A conversational AI-powered library/bookstore assistant built with Streamlit for the frontend and FastAPI for the backend. The system leverages LangChain and Ollama to handle queries, execute tools, and manage book orders, inventory, and customer interactions.

---
## 🔁 Agent Wokflow

![RAG Workflow](assets/flowchart.png)
## Features

- **Chat-based interface** to interact with the library agent.
- **Session management**: start new sessions or load previous ones.
- **Database-backed storage**: all user queries, agent responses, and executed tool calls are stored in SQLite.
- **Book management tools**:
  - Search books by title or author
  - Create customer orders
  - Restock books
  - Update book prices
  - Check order status
  - Inventory summary for low-stock books
- **Agent orchestration**: executes tools based on user prompts.

---

## 💡 Example: Streamlit App in Action

Once you run the Streamlit app, you’ll see an interface like this:
![RAG PDF Q&A Example](assets/app_example.png)

## Requirements

- Python 3.10+
- Libraries (can be installed via `requirements.txt`):
- [SQLite3](https://www.sqlite.org/index.html) – For storing messages, tool calls, books, and orders
- [Ollama 3.1](https://ollama.com/) – LLM model used via LangChain Ollama integration

```bash
pip install -r requirements.txt
```
---

## Project Structure
```
.
├── server/
│   ├── __init__.py
│   ├── api.py                  # FastAPI endpoints
│   ├── api_helper_functions.py # Agent helper functions (store messages, call agent)
│   ├── agent.py                # LLM and tools setup
│   ├── db.py                   # Database query and execution functions
│   └── tools.py                # Bookstore business logic functions
├── prompts/
│   └── bookstore_prompt.txt    # System prompt for agent
├── db/
│   ├── library.db              # SQLite database
│   ├── schema.sql              # DB schema definitions
│   └── seed.sql                # Seed data for initial testing
├── app/
│   └── app.py                  # Streamlit frontend
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore file
└── README.md                   # Project README
```
---

## Project Setup
### 1. Clone the repository

```bash
git clone https://github.com/Hashem-Qaryouti/llama3-rag-pipeline.git
cd <your-repo-name>
```
### 2. Create and activate a virtual environment
```bash
python -m venv <your-venv-name>
```
#### Activate the environment:
- **Windows:**
```bash
<your-venv-name>\Scripts\activate
```
- **Linux:**
```bash
source <your-venv-name>/bin/activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt

```

### 4. Set up the Database 
1. Create the SQLite database file (if not already created):

```bash
touch db/library.db
```
2. Initialize the database schema:
 ```bash
sqlite3 db/library.db < db/schema.sql
```
3. Seed the database with initial data:
 ```bash
sqlite3 db/library.db < db/seed.sql
```

### 5. Pull the Ollama Model
```bash
ollama pull llama3.1
```
---

## Usage
1. Run the Backend API
```bash
uvicorn server.api:app --reload --host 0.0.0.0 --port 8000
```
1. Run the Streamlit App
```bash
cd src
streamlit run app/app.py
```
- **Open the URL shown in your terminal (usually http://localhost:8501):**
- **Enter your question in the text box and click Send**
