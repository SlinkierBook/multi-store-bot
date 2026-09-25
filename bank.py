import sqlite3
import logging
import datetime

DB_PATH = "/app/data/bot.db"

def create_users_table():
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    
    conexao.commit()
    conexao.close()

def create_database():
    create_users_table()

    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        name TEXT NOT NULL,
        url TEXT NOT NULL,
        store TEXT NOT NULL,
        target_price REAL,
        active INTEGER DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY,
            product_id INTEGER NOT NULL,
            price REAL NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(id)
    )        
""")

    conexao.commit()
    conexao.close()

    logging.info("Database created/verified")

def add_user(email, password_hash, created_at):
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    
    cursor.execute(
        "INSERT INTO users (email, password_hash, created_at) VALUES (?, ?, ?)",
        (email, password_hash, created_at)
    )
    
    conexao.commit()
    conexao.close()


def get_user_by_email(email):
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    
    conexao.close()
    
    return user


def get_user_by_id(user_id):
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    
    conexao.close()
    
    return user

def get_all_user_ids():
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    
    cursor.execute("SELECT id FROM users")
    ids = [row[0] for row in cursor.fetchall()]
    
    conexao.close()
    
    return ids

def add_product(user_id, name, url, store, target_price=None):
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO products (user_id, name, url, store, target_price) VALUES(?,?,?,?,?)",
        (user_id, name, url, store, target_price)
    )

    conexao.commit()
    conexao.close()

    logging.info(f"Product added: {name}")

def add_price(product_id, price, date):
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO history (product_id, price, date)VALUES(?,?,?)",
        (product_id, price, date)
    )

    conexao.commit()
    conexao.close()

    logging.info(f"Saved price: product {product_id} - {price}")

def backup_bank():
    data = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    origin = "/app/data/bot.db"
    destination = f"/app/data/backup_{data}.db"

    conexao_origem = sqlite3.connect(origin)
    conexao_destino = sqlite3.connect(destination)
    
    conexao_origem.backup(conexao_destino)
    
    conexao_destino.close()
    conexao_origem.close()
    
    logging.info(f"Backup criado: {destination}")

def list_products(user_id):
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    
    cursor.execute(
        "SELECT * FROM products WHERE user_id = ? AND active = 1",
        (user_id,)
    )
    products = cursor.fetchall()
    
    conexao.close()
    
    return products

def get_history(product_id):
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM history WHERE product_id = ? ORDER BY date",
        (product_id,)
    )
    history =  cursor.fetchall()

    conexao.close()

    return history