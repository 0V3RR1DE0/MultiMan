# Example Addon

DESCRIPTION = "Lists Files in a directory."
ARGS = ["<path>"]

import os  # Import the os module for interacting with the operating system

def main(path):  # Define the main function that takes a path as an argument
    try:
        # List all files in the given directory path
        # Use a list comprehension to filter out directories
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        
        if files:  # Check if there are any files in the list
            print(f"Files in directory '{path}':")  # Print the directory path
            for file in files:  # Iterate over the list of files
                print(f"  {file}")  # Print each file name with indentation
        else:  # If the files list is empty
            print(f"No files found in directory '{path}'.")  # Inform the user that no files were found
    except FileNotFoundError:  # Handle the case where the directory does not exist
        print(f"Error: Directory '{path}' not found.")  # Print an error message for a non-existent directory
    except Exception as e:  # Handle any other exceptions that might occur
        print(f"Error: {e}")  # Print a generic error message with the exception details
