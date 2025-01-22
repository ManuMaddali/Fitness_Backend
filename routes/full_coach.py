import os
import openai
from openai import OpenAIError
from dotenv import load_dotenv
from flask import Blueprint, request, Response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.database_utils import fetch_user_by_email
from utils.validation_utils import validate_fields
from utils.auth_utils import role_required
from models import db, UserInteractions, UserPreferences
import json
from collections import OrderedDict
from functools import lru_cache
import logging
from datetime import datetime
from langchain.prompts import PromptTemplate as LangChainPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage

# Initialize logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize memory for storing user interactions
memory = ConversationBufferMemory()

full_coach_bp = Blueprint('full_coach', __name__)

# Initialize LangChain LLM with gpt-3.5-turbo
langchain_llm = ChatOpenAI(
    model="gpt-4o-mini",  # Use a chat model
    temperature=0.6,
    max_tokens=500
)

# Define LangChain Prompt Templates
fitness_prompt = LangChainPromptTemplate(
    input_variables=["context", "query"],
    template="{context}\nGoal: {query}\nSteps:"
)

nutrition_prompt = LangChainPromptTemplate(
    input_variables=["context", "query"],
    template="{context}\nGoal: {query}\nMeal Plan:"
)

mental_health_prompt = LangChainPromptTemplate(
    input_variables=["context", "query"],
    template="{context}\nGoal: {query}\nMental health tips:"
)

# Create Direct Pipelines
fitness_chain = fitness_prompt | langchain_llm
nutrition_chain = nutrition_prompt | langchain_llm
mental_health_chain = mental_health_prompt | langchain_llm

