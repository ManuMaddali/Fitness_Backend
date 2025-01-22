
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

