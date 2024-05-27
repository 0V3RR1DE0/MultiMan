# Example Addon

import datetime

DESCRIPTION = "Greet the user and calculate their age"
ARGS = ["<first name>", "<last name>", "<birthyear>"]

def main(first_name, last_name, birthyear):
    current_year = datetime.datetime.now().year
    age = current_year - int(birthyear)
    print(f"Hello {first_name} {last_name}, you're {age} years old :D")
