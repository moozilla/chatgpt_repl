from pathlib import Path

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
