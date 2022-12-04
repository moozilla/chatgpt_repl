from typing import List, Tuple

class CommandProcessor:
    def __init__(self):
        self.commands = {
            "/exit": self.exit_command,
            "/help": self.help_command,
            "/file": self.file_command
        }

    def is_command(self, prompt: str) -> bool:
        """Check if the given prompt is a command."""
        return prompt.startswith("/")

    def process_command(self, command: str) -> bool:
        """Process the given command."""
        # Get the name and arguments of the command
        command_parts = command.split(" ")
        command_name = command_parts[0]
        command_args = command_parts[1:]

        command_handler = self.commands.get(command_name)
        if command_handler is None:
            print(f"Unrecognized command: {command_name}")
            return False

        # Call the command handler
        return command_handler(command_args)

    def exit_command(self, args: List[str]) -> Tuple[bool, str]:
        """Exit the program."""
        return True, None

    def help_command(self, args: List[str]) -> Tuple[bool, str]:
        """List available commands."""
        print("Available commands:")
        for command_name, command_handler in self.commands.items():
            print(f"* {command_name} - {command_handler.__doc__}")
        return False, None

    def file_command(self, args: List[str]) -> Tuple[bool, str]:
        """Read the contents of a file and use it as a prompt."""
        if len(args) == 0:
            print("Usage: /file <filename> [<prompt_prefix>]")
            return False, None

        filename = args[0]
        try:
            with open(filename, "r") as f:
                data = f.read()

            prompt_prefix = " ".join(args[1:])
            if prompt_prefix:
                data = f"{prompt_prefix}\n\n{data}"

            return False, data
        except IOError:
            print(f"Error: Could not read file {filename}")
            return False, None
