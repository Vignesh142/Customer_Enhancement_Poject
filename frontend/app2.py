import streamlit as st
import requests

# Replace with your environment variable handling if needed
GROQ_KEY = "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"

# API URLs for different tasks
FAQ_API_URL = "http://127.0.0.1:5000/faq"  # Example API for FAQ Bot
CLASSIFICATION_API_URL = "http://127.0.0.1:5000/classify"  # Example API for Text Classification
SUMMARIZATION_API_URL = "http://127.0.0.1:5000/summarize"  # Example API for Text Summarization
SENTIMENT_ANALYSIS_API_URL = "http://127.0.0.1:5000/sentiment"  # Example API for Sentiment Analysis
GENERATE_FORM_API_URL = "http://127.0.0.1:5000/api/generateForm"  # Example API for generating a form

# Function to call the FAQ API
def call_faq_api(query):
    response = requests.post(FAQ_API_URL, json={"query": query, "groq_api_key": GROQ_KEY})
    if response.status_code == 200:
        return response.json().get("response", "No answer found.")
    else:
        return f"Error: {response.status_code} - Could not fetch answer from the API."

# Function to call the Text Classification API
def call_classification_api(text):
    response = requests.post(CLASSIFICATION_API_URL, json={"query": text, "groq_api_key": GROQ_KEY})
    if response.status_code == 200:
        label = response.json().get("category", "No label found.")
        save_to_csv(text, label)
        return label
    else:
        return f"Error: {response.status_code} - Could not classify the text."

# Function to call the Summarization API
def call_summarization_api(text):
    response = requests.post(SUMMARIZATION_API_URL, json={"query": text, "groq_api_key": GROQ_KEY})
    if response.status_code == 200:
        return response.json().get("summary", "No summary found.")
    else:
        return f"Error: {response.status_code} - Could not summarize the text."

def call_sentiment_analysis_api(text):
    """Sends a request to the sentiment analysis endpoint and returns the result."""
    response = requests.post(SENTIMENT_ANALYSIS_API_URL, json={"query": text, "groq_api_key": GROQ_KEY})
    if response.status_code == 200:
        sentiment_result = response.json().get("sentiment", "No sentiment found.")

        return f"Sentiment: {sentiment_result}"
    else:
        return "Error: Could not analyze sentiment."

# Function to save query and label to a CSV file
def save_to_csv(query, label, file_path="classified_queries.csv"):
    with open(file_path, mode="a") as file:
        file.write(f"{query},{label}\n")

# Function to call the Generate Form API
def generate_form():
    response = requests.post(GENERATE_FORM_API_URL)
    print(response)
    if response.status_code == 200:
        unique_url = response.json().get("url", "")
        return unique_url
    else:
        return "Error generating form."

# Streamlit Layout
st.title("AI Model Interaction")

# Sidebar with sections for testing and generating form
st.sidebar.header("Navigation")
section = st.sidebar.radio("Select a section", ["Testing", "Generate Form"])

if section == "Testing":
    st.sidebar.subheader("Model Testing")
    task = st.selectbox("Select Task", ["FAQ Bot", "Text Classification", "Text Summarization", "Sentiment Analysis"])
    text_input = st.text_area("Enter your query/text here")
    
    if task == "FAQ Bot":
        if text_input:
            result = call_faq_api(text_input)
            st.write(result)
    elif task == "Text Classification":
        if text_input:
            result = call_classification_api(text_input)
            st.write(result)
    elif task == "Text Summarization":
        if text_input:
            result = call_summarization_api(text_input)
            st.write(result)
    elif task == "Sentiment Analysis":
        if text_input:
            result = call_sentiment_analysis_api(text_input)
            st.write(result)

elif section == "Generate Form":
    st.sidebar.subheader("Form Generation")
    generate_button = st.button("Generate Form URL")
    
    if generate_button:
        form_url = generate_form()
        st.text_input("Generated Form URL", form_url, key="form_url", disabled=True)
        
        if form_url:
            st.write(f"Click the link to open the form: [Open Form]({form_url})")

            # To generate a new form URL
            new_generate_button = st.button("Generate New URL")
            if new_generate_button:
                new_form_url = generate_form()
                st.text_input("Generated Form URL", new_form_url, key="new_form_url", disabled=True)
                st.write(f"Click the link to open the new form: [Open Form]({new_form_url})")
