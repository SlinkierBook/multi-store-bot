import logging
from playwright.sync_api import sync_playwright
from .base import Store
from config import configure_log

configure_log()

class QuotesJS(Store):
    def __init__(self):
        super().__init__("Quotes JS", "https://quotes.toscrape.com/js/")

    def block_request(self, route):
        url = route.request.url

        permitted = [
            "quotes.toscrape.com",
            "cdn.jsdelivr.net",
            "maxcdn.bootstrapcdn.com",
        ]

        if any(domain in url for domain in permitted):
            route.continue_()
        else:
            print(f"blocked: {url}")
            route.abort()

    def extract(self, url):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()

            page.route("**/*",self.block_request)
            
            try:
                page.goto(url, timeout=30000)
            except Exception as e:
                logging.error(f"Error accessing {url}: {e}")
                browser.close()
                return []

            quotes = page.query_selector_all("div.quote")

            results = []
            for quote in quotes:
                text = quote.query_selector("span.text").text_content()
                author =  quote.query_selector("small.author").text_content()
                results.append({"text": text, "author": author})

            browser.close()

            logging.info(f"Extracted {len(results)} items of {url}")

            return results