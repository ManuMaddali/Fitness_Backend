from app import create_app
from models import db, PromptTemplate

app = create_app()

with app.app_context():
    def seed_prompt_templates():
        templates = [
            {"category": "general", "template": "Provide a detailed response including:\n1. A motivational introduction.\n2. Specific tips based on my stats.\n3. Additional advice to achieve my goals.", "description": "General advice"},
            {"category": "hydration", "template": "Focus on hydration. Provide actionable tips to improve water intake based on stats.", "description": "Hydration advice"},
            {"category": "nutrition", "template": "Focus on nutrition. Provide personalized meal plans based on stats.", "description": "Nutrition advice"},
            {"category": "fitness", "template": "Provide fitness routines and strength training plans based on stats.", "description": "Fitness advice"},
        ]

        for template in templates:
            existing = PromptTemplate.query.filter_by(category=template["category"]).first()
            if not existing:
                db.session.add(PromptTemplate(**template))

        db.session.commit()
        print("Prompt templates seeded successfully.")

    seed_prompt_templates()
