# Directory File Lister 📂

This Python script allows you to select a directory using a graphical user interface (GUI) and lists all the files in that directory (excluding subdirectories). The file names are printed to the console.

## How It Works 🛠️

1. **Imports**:
   - The script imports the necessary modules: `os` for interacting with the operating system and `tkinter` for creating the GUI.

2. **list_files_in_directory Function**:
   - This function takes a directory path as an argument.
   - It lists all files in the given directory (excluding subdirectories) and prints their names.
   - If an error occurs, it prints an error message.

3. **choose_directory Function**:
   - This function creates a hidden `tkinter` root window.
   - It opens a directory chooser dialog for the user to select a directory.
   - If a directory is selected, it calls the `list_files_in_directory` function with the chosen directory.

4. **Main Execution**:
   - When the script is run directly, it calls the `choose_directory` function to start the process.

## Usage 🚀

1. Run the script:
   ```bash
   python copy.py
   ```

2. A directory chooser dialog will appear. Select the directory you want to list the files from.

3. The script will print the names of all files in the selected directory to the console.

## Example Output 📋

```
file1.txt
file2.jpg
file3.pdf
...
```

## Requirements 📦

- Python 3.x
- 

tkinter

 library (usually included with Python installations)

## Notes 📝

- The script does not list files in subdirectories.
- If an error occurs (e.g., the directory does not exist), an error message will be printed.

Enjoy using the Directory File Lister! 🎉