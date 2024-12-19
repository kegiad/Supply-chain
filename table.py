import requests
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")

db_name = 'news_data.db'
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

url = "https://serpapi.com/search"
params = {
    "engine": "google_news",
    "q": "supply chain",
    "api_key": API_KEY
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    for article in data.get("news_results", []):
        title = article.get("title", "No title found")
        content = article.get("snippet", "No content found")
        print(title)
        cursor.execute('''INSERT INTO news_articles(title,content) VALUES(?,?)''',(title,content))
    conn.commit()
else:
    print(f"Error: {response.status_code}")

cursor.execute("SELECT * FROM news_articles")

articles = cursor.fetchall()

for article in articles:
    print(f"Title: {article[1]}")
    print(f"Content: {article[2]}\n")

conn.close()