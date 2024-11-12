import os
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd

load_dotenv()  # Load environment variables from .env

# Access the API key from the environment variable
gemini_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_api_key)

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# List of questions
def get_questions_from_excel(filename):
    """Reads questions from column C, starting from row 2, of an Excel file using pandas.

    Args:
        filename: The name of the Excel file.

    Returns:
        A list of questions.
    """

    df = pd.read_excel(filename)
    questions = df['Describe the Situation (What was going on), Background (clinical history/context), Assessment (what was observed)'][1:].tolist()  # Select column C, starting from row 1 (index 0)


# Iterate through the questions and print responses
    for question in questions:
        response = model.generate_content(question)
        print(response.text)
        # TODO
        #  write to a column in the execl file


if __name__ == "__main__":
    get_questions_from_excel("questions.xlsx")