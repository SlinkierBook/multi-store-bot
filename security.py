import re
from urllib.parse import urlparse

def validate_url(url, allowed_sites):
    try:
        parsed = urlparse(url)
    except:
        return False
    if parsed.scheme not in ["http", "https"]:
        return False

    for site in allowed_sites:
        if site in url:
            return True

    return False

def validate_name(name):
    if not name or len(name) < 2 or len(name) >100:
        return False
    if not re.match(r"^[\w\s]+$", name):
        return False
    return True

def validate_price(price):
    try:
        p = float(price)
        if p < 0 or p > 100000:
            return False
        return True
    except:
        return False