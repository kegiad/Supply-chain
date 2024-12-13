import sqlite3

db_name = 'news_data.db'
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

cursor.execute("SELECT * FROM news_articles")
articles = cursor.fetchall()

print("ID | Title | Sentiment")
print("-------------------------")
for article in articles:
    print(f"{article[0]} | {article[1]} | {article[3]}")

conn.close()