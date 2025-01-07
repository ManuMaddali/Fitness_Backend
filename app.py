import os
import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask app
app = Flask(__name__)

# Home route
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Fitnes Backend!"})

# AI coach route
@app.route('/api/coach', methods=['POST'])
def ai_coach():
    data = request.json
    user_query = data['query']

    # Use ChatCompletion instead of Completion
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Specify the model
        messages=[
            {"role": "system", "content": "You are a helpful fitness and nutrition assistant."},
            {"role": "user", "content": user_query}
        ],
        max_tokens=150
    )
    return jsonify({"response": response['choices'][0]['message']['content'].strip()})

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