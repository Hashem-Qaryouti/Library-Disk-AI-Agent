from server.db import query_db, execute_db
from typing import List, Dict
import json

def find_books(q: str, by: str= "title") -> List[Dict]:
    if by not in ["title", "author"]:
        raise ValueError("Search must be by title or author")
    sql = f"SELECT * FROM BOOKS WHERE {by} LIKE ?"
    book = query_db(sql, (f"%{q}%",))
    return book

def create_order(customer_id: int, items:List[Dict])->Dict:
    order_id = execute_db("INSERT INTO ORDERS (customer_id) VALUES (?)", (customer_id,))

    for item in items:
        isbn = item['isbn']
        quantity = item['qty']
        execute_db("UPDATE BOOKS set stock = stock - ? WHERE isbn = ?", (quantity, isbn))
        execute_db("INSERT INTO order_items (order_id, isbn, quantity) VALUES (?,?,?)", (order_id, isbn, quantity))
    
    print(f"Order: {order_id} is created")
    return {"order_id":order_id}


def restock_book(isbn: str, qty: int) -> Dict:
    execute_db("UPDATE BOOKS SET stock = stock + ? WHERE isbn = ?", (qty, isbn))
    book = query_db("SELECT * FROM BOOKS WHERE isbn = ?", (isbn,))
    if book:
        print(f"Updated stock for {book[0]['title']}: {book[0]['stock']}")
        return book[0]
    else:
        print(f"No book found with ISBN {isbn}")
        return {}
    
def update_price(isbn: int, price: float)->None:
    execute_db("UPDATE BOOKs set price = ? WHERE isbn = ?", (price, isbn))
    book = query_db("SELECT * FROM BOOKS WHERE isbn = ?", (isbn,))
    print(f"Updated price for {book[0]['isbn']}: {book[0]['price']}$")
    
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
