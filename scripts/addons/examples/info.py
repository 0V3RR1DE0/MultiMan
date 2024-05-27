# Example Addon

DESCRIPTION = "Display information based on page number"
ARGS = ["<page>"]
ALIASES = ["info", "details"]

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
