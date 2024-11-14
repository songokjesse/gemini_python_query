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
    """Reads questions from column C, starting from row 2, of an Excel file using pandas.

    Args:
        filename: The name of the Excel file.

    Returns:
        A DataFrame with the questions and responses.
    """
    df = pd.read_excel(filename)
    questions = df[
                    'Describe the Situation (What was going on), Background (clinical history/context), Assessment (what was observed)'][
                1:]  # Select column C, starting from row 1 (index 0)

    responses = []
    for idx, question in enumerate(questions):
        try:
            response = rate_limited_call(model.generate_content, question)
            if hasattr(response, 'text'):
                clean_response = clean_response_text(response.text)
                responses.append(clean_response)
            else:
                responses.append("Response omitted due to content restrictions.")
        except google.api_core.exceptions.ResourceExhausted as e:
            print(f"Rate limit exceeded at question {idx}: {e}")
            # Save responses up to this point
            df.loc[1:len(responses), 'Gemini_LLM'] = responses
            save_updated_excel(df, filename)
            return df
        except Exception as e:
            print(f"An error occurred at question {idx}: {e}")
            responses.append("Error generating response.")

    # Add the responses to the DataFrame in a new column named "Gemini_LLM"
    df.loc[1:, 'Gemini_LLM'] = responses

    return df


# Save the updated DataFrame back to the Excel file
def save_updated_excel(df, filename):
    df.to_excel(filename, index=False)


if __name__ == "__main__":
    filename = "questions.xlsx"
    df = get_questions_from_excel(filename)
    save_updated_excel(df, filename)
