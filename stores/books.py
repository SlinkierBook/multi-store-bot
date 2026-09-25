import logging
import requests
from bs4 import BeautifulSoup
from .base import Store
from config import configure_log

configure_log()

class BooksToScrape(Store):
    def __init__(self):
        super().__init__("Books to Scrape", "https://books.toscrape.com/")

    def get_price(self, url):
        results = self.extract(url)
        return results[0]["price"]

    def extract(self, url):
        response = requests.get(url)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")
        
        books = soup.find_all("article", class_="product_pod")
        
        results = []
        for book in books:
            title = book.h3.a.get("title")
            price_text = book.find("p", class_="price_color").text
            price = float(price_text.replace("£", ""))
            results.append({"title": title, "price": price})

        logging.info(f"Extracted {len(results)} items of {url}")

        return results