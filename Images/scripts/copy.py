import os
import tkinter as tk
from tkinter import filedialog

def list_files_in_directory(directory):
    try:
        # List all files in the given directory without reading subdirectories
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        for file in files:
            print(file)
    except Exception as e:
        print(f"Error: {e}")

def choose_directory():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    directory = filedialog.askdirectory()  # Open the directory chooser dialog
    if directory:
        list_files_in_directory(directory)

if __name__ == "__main__":
    choose_directory()