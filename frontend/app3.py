import streamlit as st
import pandas as pd
import numpy as np

st.title('My first app')
# Navigation for sections
section = st.sidebar.radio("Select Section", ["MCQ Visualization & Sentiment", "Customer Queries"])

if section == "MCQ Visualization & Sentiment":
    # Add the visualization code here
    # Sample MCQ data (replace with actual data fetching from CSV or DB)
    mcq_data = {
        'Question 1': ['Option A', 'Option B', 'Option A', 'Option C', 'Option B'],
        'Question 2': ['Option 1', 'Option 2', 'Option 1', 'Option 1', 'Option 2']
    }

    # Sample sentiment data (replace with actual sentiment results from your feedback)
    sentiment_data = ['positive', 'negative', 'neutral', 'positive', 'positive']

    st.subheader("MCQ Responses and Feedback Sentiment")

    # MCQ visualization and sentiment analysis code here
    # Visualization for MCQ responses
    st.subheader("MCQ Responses Visualization")
    for question, responses in mcq_data.items():
        st.write(f"**{question}:**")
        response_counts = pd.Series(responses).value_counts()
        st.bar_chart(response_counts)

    # Visualization for sentiment analysis of feedback
    st.subheader("Sentiment Analysis of Customer Feedback")
    sentiment_counts = pd.Series(sentiment_data).value_counts()
    st.bar_chart(sentiment_counts)

elif section == "Customer Queries":
    # Add the customer query section here
    # Sample customer queries data (replace with actual data fetching)
    customer_queries = [
        {"category": "Product Inquiry", "query": "What is the return policy?", "answer": "Our return policy allows returns within 30 days."},
        {"category": "Technical Support", "query": "How to reset my password?", "answer": "Please click on 'Forgot Password' to reset."},
        {"category": "Order Status", "query": "When will my order arrive?", "answer": "Your order will arrive within 5-7 business days."}
    ]

    # Section for displaying customer queries
    st.subheader("Customer Queries")
    query_dropdown = st.selectbox("Select a query", customer_queries, format_func=lambda x: f"{x['category']} - {x['query']}")

    # Show summary of the selected query
    st.write("**Customer Query Summary:**")
    st.write(f"**Category:** {query_dropdown['category']}")
    st.write(f"**Query:** {query_dropdown['query']}")
    st.subheader("Customer Query Management")
    # Customer queries display and answer code here
    # Text area for answering the query
    answer = st.text_area("Your Answer", value=query_dropdown['answer'])

    # Button to submit the answer
    if st.button("Submit Answer"):
        st.success(f"Answer submitted for query: {query_dropdown['query']}")
        # You can save the updated answer to a database or perform any other action here
