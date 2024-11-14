
# GeminiQ - Automated Question Response Script
## Overview

GeminiQ is a Python script designed to automate the process of generating responses to a set of questions from an Excel file using the Gemini AI model. The script reads questions from a specified column in an Excel file, queries the Gemini model to generate responses, and saves these responses back into a new column in the same Excel file. The script also handles rate limiting and ensures that previously generated responses are not overwritten.
Features

    1. Automated Response Generation: Uses the Gemini AI model to generate responses to questions from an Excel file.

    2. Rate Limiting: Incorporates a rate limiting function to avoid exceeding API call quotas.

    4. Incremental Saves: Saves progress and responses to the Excel file if the rate limit is reached or an error occurs.

    5. Duplicate Check: Skips generating responses for questions that already have a response in the "Gemini" column.

## Requirements

    - Python 3.7 or higher
    - pandas
    - dotenv
    - google-generativeai

## Installation

    1. Clone the repository:
        git clone https://github.com/songokjesse/gemini_python_query 
        cd GeminiQ
    2. Create a virtual environment and activate it:
        python3 -m venv venv source venv/bin/activate # On Windows use `venv\Scripts\activate`
    3. Install dependencies:
        pip install -r requirements.txt
    4. Set up environment variables:
        Create a .env file in the project directory.    
        Add your Gemini API key to the .env file:
            GEMINI_API_KEY=your_api_key_here
# Script Details

### main.py

- Imports and Configurations: Loads environment variables, configures the Gemini model, and imports necessary libraries.

- rate_limited_call: A function to enforce a delay between API calls to avoid hitting rate limits.

- clean_response_text: A function to clean up response text by removing unwanted characters (e.g., asterisks).

- get_questions_from_excel: Reads the Excel file, generates responses for each question, and saves the responses in a new column named "Gemini".

- save_updated_excel: Saves the updated DataFrame back to the Excel file.

### Example

Suppose your Excel file "questions.xlsx" has questions in column C (index 2). The script will read these questions, generate responses using the Gemini AI model, and save the responses in a new column named "Gemini".

### Contributing

Feel free to contribute to this project by opening issues or submitting pull requests. Your feedback and improvements are welcome!

### License

This project is licensed under the MIT License.