# search.py

import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Module metadata
DESCRIPTION = "Search for files, folders, or text within files."
ARGS = ["<option>", "<keyword>", "[<optional path>]"]
ALIASES = ["find"]

def get_all_drives():
    from string import ascii_uppercase
    drives = [f"{drive}:/" for drive in ascii_uppercase if os.path.exists(f"{drive}:/")]
    return drives

def search_file(file_name, path):
    found_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file_name.lower() == file.lower():
                found_files.append(os.path.join(root, file))
    return found_files

def search_text(text, path):
    found_files = {}
    text_lower = text.lower()
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line_number, line in enumerate(f, 1):
                        column_number = line.lower().find(text_lower)
                        if column_number != -1:
                            if file_path not in found_files:
                                found_files[file_path] = []
                            found_files[file_path].append((line_number, column_number + 1))
            except Exception:
                pass
    return found_files

def search_folder(folder_name, path):
    found_folders = []
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if folder_name.lower() == dir.lower():
                found_folders.append(os.path.join(root, dir))
    return found_folders

def main(option, keyword, search_path=None):
    if not search_path:
        search_paths = get_all_drives()
    else:
        search_paths = [search_path]

    results = []
    with ThreadPoolExecutor() as executor:
        futures = []
        for path in search_paths:
            if option == '-f':
                futures.append(executor.submit(search_file, keyword, path))
            elif option == '-t':
                futures.append(executor.submit(search_text, keyword, path))
            elif option == '-ft':
                futures.append(executor.submit(search_folder, keyword, path))
            else:
                print("Invalid option. Please use -f, -t, or -ft.")
                print_help()
                return

        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)

    if not results:
        print("The specified file, text, or folder was not found.")
    else:
        if option == '-t':
            for result_dict in results:
                for file_path, positions in result_dict.items():
                    abs_path = os.path.abspath(file_path)
                    # Print the directory path
                    directory_path = os.path.dirname(abs_path)
                    print(f"\033]8;;file://{directory_path}\a{abs_path}\033]8;;\a")
                    for line, column in positions:
                        print(f"    Line {line}, Column {column}")
        else:
            for sublist in results:
                for item in sublist:
                    abs_path = os.path.abspath(item)
                    # Print the directory path and file name
                    directory_path = os.path.dirname(abs_path)
                    print(f"\033]8;;file://{directory_path}\a{abs_path}\033]8;;\a")

def print_help():
    help_text = """
Usage: search <option> <file/folder/text string> [<optional path>]

Options:
  -f        Search for a file
  -t        Search for text inside files
  -ft       Search for a folder
  -h, --help  Display this help message
"""
    print(help_text)

# Test if this script is being run directly
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print_help()
    else:
        main(*sys.argv[1:])
