version: '3.8'
services:
  ssl:
    build: ./ssl
    ports:
      - '8000:8000'
  phishing:
    build: ./phishing
    ports:
      - '8001:8001'
  reconng:
    build: ./reconng
    ports:
      - '8002:8002'
  theharvester:
    build: ./theharvester
    ports:
      - '8003:8003'
  spiderfoot:
    build: ./spiderfoot
    ports:
      - '5001:5001'
networks:
  default:
    driver: bridge
