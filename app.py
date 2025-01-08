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
    return jsonify({"message": "Welcome to the Fitness Backend!"})

# AI coach route
@app.route('/api/coach', methods=['POST'])
def ai_coach():
    data = request.json
    user_query = data['query']

    # OpenAI API call
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful fitness and nutrition assistant."},
            {"role": "user", "content": user_query}
        ],
        max_tokens=300
    )

    return jsonify({"response": response['choices'][0]['message']['content'].strip()})

# TDEE calculation route
@app.route('/api/tdee', methods=['POST'])
def calculate_tdee():
    data = request.json
    weight = data['weight']  # in kg
    height = data['height']  # in cm
    age = data['age']        # in years
    activity_factor = data['activity_factor']  # multiplier for activity level

    # Calculate TDEE using Mifflin-St Jeor equation
    tdee = (10 * weight) + (6.25 * height) - (5 * age) + 5
    tdee *= activity_factor

    return jsonify({"tdee": round(tdee)})

# Full coach route
@app.route('/api/full_coach', methods=['POST'])
def full_coach():
    data = request.json

    # Extract inputs
    weight_lbs = data.get('weight')  # in lbs
    height_feet = data.get('height_feet')  # in feet
    height_inches = data.get('height_inches')  # in inches
    age = data.get('age')  # in years
    activity_factor = data.get('activity_factor')  # multiplier for activity level
    gender = data.get('gender', '').lower()  # 'male' or 'female'

    if not all([weight_lbs, height_feet, height_inches, age, activity_factor, gender]):
        return jsonify({"error": "Missing required fields: weight, height_feet, height_inches, age, activity_factor, or gender"}), 400

    # Convert weight from lbs to kg
    weight_kg = weight_lbs / 2.20462

    # Convert height from feet and inches to cm
    height_cm = ((height_feet * 12) + height_inches) * 2.54

    # Calculate TDEE
    tdee = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + (5 if gender == 'male' else -161)
    tdee *= activity_factor

    # Calculate BMI
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)

    # Calculate BFP
    bfp = 1.20 * bmi + 0.23 * age - (16.2 if gender == 'male' else 5.4)

    # Calculate BMR
    bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + (5 if gender == 'male' else -161)

    # Calculate Ideal Body Weight (IBW)
    height_total_inches = (height_feet * 12) + height_inches
    ibw = (50 + 2.3 * (height_total_inches - 60)) if gender == 'male' else (45.5 + 2.3 * (height_total_inches - 60))

    # Calculate Hydration Needs
    hydration = weight_kg * 0.033

    # Generate AI advice
    user_query = data.get('query', '')
    combined_query = (
        f"My TDEE is {round(tdee)} calories per day, my BMI is {round(bmi, 2)}, "
        f"my body fat percentage is {round(bfp, 2)}%, and my ideal body weight is {round(ibw, 1)} kg. "
        f"Additionally, I need {round(hydration, 2)} liters of water daily. {user_query}"
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a fitness coach. Provide advice based on the user's TDEE, BMI, BFP, IBW, and hydration needs."},
            {"role": "user", "content": combined_query}
        ],
        max_tokens=300
    )

    return jsonify({
        "tdee": round(tdee),
        "bmi": round(bmi, 2),
        "bfp": round(bfp, 2),
        "bmr": round(bmr),
        "ibw": round(ibw, 1),
        "hydration": round(hydration, 2),
        "advice": response['choices'][0]['message']['content'].strip()
    })

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
