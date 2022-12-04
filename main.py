import revChatGPT
import json
import os
from dotenv import load_dotenv

def load_access_token():
    # Load environment variables from the .env file
    load_dotenv()

    # Get the access token from the environment variable
    access_token = os.getenv("access_token")
    return access_token

def create_chatbot(access_token):
    # Create the chatbot using the access token
    chatbot = Chatbot(access_token, conversation_id=None)
    return chatbot

def get_chat_response(chatbot, prompt):
    # Use the chatbot to get a response to the given prompt
    response = chatbot.get_chat_response(prompt)

    # Print the response
    print(response["message"])
    print(response["conversation_id"])
    print(response["parent_id"])

def main():
    # Load the access token
    access_token = load_access_token()

    # Create the chatbot
    chatbot = create_chatbot(access_token)

    # Use the chatbot to get a response
    prompt = "hello, tell me about your capabilities"
    get_chat_response(chatbot, prompt)

if __name__ == "__main__":
    main()
