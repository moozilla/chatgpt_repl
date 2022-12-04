from typing import List

class CommandProcessor:
    def __init__(self):
        self.commands = {
            "/exit": self.exit_command,
            "/help": self.help_command
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

    def exit_command(self, args: List[str]) -> bool:
        """Exit the program."""
        return True

    def help_command(self, args: List[str]) -> bool:
        """List available commands."""
        print("Available commands:")
        for command_name, command_handler in self.commands.items():
            print(f"* {command_name} - {command_handler.__doc__}")
        return False
