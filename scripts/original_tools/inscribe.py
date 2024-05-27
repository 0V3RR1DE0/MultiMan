import curses
import os
import time

DESCRIPTION = "Open a file in the inscribe text editor"
ARGS = ["<file>"]

def main(file_path):
    curses.wrapper(start_editor, file_path)

def start_editor(stdscr, file_path):
    
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # White text on black background
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Black text on white background
    
    
    curses.curs_set(1)
    stdscr.keypad(True)
    curses.noecho()
    

    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()
    else:
        lines = [""]

    y, x = 0, 0
    max_y, max_x = stdscr.getmaxyx()
    top_line = 0
    has_changes = False

    while True:
        stdscr.clear()
        for idx, line in enumerate(lines[top_line:top_line + max_y - 1]):
            stdscr.addstr(idx + 1, 0, line.rstrip())

        # Calculate center position for the banner
        banner_text = f"Inscribe - Editing {file_path}"
        banner_padding = " " * ((max_x - len(banner_text)) // 2)
        banner = f"{banner_padding}{banner_text}{banner_padding}"
        stdscr.addstr(0, 0, banner, curses.color_pair(2) | curses.A_BOLD)  # Use color pair 2 for banner



        stdscr.move(y + 1, x)
        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP:
            if y > 0:
                y -= 1
            elif top_line > 0:
                top_line -= 1
        elif key == curses.KEY_DOWN:
            if y < max_y - 2 and y + top_line < len(lines) - 1:
                y += 1
            elif top_line + y < len(lines) - 1:
                top_line += 1
        elif key == curses.KEY_LEFT:
            if x > 0:
                x -= 1
        elif key == curses.KEY_RIGHT:
            if x < max_x - 1 and x < len(lines[y + top_line]) - 1:
                x += 1
        elif key == 10 or key == 13:  # Enter key
            lines.insert(y + top_line + 1, "")
            if y < max_y - 2:
                y += 1
            else:
                top_line += 1
            x = 0
            has_changes = True
        elif key == 9:  # Tab key
            lines[y + top_line] = lines[y + top_line][:x] + " " * 4 + lines[y + top_line][x:]
            x += 4
            has_changes = True
        elif key == 24:  # Ctrl + X
            if has_changes:
                stdscr.addstr(max_y - 1, 0, "Save changes before exiting? (Y/N)")
                stdscr.refresh()
                choice = stdscr.getch()
                if choice == ord('Y') or choice == ord('y'):
                    with open(file_path, 'w') as f:
                        f.writelines(line.rstrip('\r\n') + '\n' for line in lines)
                    break
                else:
                    break
            else:
                break
        elif key == 19:  # Ctrl + S
            with open(file_path, 'w') as f:
                f.writelines(line.rstrip('\r\n') + '\n' for line in lines)
            lines_with_text = sum(1 for line in lines if line.strip())  # Count non-empty lines
            save_msg = f"Wrote {lines_with_text} lines with text"
            stdscr.addstr(max_y - 1, max_x // 2 - len(save_msg) // 2, save_msg, curses.color_pair(2) | curses.A_BOLD)  # Use color pair 2 for message
            stdscr.refresh()
            time.sleep(1)  # Wait for 1 second
            stdscr.addstr(max_y - 1, max_x // 2 - len(save_msg) // 2, " " * len(save_msg))
            stdscr.refresh()
            has_changes = False
        elif key == 8 or key == 127:  # Backspace
            if x > 0:
                lines[y + top_line] = lines[y + top_line][:x-1] + lines[y + top_line][x:]
                x -= 1
                has_changes = True
            elif y > 0:
                prev_len = len(lines[y + top_line - 1])
                lines[y + top_line - 1] += lines[y + top_line]
                lines.pop(y + top_line)
                if y < max_y - 2:
                    y -= 1
                else:
                    top_line -= 1
                x = prev_len
                has_changes = True
        else:
            if 32 <= key <= 126:  # Printable characters
                lines[y + top_line] = lines[y + top_line][:x] + chr(key) + lines[y + top_line][x:]
                x += 1
                has_changes = True

    curses.curs_set(0)
    stdscr.keypad(False)
    curses.echo()