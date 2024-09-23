import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='manufacturing_articles.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            date TEXT,
            url TEXT UNIQUE,
            embedding BLOB
        )
        ''')
        self.conn.commit()

    def insert_article(self, article, embedding=None):
        try:
            self.cursor.execute('''
            INSERT OR REPLACE INTO articles (title, content, date, url, embedding)
            VALUES (?, ?, ?, ?, ?)
            ''', (article['title'], article['content'], article['date'], article['url'], embedding))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f"Article with URL {article['url']} already exists in the database.")

    def get_all_articles(self):
        self.cursor.execute('SELECT * FROM articles')
        return self.cursor.fetchall()

    def get_article_by_id(self, article_id):
        self.cursor.execute('SELECT * FROM articles WHERE id = ?', (article_id,))
        return self.cursor.fetchone()

    def update_embedding(self, article_id, embedding):
        self.cursor.execute('UPDATE articles SET embedding = ? WHERE id = ?', (embedding, article_id))
        self.conn.commit()

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = Database()
    test_article = {
        'title': 'Test Article',
        'content': 'This is a test article content.',
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'url': 'https://example.com/test-article'
    }
    db.insert_article(test_article)
    
    articles = db.get_all_articles()
    for article in articles:
        print(article)
    
    db.close()