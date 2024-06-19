import sys
import os

if len(sys.argv) > 1:
    script_file = sys.argv[1]
    python_script = "quanta-cli.py"  # Assuming both scripts are in the same directory
    os.system(f"python {python_script} {script_file}")
else:
    print("Error: No script file provided.")
    sys.exit(1)
