# convert_py_to_exe by Mr.Patchara Al-umaree ^^!

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os
import json

def install_pyinstaller():
    try:
        subprocess.run(['pip', 'install', 'pyinstaller'], check=True, capture_output=True)
        messagebox.showinfo("Success", "PyInstaller has been installed successfully. You can now convert Python files to executable.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred while installing PyInstaller:\n{e.stderr.decode('utf-8')}")

def check_and_install_pyinstaller():
    try:
        subprocess.run(['pyinstaller', '--version'], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        if messagebox.askyesno("PyInstaller Not Found", "PyInstaller is not installed. Do you want to install it now?"):
            install_pyinstaller()
        else:
            messagebox.showwarning("Warning", "PyInstaller is required to convert Python files to executable. Please install it manually using 'pip install pyinstaller'.")

def select_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("Python files", "*.py")])
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(0, ';'.join(file_paths))

def select_output_directory():
    dir_path = filedialog.askdirectory()
    entry_output_directory.delete(0, tk.END)
    entry_output_directory.insert(0, dir_path)

def select_icon_file():
    file_path = filedialog.askopenfilename(filetypes=[("Icon files", "*.ico")])
    entry_icon_path.delete(0, tk.END)
    entry_icon_path.insert(0, file_path)

def load_settings():
    if os.path.exists('settings.json'):
        with open('settings.json', 'r') as file:
            settings = json.load(file)
            entry_output_directory.insert(0, settings.get('output_directory', ''))
            entry_icon_path.insert(0, settings.get('icon_path', ''))
            var_onefile.set(settings.get('onefile', False))
            var_windowed.set(settings.get('windowed', False))

def save_settings():
    settings = {
        'output_directory': entry_output_directory.get(),
        'icon_path': entry_icon_path.get(),
        'onefile': var_onefile.get(),
        'windowed': var_windowed.get()
    }
    with open('settings.json', 'w') as file:
        json.dump(settings, file)

def reset_form():
    entry_file_path.delete(0, tk.END)
    entry_output_directory.delete(0, tk.END)
    entry_icon_path.delete(0, tk.END)
    var_onefile.set(False)
    var_windowed.set(False)
    output_text.delete(1.0, tk.END)

def convert_to_exe():
    check_and_install_pyinstaller()  # Check and install PyInstaller if not installed

    file_paths = entry_file_path.get().split(';')
    output_directory = entry_output_directory.get()
    icon_path = entry_icon_path.get()
    onefile = var_onefile.get()
    windowed = var_windowed.get()

    if not file_paths:
        messagebox.showwarning("Warning", "Please select Python files first.")
        return

    for file_path in file_paths:
        cmd = ['pyinstaller']
        
        if onefile:
            cmd.append('--onefile')
        
        if windowed:
            cmd.append('--windowed')
        
        if icon_path:
            cmd.extend(['--icon', icon_path])
        
        cmd.append(file_path)
        
        output_text.insert(tk.END, f"Starting conversion for {file_path}...\n")
        try:
            process = subprocess.run(cmd, check=True, capture_output=True, text=True)
            output_text.insert(tk.END, process.stdout)
            if output_directory:
                dist_path = os.path.join(os.getcwd(), 'dist')
                exe_file = os.path.basename(file_path).replace('.py', '.exe')
                os.replace(os.path.join(dist_path, exe_file), os.path.join(output_directory, exe_file))
            output_text.insert(tk.END, f"Conversion for {file_path} completed successfully!\n")
        except subprocess.CalledProcessError as e:
            output_text.insert(tk.END, e.output)
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Save settings and log after conversion
    save_settings()
    with open('conversion_log.txt', 'a') as log_file:
        log_file.write(output_text.get(1.0, tk.END))
    
    if output_directory:
        if messagebox.askyesno("Open File", "Do you want to open the output directory?"):
            os.startfile(output_directory)

def show_contact_info():
    contact_info = "Developer: Mr.Patchara Al-umaree \nEmail: Patcharaalumaree@gmail.com\nGitHub: https://github.com/MrPatchara\n\nThank you for using the application!"
    messagebox.showinfo("Contact Information", contact_info)

# Create the main window
root = tk.Tk()
root.title("Python to EXE Converter V1.0 by Mr.Patchara Al-umaree!")

# Create and place the widgets
label_file_path = tk.Label(root, text="Select Python files:")
label_file_path.pack(pady=5)

entry_file_path = tk.Entry(root, width=50)
entry_file_path.pack(pady=5)

button_browse = tk.Button(root, text="Browse", command=select_files)
button_browse.pack(pady=5)

label_output_directory = tk.Label(root, text="Select Output Directory:")
label_output_directory.pack(pady=5)

entry_output_directory = tk.Entry(root, width=50)
entry_output_directory.pack(pady=5)

button_browse_output = tk.Button(root, text="Browse", command=select_output_directory)
button_browse_output.pack(pady=5)

label_icon_path = tk.Label(root, text="Select Icon file (optional):")
label_icon_path.pack(pady=5)

entry_icon_path = tk.Entry(root, width=50)
entry_icon_path.pack(pady=5)

button_browse_icon = tk.Button(root, text="Browse", command=select_icon_file)
button_browse_icon.pack(pady=5)

var_onefile = tk.BooleanVar()
check_onefile = tk.Checkbutton(root, text="Create a single executable file (--onefile)", variable=var_onefile)
check_onefile.pack(pady=5)

var_windowed = tk.BooleanVar()
check_windowed = tk.Checkbutton(root, text="Disable console window (--windowed)", variable=var_windowed)
check_windowed.pack(pady=5)

button_convert = tk.Button(root, text="Convert to EXE", command=convert_to_exe)
button_convert.pack(pady=20)

output_text = scrolledtext.ScrolledText(root, width=60, height=10)
output_text.pack(pady=10)

button_contact = tk.Button(root, text="Contact Developer", command=show_contact_info)
button_contact.pack(pady=10)

button_reset = tk.Button(root, text="Reset", command=reset_form)
button_reset.pack(pady=10)

# Load settings on startup
load_settings()

# Save settings on close
root.protocol("WM_DELETE_WINDOW", lambda: (save_settings(), root.destroy()))

# Run the application
root.mainloop()
