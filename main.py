import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()  # Load environment variables from .env

# Access the API key from the environment variable
gemini_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_api_key)

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# List of questions
questions = [
    # "What is the capital of France?",
    # "How many planets are in the solar system?",
    # "Who painted the Mona Lisa?",
    "A patient came to facility with shortness of breath, chest pains, sweating at night.Was in contact with someone who had TB and the guy had cough."
]

# Iterate through the questions and print responses
for question in questions:
    response = model.generate_content(question)
    print(response.text)