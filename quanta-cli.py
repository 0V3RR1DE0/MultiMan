# Quanta.py

import argparse
import importlib.util
import os
import datetime
import socket
import setproctitle
import shutil
import sys

# Change the console window title
os.system("title Quanta")

# Change the process name
setproctitle.setproctitle("Quanta")

# Determine the base directory of the main script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_module(module_path):
    spec = importlib.util.spec_from_file_location("module", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_command_info(module_path):
    module = load_module(module_path)
    description = getattr(module, "DESCRIPTION", "No description available")
    args = getattr(module, "ARGS", "")
    aliases = getattr(module, "ALIASES", [])
    return description, args, aliases

def list_commands():
    print("\033[1m\033[4mAvailable commands:\033[0m")
    print()

    # Print base commands
    print("\033[1mBase commands:\033[0m")
    print("- help: Display available commands and their descriptions")
    print("- clear: Clear the screen")
    print("- version: Display the CLI version")
    print("- time: Display the current date and time")
    print("- ls <directory>: List contents of a directory")
    print("- cd <directory>: Change the current working directory")
    print("- echo <text>: Echo back the provided text or create/edit files")
    print("- cat <file>: Display the contents of a file")
    print("- mkdir <directory>: Create a new directory")
    print("- rm <options> <file/directory>: Remove a file or directory")
    print()

    # Print original tools
    print("\033[1mOriginal tools:\033[0m")
    for script_dir in [os.path.join(BASE_DIR, "scripts/original_tools")]:
        for script_file in os.listdir(script_dir):
            if script_file.endswith(".py") and not script_file.startswith("__"):
                module_name = os.path.splitext(script_file)[0]
                module_path = os.path.join(script_dir, script_file)
                description, args, aliases = get_command_info(module_path)
                if isinstance(args, (tuple, list)):
                    args_str = " ".join(args)
                else:
                    args_str = args
                alias_str = f" (Aliases: {', '.join(aliases)})" if aliases else ""
                print(f"- {module_name} {args_str}: {description}{alias_str}")
    print()

    # Print addons
    addon_found = False
    print("\033[1mAddons:\033[0m")
    for script_dir in [os.path.join(BASE_DIR, "scripts/addons")]:
        for script_file in os.listdir(script_dir):
            if script_file.endswith(".py") and not script_file.startswith("__"):
                module_name = os.path.splitext(script_file)[0]
                module_path = os.path.join(script_dir, script_file)
                description, args, aliases = get_command_info(module_path)
                if isinstance(args, (tuple, list)):
                    args_str = " ".join(args)
                else:
                    args_str = args
                alias_str = f" (Aliases: {', '.join(aliases)})" if aliases else ""
                print(f"- {module_name} {args_str}: {description}{alias_str}")
                addon_found = True
    if not addon_found:
        print("No addons available")
    print()

    # Print addon examples
    print("\033[1mAddon examples:\033[0m")
    for script_dir in [os.path.join(BASE_DIR, "scripts/addons/examples")]:
        for script_file in os.listdir(script_dir):
            if script_file.endswith(".py") and not script_file.startswith("__"):
                module_name = os.path.splitext(script_file)[0]
                module_path = os.path.join(script_dir, script_file)
                description, args, aliases = get_command_info(module_path)
                if isinstance(args, (tuple, list)):
                    args_str = " ".join(args)
                else:
                    args_str = args
                alias_str = f" (Aliases: {', '.join(aliases)})" if aliases else ""
                print(f"- {module_name} {args_str}: {description}{alias_str}")


def execute_command(command):
    parts = command.split(" ", 1)
    cmd = parts[0]
    args = parts[1] if len(parts) > 1 else ""

    found = False

    # Check both directories for the specified command
    for script_dir in [os.path.join(BASE_DIR, "scripts/original_tools"), os.path.join(BASE_DIR, "scripts/addons")]:
        for script_file in os.listdir(script_dir):
            if script_file.endswith(".py") and not script_file.startswith("__"):
                module_name = os.path.splitext(script_file)[0]
                module_path = os.path.join(script_dir, script_file)
                module = load_module(module_path)
                aliases = getattr(module, "ALIASES", [])

                if cmd == module_name or cmd in aliases:
                    main_func = module.main
                    found = True

                    # Check if the main function accepts arguments based on ARGS attribute
                    module_args = getattr(module, "ARGS", [])
                    if len(module_args) == 0:
                        main_func()
                    else:
                        if not args:
                            print(f"Error: Command '{cmd}' requires arguments: {' '.join(module_args)}")
                        else:
                            main_func(*args.split())
                    break

        if found:
            break

    if not found:
        print(f"Command '{cmd}' not found.")

def clear_screen():
    """Clears the screen."""
    # ANSI escape codes for clearing the screen
    print("\033c", end="")

def display_version():
    """Displays the CLI version."""
    print("Python Multitool CLI version 1.0")

def display_time():
    """Displays the current date and time."""
    print("Current date and time:", datetime.datetime.now())

def list_directory(directory="."):
    """Lists the contents of a directory."""
    try:
        items = os.listdir(directory)
        print(f"Contents of directory '{directory}':")
        for item in items:
            print(f"  {item}")
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found.")

def change_directory(directory):
    """Changes the current working directory."""
    try:
        os.chdir(directory)
        print(f"Changed directory to: {os.getcwd()}")
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found.")

def echo(args):
    """Echoes back the provided text or creates/edits files."""
    if ">>" in args:
        command, filename = args.split(">>", 1)
        with open(filename.strip(), "a") as file:
            file.write(command.strip() + "\n")
    elif ">" in args:
        command, filename = args.split(">", 1)
        with open(filename.strip(), "w") as file:
            file.write(command.strip() + "\n")
    else:
        print(args)

def cat(file):
    """Displays the contents of a file."""
    try:
        with open(file, "r", encoding="utf-8") as f:
            print(f.read())
    except FileNotFoundError:
        print(f"Error: File '{file}' not found.")
    except UnicodeDecodeError:
        print(f"Error: File '{file}' contains characters that cannot be decoded with UTF-8.")
    except Exception as e:
        print(f"Error: {e}")

def make_directory(directory):
    """Creates a new directory."""
    try:
        os.makedirs(directory)
        print(f"Directory '{directory}' created.")
    except FileExistsError:
        print(f"Error: Directory '{directory}' already exists.")
    except Exception as e:
        print(f"Error: {e}")

def remove(path, recursive=False, force=False):
    """Removes a file or directory."""
    try:
        if os.path.isdir(path) and recursive:
            shutil.rmtree(path)
            print(f"Directory '{path}' removed recursively.")
        elif os.path.isdir(path):
            os.rmdir(path)
            print(f"Directory '{path}' removed.")
        else:
            os.remove(path)
            print(f"File '{path}' removed.")
    except FileNotFoundError:
        if not force:
            print(f"Error: '{path}' not found.")
    except Exception as e:
        if not force:
            print(f"Error: {e}")

def parse_rm_command(args):
    """Parses the rm command arguments to handle options."""
    import shlex
    parser = argparse.ArgumentParser(prog='rm', add_help=False)
    parser.add_argument('-r', '--recursive', action='store_true', help='remove directories and their contents recursively')
    parser.add_argument('-f', '--force', action='store_true', help='ignore nonexistent files and arguments, never prompt')
    parser.add_argument('path', nargs='+', help='file or directory to remove')

    args = parser.parse_args(shlex.split(args))
    for path in args.path:
        remove(path, recursive=args.recursive, force=args.force)
        
def execute_script_file(script_file):
    try:
        with open(script_file, 'r') as f:
            commands = f.readlines()
            for command in commands:
                execute_command(command.strip())
    except FileNotFoundError:
        print(f"Error: File '{script_file}' not found.")
    except Exception as e:
        print(f"Error: {e}")
        
        
############################################################
######################## Modules ###########################
############################################################

def main(script_file=None):
    print("Welcome to the Python Multitool CLI. Type 'help' to see available commands.")
    
    if script_file:
        execute_script_file(script_file)
        return

    while True:
        # Get the username, hostname, and current path
        username = os.getlogin()
        hostname = socket.gethostname()
        current_path = os.getcwd()

        print(f"\033[97m╔══(\033[92m{username}\033[0m@\033[95m{hostname}\033[0m)-[\033[91m{current_path}\033[0m]\033[0m\n\033[97m╚══>\033[0m ", end="")

        user_input = input().strip()

        if not user_input:
            continue

        if user_input.lower() == "help":
            list_commands()
        elif user_input.lower() == "exit":
            print("Exiting...")
            break
        elif user_input.lower() == "clear":
            clear_screen()
        elif user_input.lower() == "version":
            display_version()
        elif user_input.lower() == "ver":
            display_version()
        elif user_input.lower() == "time":
            display_time()
        elif user_input.lower().startswith("ls"):
            directory = user_input.split(" ", 1)[-1].strip() if len(user_input.split(" ", 1)) > 1 else "."
            list_directory(directory)
        elif user_input.lower().startswith("cd"):
            directory = user_input.split(" ", 1)[-1].strip() if len(user_input.split(" ", 1)) > 1 else "."
            change_directory(directory)
        elif user_input.lower().startswith("echo"):
            echo(user_input.split(" ", 1)[-1].strip() if len(user_input.split(" ", 1)) > 1 else "")
        elif user_input.lower().startswith("cat"):
            file = user_input.split(" ", 1)[-1].strip()
            cat(file)
        elif user_input.lower().startswith("mkdir"):
            directory = user_input.split(" ", 1)[-1].strip()
            make_directory(directory)
        elif user_input.lower().startswith("rm"):
            args = user_input.split(" ", 1)[-1].strip()
            parse_rm_command(args)
        else:
            execute_command(user_input)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()