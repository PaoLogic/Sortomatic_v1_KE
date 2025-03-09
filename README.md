# Sortomatic v1 (Keyword Edition)

## Overview
Sortomatic is a Python-based file sorter that organizes files into folders based on predefined keywords. It supports both command-line and macOS GUI interaction.

## Features
- Automatically sorts files based on keywords.
- Creates timestamped "Sorted" folders (e.g., `Sorted 8-3-2025 (15:00)`).
- Allows drag-and-drop GUI sorting for macOS users.
- Can process new files and update the last used sorted folder dynamically.

## Installation
1. Ensure Python is installed (version 3.7+ recommended).
2. Clone or download this repository.
3. Install dependencies (if needed):
   ```sh
   pip install -r requirements.txt
   ```

## Usage
### **Command-Line Mode**
Run the script via terminal:
```sh
python sortomatic.py
```
Then enter the folder path to sort.

### **GUI Mode (macOS)**
Run the GUI version:
```sh
python sortomatic_gui.py
```
Click "Browse Folder" to select a directory for sorting.

## Keywords File (`keywords.txt`)
The program uses a `keywords.txt` file to map file prefixes to destination folders.

Example:
```
invoice/bill: Finances
report/summary: Work Documents
photo/image: Pictures
```
Files starting with these keywords will be moved accordingly.

## Future Improvements
- Windows GUI version
- Background monitoring for auto-sorting

