from .books import BooksToScrape
from .quotes import QuotesToScrape
from .quotesjs import QuotesJS


class Manager:
    def __init__(self):
        self.stores = [
            BooksToScrape(),
            QuotesToScrape(),
            QuotesJS(),
        ]

    def find_store(self, url): 
        for store in self.stores:
            if store.url_base in url:
                return store
        return None

    def extract(self,url):
        store = self.find_store(url)

        if store is None:
            return None

        return store.extract(url)

    def list_stores(self):
        for store in self.stores:
            print(f"- {store.name}: {store.url_base}")