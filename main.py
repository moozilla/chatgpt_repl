from revChatGPT.revChatGPT import Chatbot
import json
import os
from dotenv import load_dotenv

def create_config():
    load_dotenv()
    access_token = os.getenv("access_token")
    config = {
        "Authorization": access_token
    }
    return config

def create_chatbot(config):
    chatbot = Chatbot(config, conversation_id=None)
    return chatbot

def get_chat_response(chatbot, prompt):
    response = chatbot.get_chat_response(prompt)

    if not isinstance(response, dict):
        if isinstance(response, ValueError):
            print("Warning: The access token may be invalid")
        # Return None to indicate that an error occurred
        return None

    print(response["message"])
    print(response["conversation_id"])
    print(response["parent_id"])

    return response


def main():
    config = create_config()
    chatbot = create_chatbot(config)
    prompt = "hello, tell me about your capabilities"

    # Get the chat response
    response = get_chat_response(chatbot, prompt)

    # Exit if an error occurred
    if response is None:
        return

if __name__ == "__main__":
    main()
