import gradio as gr
import requests
import os

# Replace with your environment variable handling if needed
GROQ_KEY = "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"

# API URLs for different tasks
FAQ_API_URL = "http://127.0.0.1:5000/faq"  # Example API for FAQ Bot
CLASSIFICATION_API_URL = "http://127.0.0.1:5000/classify"  # Example API for Text Classification
SUMMARIZATION_API_URL = "http://127.0.0.1:5000/summarize"  # Example API for Text Summarization
SENTIMENT_ANALYSIS_API_URL = "http://127.0.0.1:5000/sentiment"  # Example API for Sentiment Analysis
GENERATE_FORM_API_URL = "http://127.0.0.1:5000/api/generateForm"  # Example API for Form Generation

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
    if response.status_code == 200:
        unique_url = response.json().get("url", "")
        return unique_url
    else:
        return "Error generating form."

# Function to generate a new form
def generate_new_form():
    return generate_form()

# Gradio interface function
def gradio_interface(task, text_input):
    if task == "FAQ Bot":
        return call_faq_api(text_input)
    elif task == "Text Classification":
        return call_classification_api(text_input)
    elif task == "Text Summarization":
        return call_summarization_api(text_input)
    elif task == "Sentiment Analysis":
        return call_sentiment_analysis_api(text_input)

# Create Gradio interface with Blocks layout
with gr.Blocks() as demo:
    with gr.Row():
        # Sidebar on the left
        with gr.Column(scale=1, min_width=200):
            gr.Markdown("## Sidebar")
            
            # Create an Accordion for collapsible sections
            with gr.Accordion("Testing", open=True):
                gr.Markdown("### Model Testing")
                task_dropdown = gr.Dropdown(
                    choices=["FAQ Bot", "Text Classification", "Text Summarization", "Sentiment Analysis"],
                    label="Select Task"
                )
                input_text = gr.Textbox(lines=2, placeholder="Enter your query/text here", label="Input Text")
                output = gr.Textbox(label="Output")

                # Connect tasks to the model functions
                task_dropdown.change(gradio_interface, [task_dropdown, input_text], output)

            with gr.Accordion("Generate Form", open=False):
                gr.Markdown("### Form Generation")
                generate_button = gr.Button("Generate Form")
                form_url = gr.Textbox(label="Generated Form URL", interactive=False)
                generate_button.click(generate_form, inputs=[], outputs=form_url)

                generate_new_button = gr.Button("Generate New URL")
                generate_new_button.click(generate_new_form, inputs=[], outputs=form_url)

        # Main Content Section (to the right of the sidebar)
        with gr.Column(scale=3):
            gr.Markdown("### Main Content")
            gr.Markdown("Test your model here or generate a form link.")

    # Launch the interface
    demo.launch(debug=True)