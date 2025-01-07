from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Fitness Backend!"})

if __name__ == '__main__':
    app.run(debug=True)

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

