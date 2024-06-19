# Creating Addons for Quanta CLI

To create addons for the Quanta CLI, follow these steps:

## 1. Import Required Modules

At the beginning of your addon script, import any required modules. These could include standard Python modules or any additional libraries needed for your addon.

```python
import os
import datetime
```

## 2. Define Description and Arguments

Define a description and any arguments your addon function requires. This will help users understand what your addon does and how to use it.

```python
DESCRIPTION = "Example addon to demonstrate addon creation" # Lists description in help menu
ARGS = ["<arg1>", "<arg2>", "<arg3>"] # Lists arguments in help menu
```

If an module does not have arguments you can ignore the `ARGS` option.

```python
DESCRIPTION = "Example addon to demonstrate addon creation" # Lists description in help menu
```

## 3. Define the Main Function

Create the main function of your addon. This function will contain the code that performs the desired functionality of your addon. Make sure to use the arguments defined earlier if your addon requires any.

```python
def main(arg1, arg2, arg3): # your arguments in the code
    # Your addon code goes here
    print(f"Argument 1: {arg1}")
    print(f"Argument 2: {arg2}")
    print(f"Argument 3: {arg3}")
```

## 4. Save the Addon Script

Save your addon script with a meaningful name, preferably reflecting the functionality of the addon. For example, if your addon lists files in a directory, you could name it `list_files.py`.

## 5. Usage

To use your addon, place it in the `addons` directory within the Quanta CLI project. Then, when you run the Quanta CLI, your addon will be automatically detected and listed as an available command.

```
╔══(User@Computer)-[Current/Directory]
╚══> help

Available commands:
- example <arg1> <arg2> <arg3>: Example addon to demonstrate addon creation
- help: Display available commands and their descriptions
- clear: Clear the screen
- ...
```

## 6. Running the Addon

Once your addon is listed as an available command, users can run it by providing the required arguments.

```
╔══(User@Computer)-[Current/Directory]
╚══> example value1 value2 value3
Argument 1: value1
Argument 2: value2
Argument 3: value3
```

## Example Program

Here's an example addon program:

```python
import os

DESCRIPTION = "Example addon to demonstrate addon creation" # Lists description in help menu
ARGS = ["<arg1>", "<arg2>", "<arg3>"] # Lists arguments in help menu

def main(arg1, arg2, arg3): # your arguments in the code
    print(f"Argument 1: {arg1}")
    print(f"Argument 2: {arg2}")
    print(f"Argument 3: {arg3}")
```

This addon simply prints the provided arguments to the console.

---

## Advanced

If your arguments have multiple options, you can handle them as shown in this example:

```python
DESCRIPTION = "Display information based on page number"
ARGS = ["<page>"]

def main(page):
    if page == "1":
        print("Information for page 1")
    elif page == "2":
        print("Information for page 2")
    elif page == "3":
        print("Information for page 3")
    elif page == "4":
        print("Information for page 4")
    elif page == "5":
        print("Information for page 5")
    else:
        print("Invalid page number. Please provide a number between 1 and 5.")
```

---

## Adding Aliases

To add aliases to your addon command, include an `ALIASES` attribute in your script. This allows users to invoke your command using different names.

```python
import os

DESCRIPTION = "Example addon with aliases"
ARGS = ["<arg1>"]
ALIASES = ["example", "ex", "demo"]

def main(arg1):
    print(f"Argument 1: {arg1}")
```

With this setup, users can run your addon using any of the specified aliases:

```
╔══(User@Computer)-[Current/Directory]
╚══> example value
Argument 1: value

╔══(User@Computer)-[Current/Directory]
╚══> ex value
Argument 1: value

╔══(User@Computer)-[Current/Directory]
╚══> demo value
Argument 1: value
```

That's it! You've successfully created and used an addon for the Quanta CLI.