import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import json

# config of gemini api
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)


# function declaration for review
review_function = {
    "name": "collect_review",
    "description": "Collects user feedback after chat ends.",
    "parameters": {
        "type": "object",
        "properties": {
            "review": {
                "type": "string",
                "description": "User's feedback on the chatbot interaction.",
            },
            "rating": {
                "type": "integer",
                "description": "Rating between 1 to 5 for the chat experience.",
            },
        },
        "required": ["review", "rating"],
    },
}

# Config of function Call
tools = types.Tool(function_declarations=[review_function])
config = types.GenerateContentConfig(tools=[tools])


def chat_with_gemini(user_message):
    """ Sends user message to Gemini API and returns the response. """
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[user_message]
    )
    return response.candidates[0].content.parts[0].text if response.candidates else "No response received."


def collect_review():
    """Collects review and rating manually before invoking Gemini API."""
    
    review = input("Your feedback: ")
    while True:
        try:
            rating = int(input("Rate your chat experience (1-5): "))
            if 1 <= rating <= 5:
                break
            else:
                print("Please enter a valid rating between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")

    review_prompt = (
        f"Invoke 'collect_review' function with the following details:\n"
        f"{{'review': '{review}', 'rating': {rating}}}"
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[review_prompt],
        config=config,
    )

    if response.candidates and response.candidates[0].content.parts:
        part = response.candidates[0].content.parts[0]

        if hasattr(part, "function_call") and part.function_call:
            function_call = part.function_call

            feedback = function_call.args if hasattr(function_call, "args") else None
            if feedback:
                save_feedback(feedback)
            else:
                print("Function call detected, but no arguments received.")
        else:
            print("No function call detected. Saving manually.")
            save_feedback({'review': review, 'rating': rating})
    else:
        print("Unexpected API response format.")


def save_feedback(feedback):
    """ Saves feedback to a text file. """
    with open("feedback.txt", "a") as file:
        file.write(json.dumps(feedback, indent=4) + "\n")
    print("Thank you! Your feedback has been saved.")

def check_exit_intent(user_message):
    """Sends the user message to Gemini and asks if the user wants to exit."""
    prompt = f"Does the following user message indicate an intent to end the conversation? Respond with 'yes' or 'no'.\n\nUser: {user_message}"
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt]
    )

    exit_phrases = ["bye", "exit", "end chat", "i want to leave"]
    if response.candidates and response.candidates[0].content.parts:
        exit_intent = response.candidates[0].content.parts[0].text.strip().lower()
        if "yes" in exit_intent:
            print("Say bye, exit, or end chat, If you want to leave the chat.")
            if user_message.lower() in exit_phrases:
                return True
    return False


def main():
    print("Welcome to the CLI Chatbot! Type your messages below.")
    while True:
        user_input = input("> ")

        if check_exit_intent(user_input):
            print("ChatBot: Before you leave, Kindly give your feedback.")
            collect_review()
            break
        response = chat_with_gemini(user_input)
        print(f"CLI ChatBot: {response}")

if __name__ == "__main__":
    main()