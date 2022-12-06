from typing import Dict, Optional
from prompt_toolkit import prompt
from revChatGPT.revChatGPT import Chatbot
from .command_processor import CommandProcessor, CommandCompleter
from .history_logger import HistoryLogger


class ChatSession:
    def __init__(
        self,
        session_token: str,
        initial_prompt: str,
        conversation_id: Optional[str] = None,
    ):
        """Initialize a new `ChatSession` instance."""
        self.initial_prompt = initial_prompt
        self.history_logger = HistoryLogger()
        self.conversation_id = conversation_id

        config = self.create_config(session_token)
        self.chatbot = self.create_chatbot(config, conversation_id)
        self.command_processor = CommandProcessor()
        self.command_completer = CommandCompleter(self.command_processor)

    @staticmethod
    def create_config(session_token: str) -> Dict[str, str]:
        """Create the configuration object to use when communicating with the chatbot API."""
        return {
            "Authorization": "",  # will be set using session_token
            "session_token": session_token,
        }

    @staticmethod
    def create_chatbot(
        config: Dict[str, str], conversation_id: Optional[str] = None
    ) -> Chatbot:
        """Create a new `Chatbot` instance."""
        return Chatbot(config, conversation_id)

    def get_chat_response(
        self, prompt: str, is_retry: bool = False
    ) -> Optional[Dict[str, str]]:
        """Get a response from the chatbot for the given prompt."""
        # TODO: update to use streaming now supported by revChatGPT
        response = self.chatbot.get_chat_response(prompt, output="text")

        if not isinstance(response, dict):
            if isinstance(response, ValueError):
                if not is_retry:
                    print(
                        "Warning: The access token may be invalid! Attempting to refresh session."
                    )
                    self.chatbot.refresh_session()
                    return self.get_chat_response(prompt, True)
                else:
                    # Don't try again to avoid retry loop
                    pass
            return None

        if self.conversation_id is None:
            # Save the conversation ID and create the history logger
            self.conversation_id = response["conversation_id"]
            self.history_logger.init(self.conversation_id)

        self.history_logger.log_prompt_response(prompt, response)
        return response

    def run_prompt_loop(self):
        """Run the input loop for the chat session, with tab completion."""
        print("-- Enter /help for available commands, /exit to exit --")
        while True:
            raw_prompt = prompt(
                "Enter a prompt: ",
                completer=self.command_completer,
                complete_while_typing=True,
            )
            # Check if the user entered a command
            if self.command_processor.is_command(raw_prompt):
                # Process the command and check if we should exit the input loop
                should_exit, command_prompt = self.command_processor.process_command(
                    raw_prompt
                )
                if should_exit:
                    break

                # Check if the command returned a prompt to use
                if command_prompt is not None:
                    # Get a response from the chatbot using the prompt returned by the command
                    response = self.get_chat_response(command_prompt)
                    if response is not None:
                        print("\n" + response["message"] + "\n")
            else:
                # Get a response from the chatbot
                response = self.get_chat_response(raw_prompt)
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
            print("No response. Most likely an expired session.")
            return
        print("\n" + initial_response["message"] + "\n")

        # Start the input loop
        self.run_prompt_loop()
