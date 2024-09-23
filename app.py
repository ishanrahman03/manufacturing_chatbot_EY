import streamlit as st
from llm import LLMIntegration
import os

api_key = os.getenv("OPENAI_API_KEY")
llm = LLMIntegration(api_key)

st.title("Manufacturing and Supply Chain Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to know about Indian manufacturing?"):
    
    st.chat_message("user").markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = llm.generate_response(prompt)
    
    
    with st.chat_message("assistant"):
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

st.sidebar.title("Features")

st.sidebar.subheader("Article Search")
search_query = st.sidebar.text_input("Search for articles:")
if st.sidebar.button("Search"):
    results = llm.search.full_text_search(search_query)
    if results:
        st.sidebar.write("Search Results:")
        for result in results:
            st.sidebar.write(f"- [{result[1]}]({result[4]})")
    else:
        st.sidebar.write("No results found.")

st.sidebar.subheader("Information Extraction")
article_content = st.sidebar.text_area("Paste article content for information extraction:")
if st.sidebar.button("Extract Information"):
    structured_info = llm.extract_structured_info(article_content)
    st.sidebar.write("Extracted Information:")
    st.sidebar.write(structured_info)

if __name__ == "__main__":
    st.sidebar.info("This chatbot is powered by GPT-4 and uses data from The Economic Times.")
