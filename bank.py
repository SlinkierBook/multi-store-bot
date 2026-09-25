import psycopg2
import logging
import datetime
import os


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/bot")


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def create_users_table():
    conexao = get_connection()
    cursor = conexao.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    
    conexao.commit()
    cursor.close()
    conexao.close()


def create_database():
    create_users_table()
    
    conexao = get_connection()
    cursor = conexao.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            store TEXT NOT NULL,
            target_price REAL,
            active INTEGER DEFAULT 1
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id SERIAL PRIMARY KEY,
            product_id INTEGER NOT NULL REFERENCES products(id),
            price REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)
    
    conexao.commit()
    cursor.close()
    conexao.close()
    
    logging.info("Database created/verified")


def add_user(email, password_hash, created_at):
    conexao = get_connection()
    cursor = conexao.cursor()
    
    cursor.execute(
        "INSERT INTO users (email, password_hash, created_at) VALUES (%s, %s, %s)",
        (email, password_hash, created_at)
    )
    
    conexao.commit()
    cursor.close()
    conexao.close()


def get_user_by_email(email):
    conexao = get_connection()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    
    cursor.close()
    conexao.close()
    
    return user


def get_user_by_id(user_id):
    conexao = get_connection()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    
    cursor.close()
    conexao.close()
    
    return user


def get_all_user_ids():
    conexao = get_connection()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT id FROM users")
    ids = [row[0] for row in cursor.fetchall()]
    
    cursor.close()
    conexao.close()
    
    return ids


def add_product(user_id, name, url, store, target_price=None):
    conexao = get_connection()
    cursor = conexao.cursor()
    
    cursor.execute(
        "INSERT INTO products (user_id, name, url, store, target_price) VALUES (%s, %s, %s, %s, %s)",
        (user_id, name, url, store, target_price)
    )
    
    conexao.commit()
    cursor.close()
    conexao.close()
    
    logging.info(f"Product added: {name}")


def add_price(product_id, price, date):
    conexao = get_connection()
    cursor = conexao.cursor()
    
    cursor.execute(
        "INSERT INTO history (product_id, price, date) VALUES (%s, %s, %s)",
        (product_id, price, date)
    )
    
    conexao.commit()
    cursor.close()
    conexao.close()
    
    logging.info(f"Saved price: product {product_id} - {price}")


def list_products(user_id):
    conexao = get_connection()
    cursor = conexao.cursor()
    
    cursor.execute(
        "SELECT * FROM products WHERE user_id = %s AND active = 1",
        (user_id,)
    )
    products = cursor.fetchall()
    
    cursor.close()
    conexao.close()
    
    return products


def get_history(product_id):
    conexao = get_connection()
    cursor = conexao.cursor()
    
    cursor.execute(
        "SELECT * FROM history WHERE product_id = %s ORDER BY date",
        (product_id,)
    )
    history = cursor.fetchall()
    
    cursor.close()
    conexao.close()
    
    return history


def backup_bank():
    data = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    
    conexao = get_connection()
    cursor = conexao.cursor()
    
    logging.info(f"Backup managed by Render: {data}")