import sqlite3

conn = sqlite3.connect('orders.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bouquet_name TEXT,
    delivery_time TEXT,
    address TEXT,
    sender_name TEXT,
    recipient_name TEXT,
    card_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()

print("База данных и таблица созданы.")
