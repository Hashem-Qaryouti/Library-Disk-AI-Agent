from server.db import query_db, execute_db
from typing import List, Dict
import json

def find_books(q: str, by: str= "title") -> List[Dict]:
    if by not in ["title", "author"]:
        raise ValueError("Search must be by title or author")
    sql = f"SELECT * FROM BOOKS WHERE {by} LIKE ?"
    book = query_db(sql, (f"%{q}%",))
    return book


def create_order(customer_id: int, items: List[Dict]) -> Dict:
    order_id = execute_db(
        "INSERT INTO ORDERS (customer_id) VALUES (?)",
        (customer_id,)
    )

    for item in items:
        identifier = item.get("book_identifier")
        quantity = item["qty"]

        if identifier is None:
            print("Missing book_identifier in item:", item)
            continue

        # Detect whether identifier is ISBN or title
        if identifier.isdigit():
            book = query_db("SELECT * FROM BOOKS WHERE isbn = ?", (identifier,))
        else:
            book = query_db("SELECT * FROM BOOKS WHERE title LIKE ?", (identifier,))

        if not book:
            print(f"No book found for identifier '{identifier}'")
            continue

        isbn = book[0]["isbn"]

        execute_db(
            "UPDATE BOOKS SET stock = stock - ? WHERE isbn = ?",
            (quantity, isbn)
        )

        execute_db(
            "INSERT INTO order_items (order_id, isbn, quantity) VALUES (?, ?, ?)",
            (order_id, isbn, quantity)
        )
    updated_book = query_db("SELECT * FROM BOOKS WHERE isbn = ?", (isbn,))

    return {"order_id": order_id, "new_stock": updated_book[0]["stock"]}

def restock_book(book_identifier: str, qty: int) -> Dict:
    """
    Restock book quantity.
    If book_identifier is all digits → treat as ISBN.
    Otherwise → treat as title.
    """

    # Determine lookup method
    if book_identifier.isdigit():
        book = query_db("SELECT * FROM BOOKS WHERE isbn = ?", (book_identifier,))
    else:
        book = query_db("SELECT * FROM BOOKS WHERE title = ?", (book_identifier,))

    # Handle missing book
    if not book:
        print(f"No book found for identifier '{book_identifier}'.")
        return {}

    # Extract ISBN (true primary key)
    isbn = book[0]["isbn"]

    # Apply stock update
    execute_db(
        "UPDATE BOOKS SET stock = stock + ? WHERE isbn = ?",
        (qty, isbn)
    )

    # Fetch updated record
    updated = query_db("SELECT * FROM BOOKS WHERE isbn = ?", (isbn,))
    print(f"Updated stock for {updated[0]['title']}: {updated[0]['stock']}")
    return updated[0]

def update_price(book_identifier: str, price: float)->Dict:
    # Determine whether identifier is ISBN or Title
    if book_identifier.isdigit():
        # Identifier is ISBN
        book = query_db("SELECT * FROM BOOKS WHERE isbn = ?", (book_identifier,))
    else:
        # Identifier is a Title
        book = query_db("SELECT * FROM BOOKS WHERE title LIKE ?", (book_identifier,))

    if not book:
        print(f"No book found for identifier '{book_identifier}'")
        return {"error": f"No book found for identifier '{book_identifier}'"}

    book = book[0]
    isbn = book["isbn"]

    # Update price
    execute_db("UPDATE BOOKS SET price = ? WHERE isbn = ?", (price, isbn))

    # Fetch updated info
    updated_book = query_db("SELECT * FROM BOOKS WHERE isbn = ?", (isbn,))
    updated_book = updated_book[0]

    print(f"Updated price for {updated_book['title']} ({isbn}): {updated_book['price']}$")

    return {
        "isbn": updated_book["isbn"],
        "title": updated_book["title"],
        "old_price": book["price"],
        "new_price": updated_book["price"]
    }

def order_status(order_id: int)->Dict:
    sql = """
    SELECT O.id AS order_id,
            O.created_at,
            C.id as customer_id,
            C.name as customer_name,
            C.email as customer_email
            FROM ORDERS O
            JOIN CUSTOMERS C
            ON O.CUSTOMER_ID = C.ID
            WHERE O.id = ?
"""
    order = query_db(sql, (int(order_id),))

    if not order:
        return {"error","Order not found"}
    items = query_db("SELECT * FROM ORDER_ITEMS WHERE order_id = ?", (order_id,))

    return {"order": order[0], "items":items}

def inventory_summary(low_stock_threshold: int=3)->Dict:
    return query_db("SELECT * FROM BOOKS WHERE stock <= ?", (low_stock_threshold,))
