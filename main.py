# main.py
from scraper import EconomicTimesScraper
from database import Database
from search import Search
from llm import LLMIntegration
import os
import streamlit as st

def main():
    
    scraper = EconomicTimesScraper()
    db = Database()
    search = Search()
    api_key = os.getenv("OPENAI_API_KEY")
    llm = LLMIntegration(api_key)

    articles = scraper.scrape_multiple_articles(50)  
    for article in articles:
        db.insert_article(article)

    for article in db.get_all_articles():
        embedding = search.generate_embedding(article[2])  
        db.update_embedding(article[0], embedding.tobytes())

    db.close()
    search.close()
    llm.close()

    print("Data collection and preprocessing complete. Run the Streamlit app to start the chatbot.")

if __name__ == "__main__":
    main()