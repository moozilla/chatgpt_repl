from pathlib import Path
from typing import Dict, List, Optional


class ResponseProcessor:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.processors = [
            self.process_code_blocks,
        ]

        # Use a counter to keep track of code block numbers
        self.code_block_counter = 0

    def process_response(self, response: Dict[str, str]) -> str:
        """Process the chatbot response."""
        text = response["message"]

        # Apply processing functions
        for processor in self.processors:
            text = processor(text)

        return text

    def process_code_blocks(self, text: str) -> str:
        """Process any markdown code blocks in the text."""
        if "```" not in text:
            return text

        # Split on newlines to get individual lines
        lines = text.split("\n")

        # Iterate through lines and build new string
        parsed_text = ""
        in_code_block = False
        code_lines = []
        for line in lines:
            if not in_code_block:
                # If not in a code block, add line to output
                parsed_text += line + "\n"
            if line == "```":
                # If line is start or end of code block, toggle flag
                in_code_block = not in_code_block
                if not in_code_block:
                    # If code block just ended, save the lines to file and
                    # update the parsed text
                    filename = self.save_code_lines(code_lines)
                    code_lines = []
                    if filename:
                        parsed_text += f"<CODE BLOCK {self.code_block_counter} - saved to {filename}>\n"
            elif in_code_block:
                # If in code block, add line to code lines
                code_lines.append(line)
        return parsed_text

    def save_code_lines(self, lines: List[str]) -> Optional[str]:
        """Save the given code lines to a file and return the filename."""
        if not lines:
            return None

        # Get the filename from the first line, or generate one
        filename = lines[0]
        if not filename.startswith("# "):
            self.code_block_counter += 1
            filename = f"code_block_{self.code_block_counter}.py"
        else:
            filename = filename[2:]

        # Create the output directory and any necessary directories in the filename if they don't exist
        output_path = Path(self.output_dir)
        (output_path / filename).parent.mkdir(parents=True, exist_ok=True)

        # Remove the filename line from the code lines if it exists
        if filename.startswith("# "):
            lines = lines[1:]

        # Save the code lines to the file
        with open(output_path / filename, "w") as f:
            for line in lines:
                f.write(line + "\n")

        return filename
