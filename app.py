import os
import logging
from openai import OpenAI
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Flask app
app = Flask(__name__)

# Home route
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Fitnes Backend!"})

# AI coach route
@app.route('/api/coach', methods=['POST'])
def ai_coach():
    # Debug Logging
    import logging
    logging.basicConfig(level=logging.INFO)

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
    def validate_query(query):
        fitness_keywords = ["workout", "exercise", "diet", "nutrition", "gain muscle", "lose weight", "fitness", "calories", "macros", "workout plan", "meal plan", "water intake", "protein", "carbs", "fats"]
        return any(keyword in query.lower() for keyword in fitness_keywords)

    user_query = data['query']

    if not validate_query(user_query):
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

    except openai.error.RateLimitError:
        # Handle rate limit errors
        return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429
    except openai.error.InvalidRequestError as e:
        # Handle invalid OpenAI requests
        logging.error(f"Invalid OpenAI request: {str(e)}")
        return jsonify({"error": f"Invalid request: {str(e)}"}), 400
    except openai.error.OpenAIError as e:
        # Handle generic OpenAI API errors
        logging.error(f"OpenAI API error: {str(e)}")
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500
    except Exception as e:
        # Handle all other unexpected errors
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500


# TDEE calculation route
@app.route('/api/tdee', methods=['POST'])
def calculate_tdee():
    data = request.json
    weight = data['weight']
    height = data['height']
    age = data['age']
    activity_factor = data['activity_factor']

    # Calculate TDEE using the Mifflin-St Jeor equation
    tdee = (10 * weight) + (6.25 * height) - (5 * age) + 5
    tdee *= activity_factor

    return jsonify({"tdee": round(tdee)})

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)