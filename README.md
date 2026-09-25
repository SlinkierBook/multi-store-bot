# Multi-Store Bot

Price monitoring bot that supports multiple stores, with web interface, authentication, database and email notifications.

## What it does

- Multi-store: supports static sites (requests) and dynamic sites (Playwright)
- Product registration: each user registers their products
- Automatic monitoring: runs every X minutes and saves history
- Email alerts: notifies when price drops below target
- Price history: stores all variations
- Multi-user: email + password login (bcrypt)
- Web interface: Flask + HTML + CSS
- Isolation: runs in Docker
- Logs: records everything with automatic rotation

## Technologies

- Python 3.14
- Flask (web framework)
- Flask-Login (authentication)
- bcrypt (password hashing)
- PostgreSQL (database)
- requests (HTTP requests)
- BeautifulSoup4 (HTML parsing)
- Playwright (browser automation)
- schedule (scheduling)
- Docker (isolation)

## How to run

With Docker:

    docker-compose up

Access http://localhost:5000

Without Docker:

    Requires PostgreSQL running.
    Set DATABASE_URL in .env.
    pip install -r requirements.txt
    python app.py

## Configuration

Create a .env file in the project root:

    DATABASE_URL=postgresql://user:password@host:5432/dbname
    EMAIL_USER=youremail@gmail.com
    EMAIL_PASS=your_app_password
    EMAIL_TO=youremail@gmail.com

Important: use a Gmail app password, not your normal password.

## Structure

    multi-store-bot/
      app.py
      auth.py
      bank.py
      config.py
      mail.py
      security.py
      stores/
      templates/
      static/
      Dockerfile
      docker-compose.yml
      requirements.txt

## Security

- Passwords with bcrypt
- URL validation with whitelist
- SQL with parameters against injection
- External request blocking in Playwright
- Docker isolates the environment
- .env does not go to Git

## Supported stores

- Books to Scrape (static): title + price
- Quotes to Scrape (static): quote + author
- Quotes JS (dynamic): quote + author

## Author

SlinkierBook - https://github.com/SlinkierBook

## License

This project is free to use for study and portfolio.