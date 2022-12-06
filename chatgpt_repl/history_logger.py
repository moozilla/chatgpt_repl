from pathlib import Path
from datetime import datetime


class ConversationNotInitializedError(Exception):
    """Exception raised when trying to log prompt and response without setting conversation ID"""


class HistoryLogger:
    def __init__(self, session_name):
        self.session_name = session_name
        # Create the history directory if it doesn't exist
        Path("history").mkdir(parents=True, exist_ok=True)
        self.history_file = None

    def init(self, conversation_id):
        self.conversation_id = conversation_id
        self.open_history_file()

    def open_history_file(self):
        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")

        # Open the history file for the current conversation ID, with the timestamp prepended to the filename
        self.history_file = open(
            f"history/{timestamp}_{self.session_name}_{self.conversation_id}.txt", "a"
        )

    def log_prompt_response(self, prompt, response):
        if not self.history_file:
            raise ConversationNotInitializedError(
                "History file must be opened before logging prompt and response"
            )

        # Write the prompt and response to the history file
        self.history_file.write(f"---prompt---\n{prompt}\n")
        self.history_file.write(f"---response---\n{response['message']}\n")
        self.history_file.flush()

    def __del__(self):
        if self.history_file:
            self.history_file.close()
