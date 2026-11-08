import sqlite3

def init_db():
    conn = sqlite3.connect('inventory')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_item(name, quantity, price):
    conn = sqlite3.connect('inventory')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, quantity, price) VALUES (?, ?, ?)", (name, quantity, price))
    conn.commit()
    conn.close()

def get_all_items():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    conn.close()
    return items

def update_item(item_id, name, quantity, price):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET name = ?, quantity = ?, price = ? WHERE id = ?", (name, quantity, price, item_id))
    conn.commit()
    conn.close()

def delete_item(item_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()