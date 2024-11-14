import os
import time
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd
import google.api_core.exceptions

load_dotenv()  # Load environment variables from .env

# Access the API key from the environment variable
gemini_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_api_key)

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-1.5-flash-latest")


# Rate limiting function
def rate_limited_call(func, *args, **kwargs):
    time.sleep(1)  # Sleep for 1 second
    return func(*args, **kwargs)


# Function to clean the response text
def clean_response_text(text):
    return text.replace('*', '')


# List of questions
def get_questions_from_excel(filename):
    """Reads questions from an Excel file and generates responses using Gemini model.

    Args:
        filename: The name of the Excel file.

    Returns:
        A DataFrame with the questions and responses.
    """
    df = pd.read_excel(filename)
    questions = df[
                    'Describe the Situation (What was going on), Background (clinical history/context), Assessment (what was observed)'][
                1:]  # Select column C, starting from row 1 (index 0)

    # Ensure the Gemini column exists
    if 'Gemini_LLM' not in df.columns:
        df['Gemini_LLM'] = None

    for idx, question in questions.items():  # Updated to use items
        row_idx = idx + 1  # Adjust index to match DataFrame rows
        if row_idx not in df.index:
            continue  # Skip if index is out of range
        if pd.notna(df.at[row_idx, 'Gemini_LLM']):
            continue  # Skip if response already exists

        try:
            response = rate_limited_call(model.generate_content, question)
            if hasattr(response, 'text'):
                clean_response = clean_response_text(response.text)
                df.at[row_idx, 'Gemini_LLM'] = clean_response
            else:
                df.at[row_idx, 'Gemini_LLM'] = "Response omitted due to content restrictions."
        except google.api_core.exceptions.ResourceExhausted as e:
            print(f"Rate limit exceeded at question {idx}: {e}")
            # Save responses up to this point
            save_updated_excel(df, filename)
            return df
        except Exception as e:
            print(f"An error occurred at question {idx}: {e}")
            df.at[row_idx, 'Gemini_LLM'] = "Error generating response."

    return df


# Save the updated DataFrame back to the Excel file
def save_updated_excel(df, filename):
    df.to_excel(filename, index=False)


if __name__ == "__main__":
    filename = "questions.xlsx"
    df = get_questions_from_excel(filename)
    save_updated_excel(df, filename)
