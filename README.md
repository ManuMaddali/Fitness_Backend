
## Fitness App Backend

Welcome to the **Fitness App Backend**, a feature-rich API designed to provide personalized fitness, nutrition, and wellness support. This project demonstrates my ability to leverage modern frameworks, cutting-edge AI technologies, and scalable development practices.

## 🚀 Features

- **Authentication System**
  - Secure login and registration with password encryption.
  - Role-based access control for tiered functionality (free and premium).

- **Fitness and Nutrition Modules**
  - Basal Metabolic Rate (BMR), Total Daily Energy Expenditure (TDEE), and Hydration calculators.
  - AI-powered Fitness Coach API for advice on workouts, nutrition, and mental wellness.

- **Integration with AI Models**
  - **LLMWrapper** for seamless integration of Large Language Models (LLMs) into the `/api/coach` endpoint.
  - **LangChain Framework** to structure multi-step reasoning, memory management, and dynamic chatbot responses for the `/api/full_coach` endpoint. 

- **Premium Features**
  - Advanced analytics and personalized fitness and nutrition plans powered by AI.
  - Modular endpoints for hydration and BMR/TDEE for free-tier users.

- **Database-Driven Insights**
  - Robust user data management using SQLite for fast and reliable performance.

- **API Documentation**
  - Seamless testing and integration with tools like Postman.
  - Clear and concise endpoint definitions.

## 🛠️ Technologies Used

- **Backend Framework:** Flask (Python)
- **Database:** SQLite
- **API Testing:** Postman
- **AI Integration:** OpenAI GPT Models via LLMWrapper, LangChain
- **Security:** JWT Authentication, bcrypt password hashing
- **Version Control:** Git, GitHub

## 🧠 LLM-Powered Fitness Coaching

The `/api/coach` endpoint is enhanced by:

- **LLMWrapper Integration**:
  - Streamlined LLM API calls for efficient interaction with OpenAI GPT models.
  - Custom prompt templates to generate tailored fitness, nutrition, and mental wellness advice.

The `/api/full_coach` endpoint is enhanced by:
- **LangChain Features**:
  - **Prompt Chaining**: Delivers multi-turn conversations, enabling more contextual and dynamic interactions.
  - **Memory Management**: Retains user preferences, previous queries, and history for a personalized coaching experience.
  - **Custom Tools**: Extends LangChain tools to include calculations for hydration, BMR, and TDEE, dynamically invoked during chatbot conversations.

This combination enables a conversational AI coach that provides actionable, personalized advice, making it a cornerstone of the app's premium features.


## 📈 Highlights and Accomplishments

- **AI Integration**: Successfully implemented LLMWrapper and LangChain to power conversational and dynamic AI responses.
- **User-Centric Design**: Developed APIs with a clear focus on usability and modularity to support standalone and premium features.
- **Scalable Architecture**: Organized code for future expansion, such as incorporating real-time fitness tracking or predictive analytics.
- **Security First**: Implemented robust authentication mechanisms to safeguard user data.

## 🌲 Project Structure
```plaintext
Fitness_Backend
├── instance
│   ├── users.db               # Main SQLite database storing user data
│   ├── users_backup.db        # Backup of the database for safety and recovery
├── migrations
│   ├── README                 # Overview of migration scripts and usage
│   ├── alembic.ini            # Configuration file for Alembic, managing database migrations
│   ├── env.py                 # Environment setup for Alembic migrations
│   ├── script.py.mako         # Template for generating migration scripts
├── routes
│   ├── auth.py                # API routes for user authentication (login, signup, etc.)
│   ├── bmr.py                 # Endpoint for calculating Basal Metabolic Rate (BMR)
│   ├── coach.py               # Core logic for fitness coaching functionality
│   ├── full_coach.py          # Advanced coaching features for premium users
│   ├── history.py             # Handles retrieval and management of user fitness history
│   ├── hydration.py           # Endpoint for tracking and calculating hydration needs
│   ├── login.py               # Dedicated login functionality
│   ├── register.py            # Handles user registration and account creation
│   ├── reset_history.py       # API route for resetting user history
├── static
│                               # Placeholder for static files (e.g., images, CSS, JavaScript)
├── templates
│                               # Placeholder for HTML templates (if using a web interface)
├── tests
│   ├── __init__.py            # Marks the tests folder as a Python package
│   ├── conftest.py            # Shared fixtures and configuration for pytest
│   ├── test_auth.py           # Unit tests for authentication-related functionality
│   ├── test_coach.py          # Unit tests for the coaching module
│   ├── test_full_coach.py     # Tests for premium coaching features
│   ├── test_history.py        # Tests for user fitness history management
│   ├── test_reset_history.py  # Tests for resetting user data and history
├── utils
│   ├── auth_utils.py          # Helper functions for authentication processes
│   ├── database_utils.py      # Utility functions for database operations and queries
│   ├── validation_utils.py    # Validation logic for inputs and user data
│   ├── Seed_prompt_templates.py
│                               # Predefined prompt templates for generating dynamic responses
├── models.py                  # Defines database models and ORM (Object-Relational Mapping) logic
├── app.py                     # Entry point of the application; initializes the app and routes
 
```
## 🧪 How to Run Locally

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/fitness-backend.git
   cd fitness-backend
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```

5. **Access the API**
   The API will be available at `http://127.0.0.1:5000`.

## 💡 Future Plans

- **Enhanced AI Models**: Fine-tune LLMs to provide even more accurate and personalized fitness plans.
- **Frontend Development**: Pair with a React or Flutter frontend for a seamless user experience.
- **Cloud Deployment**: Host the application on AWS or GCP for global accessibility.

## 🧑‍💻 About Me

I am a **Product Manager and Backend Developer** with 3 years of experience in financial technology and data science. I have a strong passion for building AI-powered solutions and specialize in creating user-centric products by leveraging modern frameworks and implementing scalable architectures.

Connect with me on [LinkedIn](https://linkedin.com/in/your-profile) 

