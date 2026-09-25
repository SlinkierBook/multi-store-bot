import logging
import requests
from bs4 import BeautifulSoup
from .base import Store
from config import configure_log

configure_log()

class QuotesToScrape(Store):
    def __init__(self):
        super().__init__("Quotes to Scrape", "https://quotes.toscrape.com/")

    def get_price(self, url):
        return None
    
    def extract(self, url):
        response = requests.get(url)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")
        
        quotes = soup.find_all("div", class_="quote")
        
        results = []
        for quote in quotes:
            text = quote.find("span", class_="text").text
            author = quote.find("small", class_="author").text
            results.append({"text": text, "author": author})

        logging.info(f"Extracted {len(results)} items of {url}")

        return results