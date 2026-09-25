FROM python:3.14-slim

RUN apt-get update && apt-get install -y \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install playwright
RUN playwright install chromium
RUN playwright install-deps chromium

RUN mkdir -p /app/logs /app/data

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]