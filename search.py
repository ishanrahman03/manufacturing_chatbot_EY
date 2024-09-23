import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class Search:
    def __init__(self, db_name='manufacturing_articles.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    def full_text_search(self, query, limit=5):
        self.cursor.execute('''
        SELECT id, title, content, date, url
        FROM articles
        WHERE title LIKE ? OR content LIKE ?
        LIMIT ?
        ''', (f'%{query}%', f'%{query}%', limit))
        return self.cursor.fetchall()

    def generate_embedding(self, text):
        return self.model.encode(text)

    def similarity_search(self, query, limit=5):
        query_embedding = self.generate_embedding(query)
        
        self.cursor.execute('SELECT id, title, content, date, url, embedding FROM articles')
        articles = self.cursor.fetchall()
        
        similarities = []
        for article in articles:
            article_embedding = np.frombuffer(article[5], dtype=np.float32)
            similarity = cosine_similarity([query_embedding], [article_embedding])[0][0]
            similarities.append((article, similarity))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [article for article, _ in similarities[:limit]]

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    search = Search()
    

    print("Full-text search results:")
    results = search.full_text_search("manufacturing")
    for result in results:
        print(f"Title: {result[1]}")
        print(f"URL: {result[4]}")
        print("---")
    
    print("\nSimilarity search results:")
    results = search.similarity_search("latest trends in Indian manufacturing")
    for result in results:
        print(f"Title: {result[1]}")
        print(f"URL: {result[4]}")
        print("---")
    
    search.close()
