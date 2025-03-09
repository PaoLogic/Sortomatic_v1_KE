import os
import shutil
import datetime
import tkinter as tk
from tkinter import filedialog

# Constants
SORTED_PARENT_FOLDER = "Sorted"
KEYWORDS_FILE = "keywords (place your keywords here).txt"  # Updated filename to match your file

# Load keywords from file
def load_keywords():
    keywords = {}
    if os.path.exists(KEYWORDS_FILE):
        with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("Insert") or "DESIRED KEYWORDS" in line:  # Skip instruction lines
                    continue
                
                if ":" in line:  # Check if this is a keyword definition line
                    parts = line.split(":", 1)  # Split by first colon
                    if len(parts) == 2:
                        keys, folder = parts[0].strip(), parts[1].strip()
                        for key in keys.split("/"):  # Handle multiple keywords separated by "/"
                            keywords[key.strip().lower()] = folder
    return keywords

# Generate sorted folder name
def get_sorted_folder():
    now = datetime.datetime.now()
    return f"{SORTED_PARENT_FOLDER} {now.day}-{now.month}-{now.year} ({now.hour}:00)"

# Ensure folder exists
def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Sort files
def sort_files(input_folder):
    keywords = load_keywords()
    sorted_folder = get_sorted_folder()
    ensure_folder(sorted_folder)
    
    # Print loaded keywords for debugging
    print("Loaded keywords:")
    for k, v in keywords.items():
        print(f"  '{k}' -> '{v}'")
    
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        if os.path.isfile(file_path):
            parts = filename.split(" ", 1)  # Split by first space
            if len(parts) > 1:
                keyword, _ = parts[0].lower(), parts[1]
                dest_folder = keywords.get(keyword, "Unsorted")
            else:
                dest_folder = "Unsorted"

            dest_path = os.path.join(sorted_folder, dest_folder)
            ensure_folder(dest_path)
            shutil.move(file_path, os.path.join(dest_path, filename))
            print(f"Moved: {filename} -> {dest_folder}")

# GUI Application
def open_folder_dialog():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        sort_files(folder_selected)

# Create GUI for macOS
def create_gui():
    root = tk.Tk()
    root.title("Sortomatic v1 (Keyword Edition)")
    root.geometry("400x200")
    
    label = tk.Label(root, text="Drag and drop files or browse", font=("Arial", 12))
    label.pack(pady=10)
    
    browse_button = tk.Button(root, text="Browse Folder", command=open_folder_dialog)
    browse_button.pack(pady=10)
    
    # Add status label
    status_label = tk.Label(root, text=f"Keywords file: {KEYWORDS_FILE}", font=("Arial", 10))
    status_label.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()