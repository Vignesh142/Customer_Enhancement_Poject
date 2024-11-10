# app.py
from flask import Flask, request, jsonify, render_template
import os
import json
import csv
import uuid
from bot import answer_customer_query, classify_and_log_query, summarize_and_log_query, sentiment_analysis


app = Flask(__name__)

@app.route("/faq", methods=["POST"])
def query():
    try:
        # Get the customer query from the request
        data = request.json
        query = data.get("query")
        api_key = data.get("groq_api_key")
        
        if not query:
            return jsonify({"error": "Query is required."}), 400
        
        # Get the response from the FAQ bot
        response = answer_customer_query(query, api_key=api_key)
        return jsonify({"response": response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/classify", methods=["POST"])
def classify():
    try:
        # Get the customer query from the request
        data = request.json
        query = data.get("query")
        api_key = data.get("groq_api_key")
        
        if not query:
            return jsonify({"error": "Query is required."}), 400
        
        if not api_key:
            return jsonify({"error": "API key is required for classification."}), 400
        
        # Classify the query and save it to the log file
        category = classify_and_log_query(query, api_key)

        return jsonify({"category": category})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        # Get the customer query from the request
        data = request.json
        query = data.get("query")
        api_key = data.get("groq_api_key")
        
        if not query:
            return jsonify({"error": "Query is required."}), 400
        
        if not api_key:
            return jsonify({"error": "API key is required for summarization."}), 400
        
        # Summarize the query and save it to the log file
        summary = summarize_and_log_query(query, api_key)

        return jsonify({"query": query, "summary": summary})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/sentiment", methods=["POST"])
def sentiment():
    try:
        # Get the text input from the request
        data = request.json
        text = data.get("query")
        api_key = data.get("groq_api_key")
        
        if not text:
            return jsonify({"error": "Text is required."}), 400
        if not api_key:
            return jsonify({"error": "API key is required for sentiment analysis."}), 400
        
        sentiment_result = sentiment_analysis(text, api_key)
        
        return jsonify({"sentiment": sentiment_result})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Quiz Page Code
PORT = 5000
form_data_store = {}

@app.route('/api/generateForm', methods=['POST'])
def generate_form():
    try:
        form_id = str(uuid.uuid4())  # Generate a unique form ID
        form_data_store[form_id] = {
            'responses': [],
            'completed': False 
        }

        unique_url = f'http://127.0.0.1:{PORT}/form/{form_id}'
        print(f'Generated form URL: {unique_url}')
        print(form_data_store)
        return jsonify({'url': unique_url})
    except Exception as e:
        return jsonify({'error': 'Unable to generate form', 'err': str(e)}), 500

@app.route('/api/questions', methods=['GET'])
def get_questions():
    questions_path = os.path.join('data', 'questions.json')
    try:
        with open(questions_path, 'r', encoding='utf-8') as file:
            questions = json.load(file)
            return jsonify(questions)
    except Exception as e:
        print(f'Error reading questions file: {e}')
        return jsonify({'error': 'Unable to load questions'}), 500

@app.route('/api/feedback', methods=['POST'])
def save_feedback():
    data = request.get_json()
    responses = data.get('responses', [])
    final_feedback = data.get('finalFeedback', '')

    # Prepare data to be saved
    feedback_data = [{'question': f'Question {i + 1}', 'answer': response} for i, response in enumerate(responses)]
    feedback_data.append({'question': 'Final Feedback', 'answer': final_feedback})

    # Define the path to the CSV file
    file_path = os.path.join('data', 'feedback.csv')

    # Check if the CSV file exists, create headers if it doesn't
    file_exists = os.path.isfile(file_path)

    try:
        with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

            # Write header if file doesn't exist
            if not file_exists:
                headers = [item['question'] for item in feedback_data]
                writer.writerow(headers)

            # Write the data row (flattened answers)
            data_row = [item['answer'] for item in feedback_data]
            writer.writerow(data_row)
            form_data_store[data.get('formId')]['completed'] = True

        return jsonify({'message': 'Feedback submitted successfully!'})
    except Exception as e:
        print(f'Error writing to CSV: {e}')
        return jsonify({'error': 'Unable to save feedback'}), 500

@app.route('/form/<form_id>')
def serve_form(form_id):
    print(form_data_store)
    if form_id in form_data_store:
        print(f'Serving form with ID: {form_id}')
        if not form_data_store[form_id]['completed']:
            return render_template('index.html')
        else:
            return render_template('form_submitted.html')
    else:
        return jsonify({'error': 'Invalid form ID'}), 404

@app.route('/')
def home():
    return "Hello!!, Welcome to the Customer Support Chatbot API"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
