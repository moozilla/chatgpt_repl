from pathlib import Path
from revChatGPT.revChatGPT import Chatbot
import json
import os
from dotenv import load_dotenv


class HistoryLogger:
    def __init__(self, conversation_id):
        # Create the history directory if it doesn't exist
        Path("history").mkdir(parents=True, exist_ok=True)

        # Open the history file for the current conversation ID
        self.history_file = Path(f"history/{conversation_id}.txt")
        self.history_file.touch()

    def log_prompt_response(self, prompt, response):
        with self.history_file.open("a") as f:
            # Write the prompt and response to the history file
            f.write(f"---prompt---\n{prompt}\n")
            f.write(f"---response---\n{response['message']}\n")


class ChatSession:
    def __init__(self, chatbot):
        self.chatbot = chatbot
        self.history_logger = None

    def start(self):
        while True:
            prompt = input("Enter a prompt: ")
            # Check if the user wants to exit
            if prompt.lower() == "exit":
                break

            response = self.chatbot.get_chat_response(prompt)
            if not isinstance(response, dict):
                if isinstance(response, ValueError):
                    print("Warning: The access token may be invalid")

                continue

            if self.history_logger is None:
                # Set the conversation ID and create the history logger
                self.history_logger = HistoryLogger(response["conversation_id"])

            self.history_logger.log_prompt_response(prompt, response)
            print(response["message"])


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


def main():
    config = create_config()
    chatbot = create_chatbot(config)

    chat_session = ChatSession(chatbot)
    chat_session.start()


if __name__ == "__main__":
    main()
