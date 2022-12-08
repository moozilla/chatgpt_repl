from typing import Dict, Optional
from prompt_toolkit import prompt
from revChatGPT.revChatGPT import Chatbot
from .command_processor import CommandProcessor, CommandCompleter
from .history_logger import HistoryLogger
from .response_processor import ResponseProcessor


class ChatSession:
    def __init__(
        self,
        session_name: str,
        session_token: str,
        initial_prompt: str,
        conversation_id: Optional[str] = None,
    ):
        """Initialize a new `ChatSession` instance."""
        output_dir = f"outputs/{session_name}"

        self.initial_prompt = initial_prompt
        self.history_logger = HistoryLogger(session_name)
        self.conversation_id = conversation_id

        config = self.create_config(session_token)
        self.chatbot = self.create_chatbot(config, conversation_id)
        self.command_processor = CommandProcessor()
        self.command_completer = CommandCompleter(self.command_processor)
        self.response_processor = ResponseProcessor(output_dir)

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
        print("...")
        try:
            response = self.chatbot.get_chat_response(prompt, output="text")
        except ValueError:
            # TODO: this may be unnecessary, revChatGPT tries to autorefresh now
            if not is_retry:
                print(
                    "Warning: The access token may be invalid! Attempting to refresh session."
                )
                self.chatbot.refresh_session()
                return self.get_chat_response(prompt, True)
            return None

        if self.conversation_id is None:
            # Save the conversation ID and create the history logger
            self.conversation_id = response["conversation_id"]
            self.history_logger.init(self.conversation_id)

        self.history_logger.log_prompt_response(prompt, response)
        return response

    def run_prompt_loop(self):
        """Run the input loop for the chat session."""
        print(
            "-- /help for available commands, /exit to exit, option+Enter to submit --"
        )
        while True:
            raw_prompt = self.get_raw_prompt()
            if self.command_processor.is_command(raw_prompt):
                should_exit, command_prompt = self.command_processor.process_command(
                    raw_prompt
                )
                if should_exit:
                    break
                if command_prompt is not None:
                    self.handle_response(command_prompt)
            else:
                self.handle_response(raw_prompt)

    def get_raw_prompt(self):
        return prompt(
            "Enter a prompt: ",
            completer=self.command_completer,
            complete_while_typing=True,
            multiline=True,
        )

    def process_command(self, raw_prompt):
        return self.command_processor.process_command(raw_prompt)

    def handle_response(self, prompt):
        response = self.get_chat_response(prompt)
        if response is not None:
            parsed_response = self.response_processor.process_response(response)
            print("\n" + parsed_response + "\n")
            if self.response_processor.was_cutoff:
                print("RESPONSE MAY HAVE BEEN CUT OFF")

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
