import os
import logging
import openai
from openai.error import OpenAIError
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configure logging globally
logging.basicConfig(level=logging.INFO)

# Initialize Flask app
app = Flask(__name__)

# Home route
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Fitness Backend!"})

# AI coach route
@app.route('/api/coach', methods=['POST'])
def ai_coach():
    # Ensure the request body is JSON
    if not request.is_json:
        return jsonify({"error": "Request body must be in JSON format."}), 400

    data = request.json

    # Check if the query field exists and is not empty
    if 'query' not in data or not data['query'].strip():
        return jsonify({"error": "The 'query' field is required and cannot be empty."}), 400

    # Validate query length
    if len(data['query']) > 500:
        return jsonify({"error": "The 'query' field exceeds the maximum allowed length of 500 characters."}), 400

    # Query context validation (check for fitness-related keywords)
    fitness_keywords = {"workout", "exercise", "diet", "nutrition", "gain muscle", "lose weight", 
                        "fitness", "calories", "macros", "workout plan", "meal plan", 
                        "water intake", "protein", "carbs", "fats"}
    user_query = data['query']
    if not any(keyword in user_query.lower() for keyword in fitness_keywords):
        return jsonify({"error": "The query does not seem related to fitness or nutrition. Please ask relevant questions."}), 400
    
    try:
        # Log the incoming query
        logging.info(f"Received query: {user_query}")

        # Adjust token usage dynamically based on query complexity
        max_tokens = 75 if len(user_query) < 50 else 150

        # OpenAI API Call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful fitness and nutrition assistant. Always provide short and concise answers."},
                {"role": "user", "content": user_query}
            ],
            max_tokens=max_tokens
        )

        # Log the response from OpenAI
        logging.info(f"OpenAI response: {response}")

        # Return the AI-generated response
        return jsonify({"response": response['choices'][0]['message']['content'].strip()})

    except OpenAIError as e:
    # Handle OpenAI-related errors (e.g., rate limits, invalid requests)
        logging.error(f"OpenAI error: {str(e)}")
        return jsonify({"error": f"OpenAI error: {str(e)}"}), 500
    except Exception as e:
    # Handle all other unexpected errors
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

# TDEE calculation route
@app.route('/api/tdee', methods=['POST'])
def calculate_tdee():
    if not request.is_json:
        return jsonify({"error": "Request body must be in JSON format."}), 400

    data = request.json
    try:
        weight = float(data['weight'])
        height = float(data['height'])
        age = int(data['age'])
        activity_factor = float(data['activity_factor'])

        if not (20 <= weight <= 300):
            return jsonify({"error": "Weight must be between 20 and 300 kg."}), 400
        if not (50 <= height <= 250):
            return jsonify({"error": "Height must be between 50 and 250 cm."}), 400
        if not (1 <= age <= 120):
            return jsonify({"error": "Age must be between 1 and 120 years."}), 400
        if not (1.2 <= activity_factor <= 2.5):
            return jsonify({"error": "Activity factor must be between 1.2 and 2.5."}), 400

        # Calculate TDEE
        tdee = (10 * weight) + (6.25 * height) - (5 * age) + 5
        tdee *= activity_factor

        return jsonify({"tdee": round(tdee)})

    except (KeyError, ValueError):
        return jsonify({"error": "Invalid or missing input fields. Ensure weight, height, age, and activity_factor are provided and valid."}), 400

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)
