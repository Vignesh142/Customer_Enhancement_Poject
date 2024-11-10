# llm_utils.py
from groq import Groq
import csv
import os

def get_llm_response(faq_answer, query, api_key, max_tokens=100):
    """Enhances FAQ answer using the LLM (Groq API)."""
    client = Groq(api_key=api_key)
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"A customer asked: '{query}'. The answer is: '{faq_answer}'. Please rephrase it politely and directly, only answering the customer's question in plain text."
            }
        ],
        model="llama3-8b-8192",
    )
    
    return chat_completion.choices[0].message.content

def classify_query(query, categories, api_key):
    """Classifies a query into one of the given categories using the Groq API."""
    client = Groq(api_key=api_key)
    
    prompt = f"Classify the following query into one of these categories: {', '.join(categories)}.\n\nQuery: '{query}'. Output only the Category name"

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama3-8b-8192",
    )

    # Extract the response and return the category
    response_text = chat_completion.choices[0].message.content.strip()
    return response_text

def save_query_and_category(query, category, file_path="query_classification_log.csv"):
    """Appends the query and its category to a CSV file."""
    new_path = os.path.join(os.path.dirname(__file__), "../data", file_path)
    os.makedirs(os.path.dirname(new_path), exist_ok=True)

    with open(new_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([query, category])
        
def get_summarization_response(text, api_key, max_tokens=100):
    """Summarizes the input text using the Groq API."""
    prompt = f"Summarize the following text in one sentence for a quick overview while retaining its main meaning: '{text}'.Don't try to explain the query, just summarize it that evaluator can understand."
    client = Groq(api_key=api_key)
    # Create a chat completion request for summarization
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama3-8b-8192",
    )

    # Extract and return the summarized content
    return chat_completion.choices[0].message.content.strip()

def save_summary_log(query, summary, file_path="query_summary_log.csv"):
    """Appends the original query and its summary to a CSV file."""
    new_path = os.path.join(os.path.dirname(__file__), "../data", file_path)
    os.makedirs(os.path.dirname(new_path), exist_ok=True)
    with open(new_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([query, summary])

def get_sentiment_analysis(text, api_key):
    """Performs sentiment analysis on the input text using the Groq API."""
    client = Groq(api_key=api_key)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Analyze the sentiment of the following text: '{text}', and provide the sentiment label and score (positive/negative/neutral). Only output the sentiment label."
            }
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content