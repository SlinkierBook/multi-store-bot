import logging
from datetime import datetime
from bank import (
    create_database, add_product, add_price,
    list_products, get_history, backup_bank
)
from stores.manager import Manager
from config import configure_log
from security import validate_url, validate_name, validate_price
from mail import send_email

configure_log()

def register_product():
    name = input("Product name: ")
    url = input("URL: ")
    target = input("Target price (optional): ")
    
    if not validate_name(name):
        print("Invalid name!")
        return
    
    manager = Manager()
    store = manager.find_store(url)
    
    if store is None:
        print("Site not supported!")
        return
    
    if not validate_url(url, [store.url_base]):
        print("Invalid URL!")
        return
    
    target_price = None
    if target:
        if not validate_price(target):
            print("Invalid price!")
            return
        target_price = float(target)
    
    add_product(name, url, store.name, target_price)
    print("Product registered!")


def monitor():
    manager = Manager()
    products = list_products()
    
    for product in products:
        id, name, url, store, target_price, active = product
        
        store_obj = manager.find_store(url)
        
        if store_obj is None:
            continue
        
        try:
            price = store_obj.get_price(url)
            
            if price:
                date = datetime.now().strftime("%Y-%m-%d %H:%M")
                add_price(id, price, date)
                print(f"{name}: {price}")

                if target_price and price <= target_price:
                    print(f"The price has gone down!:  £{target_price}")
                    send_email(name, price, target_price)

        except Exception as e:
            logging.error(f"Error: {e}")


def menu():
    create_database()
    
    while True:
        print("\n===== MULTI-STORE BOT =====")
        print("1. Register product")
        print("2. Monitor prices")
        print("3. List products")
        print("4. View history")
        print("5. Backup")
        print("6. To go out")
        
        choice = input("\nChoice: ")
        
        if choice == "1":
            register_product()
        
        elif choice == "2":
            monitor()
        
        elif choice == "3":
            products = list_products()
            for p in products:
                print(f"ID: {p[0]} | {p[1]} | {p[3]} | £{p[4]}")
        
        elif choice == "4":
            pid = int(input("Product ID: "))
            history = get_history(pid)
            for h in history:
                print(f"{h[3]} - £{h[2]}")
        
        elif choice == "5":
            backup_bank()
            print("Backup created!")
        
        elif choice == "6":
            print("Leaving...")
            break


if __name__ == "__main__":
    menu()