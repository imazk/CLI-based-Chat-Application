#!/usr/bin/env python3
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
        contents=[user_message],
        config=config
    )
    return response.candidates[0].content.parts[0].text if response.candidates else "No response received."


def save_feedback(feedback):
    """ Saves feedback to a text file. """
    with open("feedback.txt", "a") as file:
        file.write(json.dumps(feedback, indent=4) + "\n")
    print("Thank you! Your feedback has been saved.")


def check_exit_intent(user_message):
    """Checks if the user wants to exit the chat."""
    prompt = f"""
    Determine if the following user message indicates an intent to end the conversation.
    Respond with 'yes' if the user wants to exit, otherwise respond with 'no'.
    User: {user_message}
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt]
    )

    if response.candidates and response.candidates[0].content.parts:
        exit_intent = response.candidates[0].content.parts[0].text.strip().lower()
        return "yes" in exit_intent
    return False


def ask_question_to_user(question_text):
    """Generates a natural-sounding question from Gemini."""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[question_text]
    )
    return response.candidates[0].content.parts[0].text.strip()


def collect_review_chat():
    """Interactively collects review and rating from the user."""
    print("\nBefore you go, could you please provide some feedback?")

    review_question = ask_question_to_user("Ask the user how their chatbot experience was.")
    print(f"CLI ChatBot: {review_question}")
    review = input("> ")

    while True:
        rating_question = ask_question_to_user("Ask the user to rate the chatbot experience on a scale from 1 to 5.")
        print(f"CLI ChatBot: {rating_question}")
        try:
            rating = int(input("> "))
            if 1 <= rating <= 5:
                break
            else:
                print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Please enter a valid number.")

    feedback = {
        "review": review,
        "rating": rating
    }
    save_feedback(feedback)


def main():
    print("Welcome to the CLI Chatbot! Type your messages below.")
    while True:
        user_input = input("> ")
        response = chat_with_gemini(user_input)
        print(f"CLI ChatBot: {response}")

        if check_exit_intent(user_input):
            collect_review_chat()
            break


if __name__ == "__main__":
    main()
