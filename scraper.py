import requests
from bs4 import BeautifulSoup
import time
import random

class EconomicTimesScraper:
    def __init__(self):
        self.base_url = "https://economictimes.indiatimes.com/industry/indl-goods/svs/engineering"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def get_article_links(self, num_pages=5):
        links = []
        for page in range(1, num_pages + 1):
            url = f"{self.base_url}/articlelist/{page}.cms"
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('div', class_='eachStory')
            
            for article in articles:
                link = article.find('a')['href']
                full_link = f"https://economictimes.indiatimes.com{link}"
                links.append(full_link)
            
            time.sleep(random.uniform(1, 3))  
        
        return links

    def scrape_article(self, url):
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title_element = soup.find('h1', class_='artTitle font_faus')
        title = title_element.text.strip() if title_element else ""
        
        content_element = soup.find('article', attrs={'data-ga-category': 'Article'})
        if content_element:
            
            for unwanted in content_element.find_all(['script', 'style', 'aside']):
                unwanted.decompose()
            
        
            paragraphs = content_element.find_all('p')
            content = ' '.join([p.text.strip() for p in paragraphs])
        else:
            content = ""
        
    
        date_element = soup.find('time', class_='publish_on')
        date = date_element.text.strip() if date_element else ""
        
        return {
            "title": title,
            "content": content,
            "date": date,
            "url": url
        }

    def scrape_multiple_articles(self, num_articles=50):
        links = self.get_article_links(num_pages=10)  
        articles = []
        
        for link in links[:num_articles]:
            article = self.scrape_article(link)
            if article['content']:  
                articles.append(article)
                print(f"Scraped: {article['title']}")
            else:
                print(f"Failed to scrape content from: {link}")
            time.sleep(random.uniform(1, 3))  
        
        return articles

if __name__ == "__main__":
    scraper = EconomicTimesScraper()
    articles = scraper.scrape_multiple_articles(10)  
    for article in articles:
        print(f"Title: {article['title']}")
        print(f"Date: {article['date']}")
        print(f"URL: {article['url']}")
        print(f"Content snippet: {article['content'][:100]}...")  
        print("---")