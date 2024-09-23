
# Manufacturing and Supply Chain Assistant Chatbot

## Overview

The **Manufacturing and Supply Chain Assistant Chatbot** is designed to assist users in retrieving relevant information regarding supply chain and manufacturing processes. This chatbot can search a database of articles, respond to user queries using a natural language model, and was intended to scrape real-time data from the web.

## Project Structure


app.py                    # Main application logic
database.py                # Database connection and query management
llm.py                     # Language model interaction
main.py                    # Entry point of the chatbot
scraper.py                 # Web scraping functionality (currently non-functional)
search.py                  # Article search functionality
manufacturing_articles.db  # SQLite database of manufacturing and supply chain articles


## Files and Descriptions

1. **app.py**: Main application for handling user requests and generating responses.
2. **database.py**: Manages the database connection and queries.
3. **llm.py**: Manages interactions with the language model.
4. **main.py**: Entry point of the chatbot application.
5. **scraper.py**: Scraping module (non-functional).
6. **search.py**: Search module to query articles.
7. **manufacturing_articles.db**: SQLite database storing articles.

## Setup Instructions

### Prerequisites

- Python 3.x
- SQLite3
- Required Python libraries (can be installed from `requirements.txt`)

### Installing Dependencies

```bash
pip install -r requirements.txt
```

### Running the Application

```bash
python main.py
```

## Database

Uses SQLite to store and retrieve articles.

## Search Functionality

Implements keyword-based article search from the database.

## Web Scraper (Non-Functional)

The `scraper.py` module is currently non-functional due to website limitations (CAPTCHA, dynamic content).

## Potential Improvements

- Enhance the scraper to handle CAPTCHA and dynamic content.
- Improve search functionality with advanced search features.
- Add real-time data fetching via APIs.

## License

This project is licensed under the MIT License.
