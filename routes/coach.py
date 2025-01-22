from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.database_utils import fetch_user_by_email
from models import db, UserInteractions, UserStats
from utils.auth_utils import role_required
from openai import OpenAIError
import openai
from datetime import datetime

coach_bp = Blueprint('coach', __name__)

@coach_bp.route('/api/coach', methods=['POST'])
@jwt_required()
@role_required(['free', 'premium'])  # Free and premium users can access this endpoint
def ai_coach():
    """
    Chatbot endpoint providing fitness, nutrition, and mental health advice.
    Includes:
    - Fitness stats for personalization.
    - Behavior-based responses using past queries.
    - Query categorization for tailored advice.
    - Follow-up questions for interactivity.
    - Goal tracking and follow-ups.
    """
    data = request.json
    user_query = data.get('query', '').strip()

    if not user_query or len(user_query) < 3:
        return jsonify({"error": "The query must be at least 3 characters long."}), 400

    # Fetch user info
    email = get_jwt_identity()
    user, error_response = fetch_user_by_email(email)
    if error_response:
        return jsonify(error_response), 404

    try:
        # Fetch the most recent user stats
        latest_stats = UserStats.query.filter(
            UserStats.user_id == user.id
        ).order_by(UserStats.timestamp.desc()).first()
    except Exception as e:
        latest_stats = None

    try:
        # Fetch all user goals from past interactions
        user_goals = UserInteractions.query.filter(
            UserInteractions.user_id == user.id,
            UserInteractions.goal == True
        ).all()
    except Exception as e:
        user_goals = []

    try:
        # Fetch the user's last interaction
        past_interaction = UserInteractions.query.filter(
            UserInteractions.user_id == user.id
        ).order_by(UserInteractions.timestamp.desc()).first()
    except Exception as e:
        past_interaction = None

    # Personalization and follow-up logic
    personalization = (
        f"Your stats: TDEE is {round(latest_stats.tdee)} calories/day, "
        f"BMI is {round(latest_stats.bmi, 2)}, body fat percentage is {round(latest_stats.bfp, 2)}%, "
        f"and daily hydration need is {round(latest_stats.hydration, 2)} liters."
        if latest_stats else
        "I don't have your fitness stats yet. Tracking your stats can help provide personalized advice!"
    )

    follow_up = (
        f"I see your goal is: '{user_goals[-1].query}'. How has your progress been so far? "
        f"Would you like to adjust or refine your goal?"
        if user_goals else
        f"Previously, you asked: '{past_interaction.query}'. Is there anything specific you'd like to build on?"
        if past_interaction else
        "Would you like to set a goal, such as building muscle, losing fat, or improving endurance?"
    )

    query_category = categorize_query(user_query)
    system_prompt = generate_prompt(query_category)
    combined_query = f"{personalization}\n{follow_up}\nUser Query: {user_query}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": combined_query}
            ],
            max_tokens=400
        )

        ai_response = response['choices'][0]['message']['content'].strip()
        if not latest_stats:
            ai_response += ("\n\n🚀 **Would you like to start tracking your stats to receive more personalized insights?**")

        # Structure response for clarity
        formatted_response = (
            "To effectively achieve your goals, focus on a well-rounded strategy that integrates fitness, nutrition, and mental health. "
            "Here’s how to work towards your goals:\n\n"
            "🏋️ Fitness\n"
            "Add Regular Aerobic Exercise:\n"
            "- **What to do:** Walk, run, cycle, swim, or take an aerobics class.\n"
            "- **How often:** Aim for 150 minutes of moderate-intensity or 75 minutes of vigorous-intensity aerobic activity weekly.\n"
            "- **Why it works:** Aerobic exercises burn calories and improve cardiovascular health.\n\n"
            "Incorporate Strength Training:\n"
            "- **What to do:** Lift weights, do bodyweight exercises (like squats or push-ups), or try resistance bands.\n"
            "- **How often:** 2–3 times per week to build muscle and boost your metabolism.\n"
            "- **Pro tip:** Use progressive overload (gradually increasing weight or reps) to ensure steady progress.\n\n"
            "Try High-Intensity Interval Training (HIIT):\n"
            "- **What it is:** Alternate between short bursts of intense effort and periods of rest.\n"
            "- **How often:** 1–2 sessions per week, 20 minutes each.\n"
            "- **Why it works:** HIIT burns calories faster and continues burning even after your workout ends.\n\n"
            "🥗 Nutrition\n"
            "Create a Calorie Deficit:\n"
            "- **How:** Track your intake with apps like MyFitnessPal or Cronometer.\n"
            "- **Tip:** Aim for a 500-750 calorie deficit daily for sustainable fat loss.\n\n"
            "Focus on a Balanced Diet:\n"
            "- **What to eat:** Lean proteins (chicken, tofu), complex carbs (brown rice, quinoa), and healthy fats (avocado, nuts).\n"
            "- **How:** Use the 80/20 rule—80% nutrient-dense foods, 20% indulgences.\n\n"
            "Boost Fiber Intake:\n"
            "- **Examples:** Add oatmeal, berries, spinach, and lentils to your meals.\n"
            "- **Benefit:** Fiber keeps you full longer and improves digestion.\n\n"
            "Stay Hydrated:\n"
            "- **Goal:** Drink at least 2–3 liters of water daily (adjust based on weight/activity).\n"
            "- **Hack:** Carry a water bottle to remind yourself to sip throughout the day.\n\n"
            "🧠 Mental Health\n"
            "Practice Mindful Eating:\n"
            "- **How:** Eat slowly, savor each bite, and avoid distractions like screens during meals.\n"
            "- **Why it helps:** Mindful eating prevents overeating and fosters a healthier relationship with food.\n\n"
            "Set Realistic Goals:\n"
            "- **Example:** 'I’ll walk 30 minutes a day, 5 days a week.'\n"
            "- **Tip:** Celebrate small wins—every step counts!\n\n"
            "Manage Stress:\n"
            "- **Try:** Meditation, yoga, or journaling to reduce stress that can lead to emotional eating.\n"
            "- **Pro tip:** Take 5 minutes daily for deep breathing.\n\n"
            "🚀 Ready to take your fitness journey to the next level? Start tracking your stats for personalized advice and progress updates. You’ve got this—small, consistent changes lead to big results! 💪"
        )

        ai_response = formatted_response

        new_interaction = UserInteractions(
            user_id=user.id,
            query=user_query,
            response=ai_response,
            timestamp=datetime.utcnow(),
            goal=is_goal_query(user_query)
        )
        db.session.add(new_interaction)
        db.session.commit()

        return jsonify({"message": ai_response}), 200

    except OpenAIError as e:
        return jsonify({"error": f"AI response failed: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500


def is_goal_query(user_query):
    goal_keywords = [
        "goal", "lose weight", "build muscle", "gain strength", "improve endurance", "fat loss", 
        "objective", "aim", "ambition", "target", "milestone", "aspiration", "resolution", "dream", 
        "achievement", "task", "desire", "intention", "endgame", "success", "plan", "mission", 
        "outcome", "commitment", "dedication", "focus", "productivity", "progression", 
        "self-improvement", "personal growth", "accomplishment"
    ]
    return any(keyword in user_query.lower() for keyword in goal_keywords)


def categorize_query(user_query):
    fitness_keywords = [
        "workout", "exercise", "gym", "training", "strength", "weights", "cardio", "HIIT", "build muscle",
        "gain strength", "gain muscle", "calisthenics", "muscle growth", "bodybuilding", "fat burning"
    ]
    nutrition_keywords = [
        "diet", "meal", "nutrition", "calories", "protein", "carbs", "fats", "calorie deficit", "calorie surplus",
        "healthy eating", "meal plan", "meal prep", "balanced diet"
    ]
    mental_health_keywords = [
        "stress", "anxiety", "focus", "meditation", "mindfulness", "self-care", "mental health"
    ]

    categories = []

    if any(keyword in user_query.lower() for keyword in fitness_keywords):
        categories.append("fitness")
    if any(keyword in user_query.lower() for keyword in nutrition_keywords):
        categories.append("nutrition")
    if any(keyword in user_query.lower() for keyword in mental_health_keywords):
        categories.append("mental_health")

    return categories if categories else ["general"]


def generate_prompt(categories):
    prompts = []

    if "fitness" in categories:
        prompts.append(
            "You are a fitness coach. Provide advice about workouts, strength training, and building muscle, "
            "including strategies for combining fat loss with muscle gain."
        )
    if "nutrition" in categories:
        prompts.append(
            "You are a nutrition coach. Provide advice on meal planning, calorie management, and protein-rich diets "
            "that support both fat loss and muscle growth."
        )
    if "mental_health" in categories:
        prompts.append(
            "You are a mental health coach. Provide strategies for reducing stress, maintaining focus, and staying "
            "motivated during fitness and nutrition journeys."
        )

    return " ".join(prompts)

