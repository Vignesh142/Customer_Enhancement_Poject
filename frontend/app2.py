import os
import streamlit as st
import requests
import pandas as pd
import numpy as np
import csv

# Replace with your environment variable handling if needed
GROQ_KEY = "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"

# API URLs for different tasks
FAQ_API_URL = "http://127.0.0.1:5000/faq"  # Example API for FAQ Bot
CLASSIFICATION_API_URL = "http://127.0.0.1:5000/classify"  # Example API for Text Classification
SUMMARIZATION_API_URL = "http://127.0.0.1:5000/summarize"  # Example API for Text Summarization
SENTIMENT_ANALYSIS_API_URL = "http://127.0.0.1:5000/sentiment"  # Example API for Sentiment Analysis
GENERATE_FORM_API_URL = "http://127.0.0.1:5000/api/generateForm"  # Example API for generating a form
FEEDBACK_PATH = '../data/feedback.csv'

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

        return sentiment_result
    else:
        return "Not found"

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
# Function to write the header to the CSV file if it doesn't exist or is empty
def initialize_csv(file_path, headers):
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, mode="w", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

# Streamlit Layout
st.title("AI Model Interaction")

# Sidebar with sections for testing and generating form
st.sidebar.header("Navigation")
section = st.sidebar.radio("Select a section", ["Testing", "Generate Form", "Feedback Visualization", "Customer Queries", "Ask Query?"])

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
elif section == "Feedback Visualization":
    # Load the data and handle missing values
    try:
        mcq_data = pd.read_csv(FEEDBACK_PATH)
    except FileNotFoundError:
        st.error("Feedback data file not found.")
        mcq_data = pd.DataFrame()

    if not mcq_data.empty:
        # Fill NaN with empty strings for safe processing
        mcq_data.fillna("", inplace=True)

        # Display the raw data for context
        st.subheader("Feedback Data Overview")
        st.dataframe(mcq_data)

        # Collect sentiment data for the "Final Feedback" column
        sentiment_data = []
        for feedback in mcq_data["Final Feedback"]:
            if feedback:  # Ensure feedback is not empty
                sentiment_result = call_sentiment_analysis_api(feedback)
                sentiment_data.append(sentiment_result)
            else:
                sentiment_data.append("No sentiment found.")

        # Add sentiment data as a new column for visualization
        mcq_data["Sentiment"] = sentiment_data

        # Visualize response distribution for each MCQ question
        st.subheader("Feedback Response Distribution")
        questions_to_visualize = mcq_data.columns[:-2]  # Exclude "Final Feedback" and "Sentiment"
        
        for question in questions_to_visualize:
            st.write(f"**{question}**")
            response_counts = mcq_data[question].value_counts().sort_index()
            st.bar_chart(response_counts)

        # Visualization for sentiment analysis of feedback
        st.subheader("Sentiment Analysis of Final Feedback")
        sentiment_counts = pd.Series(sentiment_data).value_counts()
        st.bar_chart(sentiment_counts)

    else:
        st.warning("No data available for feedback visualization.")


elif section == "Customer Queries":
    # Path to the CSV file with customer queries
    data_path = '../data/queries.csv'

    try:
        # Load existing customer queries from the CSV file
        customer_queries = pd.read_csv(data_path)
        customer_queries = customer_queries[customer_queries['Answer'].isna()]
        if customer_queries.empty:
            st.warning("No customer queries found.")
        else:
            # Display the customer queries in a dropdown
            st.subheader("Customer Queries")
            query_index = st.selectbox(
                "Select a query",
                customer_queries.index,
                format_func=lambda idx: f"{customer_queries.at[idx, 'Category']} - {customer_queries.at[idx, 'Query']}"
            )

            # Display the summary and details of the selected query
            st.write("**Customer Query Summary:**")
            st.write(f"**Category:** {customer_queries.at[query_index, 'Category']}")
            st.write(f"**Query:** {customer_queries.at[query_index, 'Query']}")
            st.write(f"**Summary:** {customer_queries.at[query_index, 'Summary']}")
            st.write(f"**Answer:** {customer_queries.at[query_index, 'Answer']}")

            # Text area for adding or updating the answer
            answer = st.text_area(
                "Your Answer",
                value=customer_queries.at[query_index, 'Answer'] if pd.notna(customer_queries.at[query_index, 'Answer']) else ""
            )

            # Button to submit the answer
            if st.button("Submit Answer"):
                # Update the answer in the DataFrame
                customer_queries.at[query_index, 'Answer'] = answer

                # Save the updated DataFrame back to the CSV
                customer_queries.to_csv(data_path, index=False)
                st.success(f"Answer submitted and saved for query: {customer_queries.at[query_index, 'Query']}")

    except FileNotFoundError:
        st.error("No customer query data found.")

elif section == "Ask Query?":
    # Path to the CSV file
    query_path = '../data/queries.csv'
    headers = ["Query", "Category", "Summary", "Answer"]

    # Ensure the CSV file is initialized with headers
    initialize_csv(query_path, headers)

    # Input form to take user feedback
    customer_query = st.text_area("Enter Customer Feedback")

    if st.button("Submit Feedback"):
        if customer_query:
            # Call APIs for categorization and summarization
            category_result = call_classification_api(customer_query)
            summary_result = call_summarization_api(customer_query)
            answer = ""  # Placeholder for the answer field

            # Display results to the user
            st.write("**Category Identified:**", category_result)
            st.write("**Summary Generated:**", summary_result)

            # Save the feedback data to CSV
            with open(query_path, mode="a", newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([customer_query, category_result, summary_result, answer])
            st.success("Query has been submitted and saved successfully!")
        else:
            st.warning("Please provide both a form name and feedback text.")

    # Optional: Display existing feedback data for review (if available)
    if st.checkbox("Show Saved Feedback Data"):
        try:
            feedback_df = pd.read_csv(query_path)
            st.write(feedback_df)
        except FileNotFoundError:
            st.error("No feedback data found.")