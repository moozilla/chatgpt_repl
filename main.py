import os
from pathlib import Path
from dotenv import load_dotenv
from revChatGPT.revChatGPT import Chatbot

class HistoryLogger:
    def __init__(self):
        # Create the history directory if it doesn't exist
        Path("history").mkdir(parents=True, exist_ok=True)

    def set_conversation_id(self, conversation_id):
        # Open the history file for the current conversation ID
        self.history_file = Path(f"history/{conversation_id}.txt")
        self.history_file.touch()

    def log_prompt_response(self, prompt, response):
        with self.history_file.open("a") as f:
            # Write the prompt and response to the history file
            f.write(f"---prompt---\n{prompt}\n")
            f.write(f"---response---\n{response['message']}\n")


class ChatSession:
    def __init__(self, access_token, initial_prompt, conversation_id=None):
        self.initial_prompt = initial_prompt
        self.history_logger = HistoryLogger()
        self.conversation_id = conversation_id

        config = self.create_config(access_token)
        self.chatbot = self.create_chatbot(config, conversation_id)

    @staticmethod
    def create_config(access_token):
        return {
            "Authorization": access_token
        }

    @staticmethod
    def create_chatbot(config, conversation_id=None):
        return Chatbot(config, conversation_id)

    def get_chat_response(self, prompt):
        response = self.chatbot.get_chat_response(prompt)

        if not isinstance(response, dict):
            if isinstance(response, ValueError):
                print("Warning: The access token may be invalid")

            return None

        if self.conversation_id is None:
            # Save the conversation ID and create the history logger
            self.conversation_id = response["conversation_id"]
            self.history_logger.set_conversation_id(self.conversation_id)

        self.history_logger.log_prompt_response(prompt, response)
        return response

    def run_prompt_loop(self):
        while True:
            prompt = input("Enter a prompt: ")
            # Check if the user wants to exit
            if prompt.lower() == "exit":
                break

            response = self.get_chat_response(prompt)
            if response is None:
                continue

            print(response["message"])

    def start(self):
        # Provide the initial prompt to the chatbot
        initial_response = self.get_chat_response(self.initial_prompt)
        if initial_response is None:
            # There was an error, most likely an expired session
            return
        print(initial_response["message"])

        # Start the input loop
        self.run_prompt_loop()


def main():
    load_dotenv()
    access_token = os.getenv("access_token")
    initial_prompt = os.getenv("initial_prompt")

    chat_session = ChatSession(access_token, initial_prompt)
    chat_session.start()


if __name__ == "__main__":
    main()
