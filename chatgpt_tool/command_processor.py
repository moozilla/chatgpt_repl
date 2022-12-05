import subprocess
from typing import List, Tuple
from prompt_toolkit.completion import NestedCompleter, Completion
from prompt_toolkit.completion.filesystem import PathCompleter

class CommandProcessor:
    def __init__(self):
        self.commands = {
            "/exit": self.exit_command,
            "/help": self.help_command,
            "/file": self.file_command,
            "/exec": self.exec_command
        }

        # Create a PathCompleter instance for filename completion.
        self.filename_completer = PathCompleter()
        # Create a lookup of argument completers for each command.
        self.argument_completers = {
            "/file": self.filename_completer
        }

    def is_command(self, prompt: str) -> bool:
        """Check if the given prompt is a command."""
        return prompt.startswith("/")

    def process_command(self, command: str) -> bool:
        """Process the given command."""
        # Get the name and arguments of the command
        command_parts = []
        current_arg = ""
        in_quotes = False
        for c in command:
            if c == '"':
                in_quotes = not in_quotes
            elif c == " " and not in_quotes:
                command_parts.append(current_arg)
                current_arg = ""
            else:
                current_arg += c

        # Add the final argument
        command_parts.append(current_arg)

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

            data = f"# {filename}\n{data}"
            prompt_prefix = " ".join(args[1:])
            if prompt_prefix:
                data = f"{prompt_prefix}\n\n{data}"

            return False, data
        except IOError:
            print(f"Error: Could not read file {filename}")
            return False, None

    def exec_command(self, args: List[str]) -> Tuple[bool, str]:
        """Execute a shell command and return its output."""
        if len(args) == 0:
            print("Usage: /exec \"<command>\" [<prompt_prefix>]")
            return False, None

        command = args[0]
        prompt_prefix = " ".join(args[1:])
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            output = output.decode()
            if prompt_prefix:
                output = f"{prompt_prefix}\n\n{output}"
            return False, output
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            return False, None

class CommandCompleter(NestedCompleter):
    def __init__(self, command_processor):
        self.command_processor = command_processor

        # Build the nested completer options based on the command processor.
        nested_completer_options = {
            command: self.command_processor.argument_completers.get(command)
            for command, _ in self.command_processor.commands.items()
        }

        super().__init__(nested_completer_options)