class LLMWrapper:
    def __init__(self, api_key, model="gpt-4o-mini", temperature=0.6, max_tokens=500):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        openai.api_key = self.api_key

    @lru_cache(maxsize=100)
    def query(self, prompt, context=None):
        try:
            # Construct the messages array for the chat model
            messages = [
                {"role": "system", "content": "You are a helpful fitness coach."},
                {"role": "user", "content": prompt}
            ]
            if context:
                messages.insert(1, {"role": "system", "content": context})

            logging.debug(f"Sending ChatCompletion Messages: {messages}")

            # Use the correct chat/completions endpoint
            response = openai.ChatCompletion.create(
                model=self.model,  # Ensure this is a chat model like "gpt-4"
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            # Extract the response content
            result = response["choices"][0]["message"]["content"].strip()
            logging.debug(f"LLMWrapper Response: {result}")
            return result
        except openai.error.OpenAIError as e:
            logging.error(f"OpenAI API error: {e}")
            return "Sorry, there was an issue generating your advice. Please try again later."
        except Exception as e:
            logging.error(f"Unexpected error querying LLM: {e}")
            return "An unexpected error occurred. Please try again later."


llm = LLMWrapper(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ai_suggested_goals(stats, history):
    """
    Generate AI-suggested goals based on user stats and interaction history using GPT.

    Args:
        stats (dict): User stats, such as TDEE, BMI, etc.
        history (list): List of UserInteractions objects.

    Returns:
        dict: AI-suggested goals for fitness, nutrition, and mental health.
    """
    # Prepare context for AI
    history_context = ". ".join([f"Query: {interaction.query}. Goal: {interaction.FCgoal}. Response: {interaction.response}" 
                                 for interaction in history if interaction.FCgoal])
    stats_context = "\n".join([f"{key}: {value}" for key, value in stats.items()])

    ai_prompt = (
        f"User Stats:\n{stats_context}\n\n"
        f"History:\n{history_context}\n\n"
        "Based on the user's stats and interaction history, suggest dynamic, personalized goals for:\n"
        "- Fitness\n- Nutrition\n- Mental Health\n\n"
        "Provide the output as structured JSON with 'Fitness', 'Nutrition', and 'MentalHealth' as keys, "
        "each containing a list of 3 goals."
    )

    try:
        # Use GPT to generate AI-suggested goals
        response = llm.query(ai_prompt)
        FCgoals = json.loads(response)  # Parse the AI's response into JSON
        return FCgoals
    except Exception as e:
        logging.error(f"Error generating AI-suggested goals: {e}")
        return {
            "Fitness": ["Focus on general fitness."],
            "Nutrition": ["Eat a balanced diet."],
            "MentalHealth": ["Practice mindfulness and relaxation techniques."]
        }

@full_coach_bp.route('/api/full_coach', methods=['POST'])
@jwt_required()
@role_required(['premium', 'free'])
def full_coach():
    data = request.json
    logging.info(f"Received request data: {data}")

    # Validate inputs
    required_fields = ['weight', 'height_feet', 'height_inches', 'age', 'activity_factor', 'gender']
    validation_error = validate_fields(data, required_fields)
    if validation_error:
        return jsonify(validation_error[0]), validation_error[1]

    # Extract inputs and perform calculations
    weight_lbs = data['weight']
    height_feet = data['height_feet']
    height_inches = data['height_inches']
    age = data['age']
    activity_factor = data['activity_factor']
    gender = data['gender'].lower()

    weight_kg = weight_lbs / 2.20462
    height_cm = ((height_feet * 12) + height_inches) * 2.54
    height_m = height_cm / 100
    tdee = ((10 * weight_kg) + (6.25 * height_cm) - (5 * age) + (5 if gender == 'male' else -161)) * activity_factor
    bmi = weight_kg / (height_m ** 2)
    bfp = 1.20 * bmi + 0.23 * age - (16.2 if gender == 'male' else -5.4)
    bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + (5 if gender == 'male' else -161)
    ibw_kg = (50 + 2.3 * (((height_feet * 12) + height_inches) - 60)) if gender == 'male' else (
        45.5 + 2.3 * (((height_feet * 12) + height_inches) - 60))
    ibw_lbs = ibw_kg * 2.20462
    hydration_liters = weight_kg * 0.033
    hydration_cups = hydration_liters * 4.22675

    # User-friendly stats in American units
    formatted_stats = {
        "Total Daily Energy Expenditure (TDEE)": f"{round(tdee)} calories/day",
        "Body Mass Index (BMI)": f"{round(bmi, 2)} kg/m²",
        "Body Fat Percentage (BFP)": f"{round(bfp, 2)}%",
        "Basal Metabolic Rate (BMR)": f"{round(bmr)} calories/day",
        "Ideal Body Weight (IBW)": f"{round(ibw_lbs, 1)} lbs",
        "Hydration Needs": f"{round(hydration_cups, 1)} cups/day"
    }

    # Fetch user preferences from the database
    email = get_jwt_identity()
    user, error_response = fetch_user_by_email(email)
    if error_response:
        return jsonify(error_response), 404

    user_role = user.role  # Free or premium user
    user_preferences = db.session.query(UserPreferences).filter_by(user_id=user.id).first()
    preferences_context = user_preferences.preferences if user_preferences else "No specific preferences."

    # Fetch user history
    past_interactions = db.session.query(UserInteractions).filter_by(user_id=user.id).order_by(
        UserInteractions.timestamp.desc()).limit(5).all()

    # Filter relevant past queries to avoid unrelated context
    relevant_interactions = [
        interaction for interaction in past_interactions
        if interaction.query_type == data.get("query_type", "general") or not interaction.query_type
    ]
    past_context = '. '.join(
        [f"Query: {interaction.query}. Response: {interaction.response}" for interaction in relevant_interactions]
    )

    # Suggest goals dynamically based on stats and history
    selected_goal = data.get("FCgoal", "General fitness advice")
    suggested_goals = generate_ai_suggested_goals(formatted_stats, past_interactions)

    


    # Add advanced context for AI
    context = (
        f"My stats are: TDEE {round(tdee)} calories/day, BMI {round(bmi, 2)} kg/m², BFP {round(bfp, 2)}%, "
        f"IBW {round(ibw_lbs, 1)} lbs, hydration needs {round(hydration_cups, 1)} cups/day. "
        f"Preferences: {preferences_context}. "
        f"Recent relevant queries: {past_context}. "
        f"Current goal: {selected_goal}."
    )

    memory.chat_memory.add_message(HumanMessage(content=f"Provide advice based on these stats: {context}"))
    memory.chat_memory.add_message(AIMessage(content="Working on your personalized advice now!"))

    try:
        # Refined prompts with predefined formats
        fitness_prompt = (
            f"{context}\n"
            f"Provide detailed fitness advice, including:\n"
            f"- Exercise types (compound vs isolation).\n"
            f"- Weekly workout schedule.\n"
            f"- Rest and recovery tips.\n"
            f"- Metrics to track progress."
        )
        nutrition_prompt = (
            f"{context}\n"
            f"Provide a detailed meal plan formatted as:\n"
            f"- Breakfast:\n- Snack:\n- Lunch:\n- Snack:\n- Dinner:\n- Pre-bed Snack:\n\n"
            f"Include portion sizes for someone with a caloric need of {round(tdee)} calories."
        )
        mental_health_prompt = (
            f"{context}\n"
            f"Provide mental health strategies, including:\n"
            f"- Stress reduction techniques.\n"
            f"- Motivation strategies.\n"
            f"- Goal-setting advice.\n"
            f"- How to build a support system."
        )

        # LangChain pipelines for advice
        fitness_response = fitness_chain.invoke({"context": context, "query": fitness_prompt})
        nutrition_response = nutrition_chain.invoke({"context": context, "query": nutrition_prompt})
        mental_health_response = mental_health_chain.invoke({"context": context, "query": mental_health_prompt})

        # Parse LangChain responses into structured lists
        fitness_advice = fitness_response.content.split("\n") if hasattr(fitness_response, 'content') else str(fitness_response).split("\n")
        nutrition_advice = nutrition_response.content.split("\n") if hasattr(nutrition_response, 'content') else str(nutrition_response).split("\n")
        mental_health_advice = mental_health_response.content.split("\n") if hasattr(mental_health_response, 'content') else str(mental_health_response).split("\n")

    except Exception as e:
        logging.error(f"LangChain failed: {e}")

        # Fallback to LLMWrapper if LangChain fails
        fitness_advice = llm.query(fitness_prompt).split("\n")
        nutrition_advice = llm.query(nutrition_prompt).split("\n")
        mental_health_advice = llm.query(mental_health_prompt).split("\n")

    # Structured advice output
    advice = {
        "Fitness": {"title": "Fitness Tips", "content": fitness_advice},
        "Nutrition": {"title": "Sample Meal Plan", "content": nutrition_advice},
        "MentalHealth": {"title": "Mental Health Strategies", "content": mental_health_advice}
    }

    # Save interaction with feedback collection
    feedback = data.get("feedback", None)
    new_interaction = UserInteractions(
        user_id=user.id,
        query=data.get("query", "Fitness, Nutrition, and Mental Health Advice"),
        response=json.dumps(advice),
        query_type=data.get("query_type", "general"),  # " if not provided
        FCgoal=selected_goal,
        timestamp=datetime.utcnow()
    )
    db.session.add(new_interaction)
    if feedback:
        logging.info(f"User feedback received: {feedback}")
        new_interaction.feedback = feedback
    db.session.commit()

    # Final response
    response_data = {
        "user_role": user_role,
        "stats": formatted_stats,
        "advice": advice,
        "suggested_goals": suggested_goals
    }

    logging.info(f"Response Data: {response_data}")

    return Response(
        json.dumps(response_data, indent=4),
        mimetype='application/json',
        status=200
    )
