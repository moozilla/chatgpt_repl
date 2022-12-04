from typing import Dict
from revChatGPT.revChatGPT import Chatbot
from .command_processor import CommandProcessor
from .history_logger import HistoryLogger

class ChatSession:
    def __init__(self, access_token: str, initial_prompt: str, conversation_id: str = None):
        """Initialize a new `ChatSession` instance."""
        self.initial_prompt = initial_prompt
        self.history_logger = HistoryLogger()
        self.conversation_id = conversation_id

        config = self.create_config(access_token)
        self.chatbot = self.create_chatbot(config, conversation_id)
        self.command_processor = CommandProcessor()

    @staticmethod
    def create_config(access_token: str) -> Dict[str, str]:
        """Create the configuration object to use when communicating with the chatbot API."""
        return {
            "Authorization": access_token
        }

    @staticmethod
    def create_chatbot(config: Dict[str, str], conversation_id: str = None) -> Chatbot:
        """Create a new `Chatbot` instance."""
        return Chatbot(config, conversation_id)

    def get_chat_response(self, prompt: str) -> Dict[str, str]:
        """Get a response from the chatbot for the given prompt."""
        response = self.chatbot.get_chat_response(prompt)

        if not isinstance(response, dict):
            if isinstance(response, ValueError):
                print("Warning: The access token may be invalid")

            return None

        if self.conversation_id is None:
            # Save the conversation ID and create the history logger
            self.conversation_id = response["conversation_id"]
            self.history_logger.init(self.conversation_id)

        self.history_logger.log_prompt_response(prompt, response)
        return response

    def run_prompt_loop(self):
        """Run the input loop for the chat session."""
        print("-- Enter /help for available commands, /exit to exit --\n")
        while True:
            prompt = input("Enter a prompt: ")
            # Check if the user entered a command
            if self.command_processor.is_command(prompt):
                # Process the command and check if we should exit the input loop
                should_exit = self.command_processor.process_command(prompt)
                if should_exit:
                    break
            else:
                # Get a response from the chatbot
                response = self.get_chat_response(prompt)
                if response is None:
                    continue

                print("\n" + response["message"] + "\n")

    def start(self):
        """Start the chat session."""
        # Provide the initial prompt to the chatbot
        print("Sending initial prompt to ChatGPT")
        print(f"> {self.initial_prompt}")
        initial_response = self.get_chat_response(self.initial_prompt)
        if initial_response is None:
            # There was an error, most likely an expired session
            return
        print("\n" + initial_response["message"] + "\n")

        # Start the input loop
        self.run_prompt_loop()
