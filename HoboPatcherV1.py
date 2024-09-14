import tkinter as tk
from tkinter import filedialog, messagebox
import os
import ctypes

# Function to check if the script is running with admin rights
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Function to patch the game executable
def patch_exe(file_path):
    try:
        # Read the contents of the file
        with open(file_path, 'rb') as f:
            data = f.read()

        # Search for the width (1920 in little-endian format: 07 80)
        original_width = b'\x07\x80'
        new_width = b'\x70\x0D'

        # Search for the height (1080 in little-endian format: 04 38)
        original_height = b'\x04\x38'
        new_height = b'\xA0\x05'

        # Check if the width exists in the file
        if original_width in data:
            # Replace the width
            data = data.replace(original_width, new_width)
        else:
            return False, "Width value not found"

        # Check if the height exists in the file
        if original_height in data:
            # Replace the height
            data = data.replace(original_height, new_height)
        else:
            return False, "Height value not found"

        # Write the patched content back to the file
        with open(file_path, 'wb') as f:
            f.write(data)

        return True, "Patching Successful"
    except Exception as e:
        print(f"Error patching the file: {e}")
        return False, f"Error: {e}"

# Function to check if the file is located in Program Files directories
def is_in_protected_directory(file_path):
    program_files = os.environ.get("ProgramFiles", "C:\\Program Files")
    program_files_x86 = os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")
    return file_path.startswith(program_files) or file_path.startswith(program_files_x86)

# Function to handle the patch button click
def patch_file():
    file_path = file_entry.get()
    
    if not os.path.isfile(file_path):
        messagebox.showerror("Error", "Invalid file path. Please select a valid executable.")
        return
    
    # Check if the selected file is "HoboRPG.exe"
    if not file_path.endswith("HoboRPG.exe"):
        messagebox.showerror("Error", "Only HoboRPG.exe can be patched.")
        return

    # Check if the file is in a protected directory like Program Files
    if is_in_protected_directory(file_path) and not is_admin():
        messagebox.showerror("Admin Rights Required", 
                             "As this is in the Steam directory, admin privileges are required to modify this file. "
                             "Please run the script as an administrator.")
        return
    
    success, message = patch_exe(file_path)
    
    if success:
        status_label.config(text=message, fg="green")
    else:
        status_label.config(text=message, fg="red")

# Function to open the file dialog and set the file path
def browse_file():
    file_path = filedialog.askopenfilename(title="Open Game EXE", filetypes=[("Executable files", "*.exe")])
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

# Initialize the GUI window
root = tk.Tk()
root.title("HoboUltraPatcherV1 - By MarcelMedia")

# Set window size to make it wider
root.geometry("450x180")  # Set the window width to 600 pixels and height to 300 pixels

# Create the widgets
file_label = tk.Label(root, text="Select Game EXE:")
file_label.pack(pady=10)

file_entry = tk.Entry(root, width=50)
file_entry.pack(padx=10)

browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack(pady=5)

patch_button = tk.Button(root, text="Patch", command=patch_file)
patch_button.pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
