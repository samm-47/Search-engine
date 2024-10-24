import os
from flask import Flask, request, jsonify
import google.generativeai as genai  # Ensure you have the Google Gemini SDK installed

app = Flask(__name__)

# Retrieve the API key from environment variables
API_KEY = os.environ.get("GENAI_API_KEY")
if not API_KEY:
    raise ValueError("The API key for Google Gemini is not set.")

# Configure the Generative AI model
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Sample glossary data (in practice, this should come from a database)
glossary = {
    "API": "A set of functions and protocols for building software applications.",
    "Cloud Computing": "Delivery of computing services over the internet.",
    "Machine Learning": "The study of computer algorithms that improve automatically through experience."
}

# Function to fetch suggestions from Google Gemini API
def get_suggestions_from_gemini(query):
    # Send the query to the Gemini model for processing
    try:
        # Assuming we need to use 'genai.chat' for chat-like interactions
        response = model.chat(input_text=query)  # Use the correct method for calling the API
        
        # Print the entire response for debugging
        print("Response from Gemini:", response)

        # Extract the relevant content from the response
        # The response structure may vary; you might need to adjust this based on the actual response format
        suggestions = [message.text for message in response.messages if hasattr(message, 'text')]
        
        print("Extracted suggestions:", suggestions)
        return suggestions

    except Exception as e:
        print(f"Error with Google Gemini API: {e}")
        return []

# Route for the chatbot query
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_query = request.get_json().get('query')  # Expecting user query as {"query": "your question"}

    if not user_query:
        return jsonify({"message": "No query provided."}), 400  # Return error if no query is found

    # Step 1: Get AI-powered suggestions from Google Gemini
    suggestions = get_suggestions_from_gemini(user_query)
    
    # Step 2: Fetch relevant glossary terms based on the suggestions
    matching_terms = []
    for suggestion in suggestions:
        if suggestion in glossary:
            matching_terms.append({
                "term": suggestion,
                "definition": glossary[suggestion]
            })
    
    # Step 3: If multiple matches, ask user to select one
    if len(matching_terms) > 1:
        return jsonify({
            "message": "Did you mean one of the following terms?",
            "options": [term["term"] for term in matching_terms]
        })
    
    # Step 4: If only one match, return the definition
    elif len(matching_terms) == 1:
        return jsonify({
            "term": matching_terms[0]["term"],
            "definition": matching_terms[0]["definition"]
        })
    
    # Step 5: If no matches found, inform the user
    else:
        return jsonify({
            "message": "Sorry, no matching terms found in the glossary."
        })

# Route for handling user selection from chatbot options
@app.route('/select', methods=['POST'])
def select():
    selected_term = request.json.get('term')
    
    # Return the definition of the selected term
    if selected_term in glossary:
        return jsonify({
            "term": selected_term,
            "definition": glossary[selected_term]
        })
    else:
        return jsonify({
            "message": "Sorry, term not found."
        })

if __name__ == '__main__':
    app.run(debug=True)
