import os
import sys
import shutil
import datetime
import tkinter as tk
from tkinter import filedialog, StringVar, PhotoImage
from tkinter import ttk
import tkinterdnd2 as tkdnd  # You'll need to install this package for drag and drop

# Constants
SORTED_PARENT_FOLDER = "Sorted"
KEYWORDS_FILE = "keywords (place your keywords here).txt"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load keywords from file
def load_keywords():
    keywords = {}
    keywords_path = os.path.join(SCRIPT_DIR, KEYWORDS_FILE)
    if os.path.exists(keywords_path):
        with open(keywords_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("Insert") or "DESIRED KEYWORDS" in line:
                    continue
                
                if ":" in line:
                    parts = line.split(":", 1)
                    if len(parts) == 2:
                        keys, folder = parts[0].strip(), parts[1].strip()
                        for key in keys.split("/"):
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
    sorted_folder = os.path.join(input_folder, get_sorted_folder())
    ensure_folder(sorted_folder)
    
    # Update status
    status_var.set(f"Sorting files from: {input_folder}")
    root.update()
    
    files_moved = 0
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        if os.path.isfile(file_path):
            # Skip hidden files and the script itself
            if filename.startswith('.') or filename == os.path.basename(__file__):
                continue
                
            parts = filename.split(" ", 1)
            if len(parts) > 1:
                keyword, _ = parts[0].lower(), parts[1]
                dest_folder = keywords.get(keyword, "Unsorted")
            else:
                dest_folder = "Unsorted"

            dest_path = os.path.join(sorted_folder, dest_folder)
            ensure_folder(dest_path)
            shutil.move(file_path, os.path.join(dest_path, filename))
            files_moved += 1
            print(f"Moved: {filename} -> {dest_folder}")
    
    status_var.set(f"Completed! {files_moved} files sorted to {sorted_folder}")
    path_var.set("")
    
    # Change status label color to indicate success
    status_label.configure(foreground="#008800")
    root.after(3000, lambda: status_label.configure(foreground="#000000"))

# GUI functions
def open_folder_dialog():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        path_var.set(folder_selected)
        sort_files(folder_selected)

def drop_inside_listbox(event):
    data = event.data
    
    # Remove curly braces if they exist (Windows adds them)
    if data.startswith("{") and data.endswith("}"):
        data = data[1:-1]
    
    # Check if it's a directory
    if os.path.isdir(data):
        path_var.set(data)
        sort_files(data)
    else:
        status_var.set("Please drop a folder, not a file")
        status_label.configure(foreground="#cc0000")
        root.after(3000, lambda: status_label.configure(foreground="#000000"))

# Create icon file for the application
def create_icon():
    icon_data = """
    R0lGODlhIAAgAPcAAAAAAP///4eHh8PDw8rKyr6+vsbGxs3NzdLS0tTU1NnZ2dvb297e3uLi4uXl
    5enp6ezs7O7u7vDw8PLy8vX19fb29vj4+Pr6+vz8/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAAAAAAAAAAAAAAACH5BAEAAAAALAAAAAAgACAAAAj/AAEIHEiwoMGDCBMqdNAAosOHECNKRFjL
    lkaJGDNqHDiRo8ePBAuCHEnS4IOSKFOeTKmypcuXCFfCnAkTJs2aOHMWtKmzp0+BPoMKfUm0qNGC
    SJMqvchUacOmUKM2FTgVK1GiVrNq1XoVYFevYMOKPVQoq9mzaNOiHXu2rVu0hQiyXcsPg9y7ePEe
    2su3r1+/gAMXukC44ODAEu0qRryYAuPHkCNLnjxZ8lXKBGnNM6CZs2cXnkOLFk36sgvTqFObYJGg
    w4QJFWLLjvDhw+wIESJIqC0BAgQHgQXo3p1gt/HWyJMXJwFiwvPo0qfPpk69Og0UAywweBCh/EGE
    8BCgS8ee/bv37N69k9doQIAAyxIgmL8gP/59+/TJq1evPr/79e3Tf+DQwYOHgQQWaOCBCCZIoEET
    OFdBBRZccOGFGGKoYYcdgvihiCGSWKKJJ6KYYoorvijRBRlooEEGHHzAZZdgikkmmmuy+SacctJZ
    p5134qnnnnz26aeDPvzAQw898LCDoYcimqiijDaqqKSUVmrpPZZeiummmXLa6acKhXDCCSikoKqq
    rLbq6quwxioQDTTcgEMOO2iq67TVOlQQQAA1VBBEEFVU0UYbefTRSCWdhFJKK7XU0ksxzVRTTjv1
    9FNQQxV1VFJLNfXU0QoAADs=
    """
    icon_file = os.path.join(SCRIPT_DIR, "sortomatic_icon.gif")
    with open(icon_file, 'wb') as f:
        import base64
        f.write(base64.b64decode(icon_data.replace('\n', '').replace(' ', '')))
    return icon_file

# Create double-clickable app file for macOS
def create_mac_app():
    app_script = os.path.join(SCRIPT_DIR, "Sortomatic.command")
    with open(app_script, "w") as f:
        f.write(f"""#!/bin/bash
cd "{SCRIPT_DIR}"
python3 "{os.path.basename(__file__)}"
""")
    os.chmod(app_script, 0o755)  # Make executable
    return app_script

# Create Windows shortcut
def create_windows_shortcut():
    shortcut_path = os.path.join(SCRIPT_DIR, "Sortomatic.bat")
    with open(shortcut_path, "w") as f:
        f.write(f'@echo off\ncd /d "{SCRIPT_DIR}"\npython "{os.path.basename(__file__)}"\npause')
    return shortcut_path

# Create launcher files based on platform
def create_launchers():
    if sys.platform == "darwin":  # macOS
        return create_mac_app()
    elif sys.platform == "win32":  # Windows
        return create_windows_shortcut()
    return None

# Create GUI with modern aesthetic
def create_gui():
    global root, path_var, status_var, status_label
    
    # Use TkinterDnD instead of regular Tkinter
    root = tkdnd.Tk()
    root.title("Sortomatic")
    root.geometry("600x400")
    
    # Set icon
    icon_path = create_icon()
    if os.path.exists(icon_path):
        icon = PhotoImage(file=icon_path)
        root.iconphoto(True, icon)
    
    # Create theme colors
    bg_color = "#f5f5f7"           # Light background
    accent_color = "#0071e3"       # Blue accent
    text_color = "#1d1d1f"         # Almost black text
    secondary_text = "#86868b"     # Gray text
    
    # Apply theme
    root.configure(bg=bg_color)
    style = ttk.Style()
    style.configure("TFrame", background=bg_color)
    style.configure("TLabel", background=bg_color, foreground=text_color)
    style.configure("Header.TLabel", background=bg_color, foreground=text_color, font=("Helvetica", 24, "bold"))
    style.configure("Subheader.TLabel", background=bg_color, foreground=secondary_text, font=("Helvetica", 14))
    style.configure("Status.TLabel", background=bg_color, foreground=secondary_text, font=("Helvetica", 12))
    
    # Button style
    style.configure("Accent.TButton", 
                    background=accent_color, 
                    foreground="white", 
                    font=("Helvetica", 12, "bold"))
    
    # Variables for displaying information
    path_var = StringVar()
    status_var = StringVar()
    status_var.set(f"Ready. Using keywords from: {KEYWORDS_FILE}")
    
    # Create main frame with padding
    main_frame = ttk.Frame(root, padding="30", style="TFrame")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # App logo/header - replace with your logo if you have one
    header_label = ttk.Label(
        main_frame, 
        text="Sortomatic", 
        style="Header.TLabel"
    )
    header_label.pack(pady=(0, 5), anchor="w")
    
    subheader_label = ttk.Label(
        main_frame,
        text="File sorting made simple",
        style="Subheader.TLabel"
    )
    subheader_label.pack(pady=(0, 20), anchor="w")
    
    # Separator
    separator = ttk.Separator(main_frame, orient="horizontal")
    separator.pack(fill="x", pady=10)
    
    # Instructions
    instruction_label = ttk.Label(
        main_frame,
        text="Drag and drop a folder to sort files by keyword",
        style="TLabel"
    )
    instruction_label.pack(pady=(10, 15), anchor="w")
    
    # Create a styled drop area
    drop_frame = ttk.Frame(main_frame)
    drop_frame.pack(fill=tk.X, pady=5, ipady=20)
    
    # Style for the drop area
    drop_frame_inner = tk.Frame(
        drop_frame, 
        bg="white", 
        highlightbackground="#e0e0e0", 
        highlightthickness=2,
        bd=0
    )
    drop_frame_inner.pack(fill=tk.X, ipady=25)
    
    # Drop area label
    drop_label = tk.Label(
        drop_frame_inner, 
        textvariable=path_var,
        bg="white",
        fg=text_color,
        font=("Helvetica", 12)
    )
    drop_label.pack(pady=5)
    
    # Drop zone hint
    drop_hint = tk.Label(
        drop_frame_inner,
        text="Drop folder here",
        bg="white",
        fg=secondary_text,
        font=("Helvetica", 12, "italic")
    )
    drop_hint.pack()
    
    # Make the frame and labels accept drops
    drop_frame_inner.drop_target_register(tkdnd.DND_FILES)
    drop_frame_inner.dnd_bind('<<Drop>>', drop_inside_listbox)
    drop_label.drop_target_register(tkdnd.DND_FILES)
    drop_label.dnd_bind('<<Drop>>', drop_inside_listbox)
    drop_hint.drop_target_register(tkdnd.DND_FILES)
    drop_hint.dnd_bind('<<Drop>>', drop_inside_listbox)
    
    # Browse button with custom style
    button_frame = ttk.Frame(main_frame, style="TFrame")
    button_frame.pack(fill="x", pady=15)
    
    browse_button = tk.Button(
        button_frame, 
        text="Browse Folder", 
        command=open_folder_dialog,
        bg=accent_color,
        fg="white",
        font=("Helvetica", 12, "bold"),
        padx=15,
        pady=8,
        bd=0,
        highlightthickness=0,
        activebackground="#0062c3",
        activeforeground="white",
        cursor="hand2"
    )
    browse_button.pack(side="left")
    
    # Status label
    status_label = ttk.Label(
        main_frame, 
        textvariable=status_var,
        style="Status.TLabel"
    )
    status_label.pack(pady=(20, 0), anchor="w")
    
    # Create launcher files
    create_launchers()
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()