from openai import OpenAI
from search import Search

class LLMIntegration:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.search = Search()

    def generate_response(self, user_query):
        
        relevant_articles = self.search.similarity_search(user_query, limit=3)
        
        
        context = "\n\n".join([f"Title: {article[1]}\nContent: {article[2]}" for article in relevant_articles])
        
        
        prompt = f"""You are an AI assistant specializing in Indian manufacturing and supply chain management. 
        Use the following articles as context to answer the user's question. If the information is not in the context, 
        use your general knowledge but make it clear that it's not from the specific articles.

        Context:
        {context}

        User Question: {user_query}

        Assistant:"""

        
        response = self.client.chat.completions.create(
            model="gpt-4",  
            messages=[
                {"role": "system", "content": "You are a helpful assistant specializing in Indian manufacturing and supply chain management."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )

        return response.choices[0].message.content.strip()

    def extract_structured_info(self, article_content):
        prompt = f"""Extract the following information from the given article content:
        1. Company names mentioned
        2. Technologies discussed
        3. Industry trends identified

        Article content:
        {article_content}

        Provide the extracted information in a structured format."""

        response = self.client.chat.completions.create(
            model="gpt-4",  # Changed from "gpt-4-turbo-preview" to "gpt-4"
            messages=[
                {"role": "system", "content": "You are an AI assistant that extracts structured information from articles."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )

        return response.choices[0].message.content.strip()

    def close(self):
        self.search.close()

if __name__ == "__main__":
    import os
    api_key = os.getenv("OPENAI_API_KEY")
    llm = LLMIntegration(api_key)
    
    
    user_query = "What are the latest trends in Indian manufacturing?"
    response = llm.generate_response(user_query)
    print(f"User Query: {user_query}")
    print(f"Assistant Response: {response}")
    
    
    sample_article = """
    Tata Motors, India's leading automobile manufacturer, has announced a significant investment in electric vehicle (EV) technology. 
    The company plans to launch 10 new EV models by 2025, focusing on both passenger and commercial vehicles. 
    This move is in line with the growing trend of electrification in the Indian automotive industry, 
    driven by government initiatives and increasing environmental concerns.
    """
    structured_info = llm.extract_structured_info(sample_article)
    print("\nStructured Information Extraction:")
    print(structured_info)
    
    llm.close()