FROM python:3.11-slim

WORKDIR /proxy

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY addon.py .

CMD ["mitmproxy","-s","addon.py","--listen-port","8080"]

