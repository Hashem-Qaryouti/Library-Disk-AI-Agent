from langchain_core.tools import Tool
from langchain_ollama import ChatOllama
from server.tools import find_books, create_order, restock_book, update_price, order_status, inventory_summary

from pathlib import Path
DEBUG = False

# Load system prompt
PROMPT_FILE = Path(__file__).parent.parent / "prompts" / "bookstore_prompt.txt"
with open(PROMPT_FILE, "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()
    
if DEBUG:
    print(SYSTEM_PROMPT)

external_tools = [
    Tool(
        name="find_books",
        func=find_books,
        description="Search for books by title or author."
    ),
    Tool(
        name="create_order",
        func=create_order,
        description="Create an order for a customer and reduce stock by usin the customer_id and list of items."
    ),
    Tool(
        name="restock_book",
        func=restock_book,
        description="Restock a book by a book_identifier. Call with JSON: {'book_identifier': '...', 'qty': ...}"
    ),
    Tool(
        name="update_price",
        func=update_price,
        description="Update the price of a book by ISBN."
    ),
    Tool(
        name="order_status",
        func=order_status,
        description="Return the status of an order using the order_id param."
    ),
    Tool(
        name="inventory_summary",
        func=inventory_summary,
        description="Get a summary of books that are low in stock."
    )
]

# -------------------------
llm = ChatOllama(
    model="llama3.1",
    temperature=0,
).bind_tools(tools=external_tools)