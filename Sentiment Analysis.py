import sqlite3
from textblob import TextBlob

db_name = 'news_data.db'
conn = sqlite3.connect(db_name)
cursor = conn.cursor()
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        return "Positive"
    elif sentiment < 0:
        return "Negative"
    else:
        return "Neutral"

cursor.execute("SELECT * FROM news_articles")
articles = cursor.fetchall()

for article in articles:
    title = article[1]
    content = article[2]
    sentiment = analyze_sentiment(title)
    print(f"Title : {title}")
    print(f"Sentiment : {sentiment}")

cursor.execute("ALTER TABLE news_articles ADD COLUMN Sentiment TEXT")
print("SUCCESSFULLY ADDED DATA")
cursor.execute("SELECT * FROM news_articles")
articles = cursor.fetchall()

for article in articles:
    article_id = article[0]
    title = article[1]
    sentiment = analyze_sentiment(title)
    cursor.execute("UPDATE news_articles SET Sentiment = ? WHERE id = ?", (sentiment,article_id))

conn.commit()

cursor.execute("SELECT * FROM news_articles")
articles = cursor.fetchall()


print("ID | Title | Sentiment")
print("-------------------------")
for article in articles:
    print(f"{article[0]} | {article[1]} | {article[3]}")
cursor.execute("SELECT title, COUNT(*) FROM news_articles GROUP BY title HAVING COUNT(*) > 1")
conn.close()