from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from auth import register_user, authenticate, load_user
from bank import (
    create_database, add_product, add_price,
    list_products, get_history, backup_bank
)
from stores.manager import Manager
from config import configure_log
from security import validate_url, validate_name, validate_price
from mail import send_email
from datetime import datetime
import threading
import schedule
import time
import logging


configure_log()

app = Flask(__name__)
app.secret_key = "change_this_key_to_something_secret"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

create_database()

@login_manager.user_loader
def user_loader(user_id):
    return load_user(user_id)

def monitor_task(user_id):
    manager = Manager()
    products = list_products(user_id)
    
    for product in products:
        id,user_id_db, name, url, store, target_price, active = product
        store_obj = manager.find_store(url)
        
        if store_obj is None:
            continue
        
        try:
            price = store_obj.get_price(url)
            
            if price:
                date = datetime.now().strftime("%Y-%m-%d %H:%M")
                add_price(id, price, date)
                logging.info(f"Auto: {name} - £{price}")
                
                if target_price and price <= target_price:
                    logging.info(f"Auto: {name} baixou! £{price} <= £{target_price}")
                    send_email(name, price, target_price)
        except Exception as e:
            logging.error(f"Auto error: {e}")


def run_scheduler():
    schedule.every().hours.do(monitor_all)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

def monitor_all():
    from bank import get_all_user_ids
    for user_id in get_all_user_ids():
        monitor_task(user_id)

scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()


@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect("/products")
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = register_user(email, password)
        
        if user:
            return redirect("/login")
        else:
            flash("Email já cadastrado!")
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = authenticate(email, password)
        
        if user:
            login_user(user)
            return redirect("/products")
        else:
            flash("Email ou senha inválidos!")
    
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/add_product", methods=["POST"])
@login_required
def add_product_route():
    name = request.form.get("name")
    url = request.form.get("url")
    target = request.form.get("target")
    
    if not validate_name(name):
        flash("Invalid name!")
        return redirect("/products")
    
    manager = Manager()
    store = manager.find_store(url)
    
    if store is None:
        flash("Site not supported!")
        return redirect("/products")
    
    if not validate_url(url, [store.url_base]):
        flash("Invalid URL!")
        return redirect("/products")
    
    target_price = None
    if target:
        if not validate_price(target):
            flash("Invalid price!")
            return redirect("/products")
        target_price = float(target)
    
    add_product(current_user.id, name, url, store.name, target_price)
    
    return redirect("/products")

@app.route("/products")
@login_required
def products():
    products = list_products(current_user.id)
    return render_template("products.html", products=products)


@app.route("/monitor")
@login_required
def monitor():
    monitor_task(current_user.id)
    return redirect("/products")


@app.route("/history/<int:product_id>")
@login_required
def history(product_id):
    history = get_history(product_id)
    return render_template("history.html", history=history, product_id=product_id)


@app.route("/backup")
@login_required
def backup():
    backup_bank()
    return redirect("/products")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)