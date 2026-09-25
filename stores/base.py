class Store:
    def __init__(self, name, url_base):
        self.name = name
        self.url_base = url_base

    def get_price(self, url):
        raise NotImplementedError
    
    def extract(self, url):
        raise NotImplementedError
    
    def __str__(self):
        return self.name
    