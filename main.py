import requests
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")

db_name = 'news_data.db'
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS news_articles(
    id INTEGER PRIMARY KEY,
    title TEXT,
    content TEXT
)
''')

url = "https://serpapi.com/search"
params = {
    "engine": "google_news",
    "q": "supply chain",
    "api_key": "75ba95ecc54b9c7c99fe24e1f32cd477dbea855b0dc10e632e7b4bcd08e0c664"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    for article in data.get("news_results", []):  # The key for articles is usually 'news_results'
        title = article.get("title", "No title found")
        content = article.get("snippet", "No content found")  # 'snippet' often contains the summary/content
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
