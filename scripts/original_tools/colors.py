# colors.py

DESCRIPTION = "Prints ANSI color codes for text and background colors."

def print_color_codes():
    """Prints ANSI escape codes for different text and background colors."""
    # Foreground colors
    print("Foreground colors:")
    for i in range(30, 38):
        print(f"Color {i}: \033[{i}mExample Text\033[0m (\033[{i}m\\033[{i}m\033[0m)")

    # Background colors
    print("\nBackground colors:")
    for i in range(40, 48):
        print(f"Color {i}: \033[30;{i}mExample Text\033[0m (\033[30;{i}m\\033[30;{i}m\033[0m)")

    # Bright foreground colors
    print("\nBright foreground colors:")
    for i in range(90, 98):
        print(f"Color {i}: \033[{i}mExample Text\033[0m (\033[{i}m\\033[{i}m\033[0m)")

    # Bright background colors
    print("\nBright background colors:")
    for i in range(100, 108):
        print(f"Color {i}: \033[30;{i}mExample Text\033[0m (\033[30;{i}m\\033[30;{i}m\033[0m)")

    # Styles
    print("\nStyles:")
    print("Bold: \033[1mExample Text\033[0m (\033[1m\\033[1m\033[0m)")
    print("Italic: \033[3mExample Text\033[0m (\033[3m\\033[3m\033[0m)")
    print("Underline: \033[4mExample Text\033[0m (\033[4m\\033[4m\033[0m)")
    print("Blink: \033[5mExample Text\033[0m (\033[5m\\033[5m\033[0m)")
    print("Inverse: \033[7mExample Text\033[0m (\033[7m\\033[7m\033[0m)")
    print("Strikethrough: \033[9mExample Text\033[0m (\033[9m\\033[9m\033[0m)")

    # Reset
    print("\nReset:")
    print("Reset: \033[0mExample Text\033[0m (\033[0m\\033[0m\033[0m)")

def main():
    """Entry point of the colors module."""
    print("ANSI color codes:")
    print_color_codes()

if __name__ == "__main__":
    main()
