import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

# Get the username from the command line arguments
username = sys.argv[1]

# Function to open the Manage Cargo window
def open_manage_cargo():
    # Add the code to create the Manage Cargo window here
    pass

# Function to open the Manage Packages window
def open_manage_packages():
    # Add the code to create the Manage Packages window here
    pass

# Function to open the Reports window
def open_reports():
    # Add the code to create the Reports window here
    pass

# Function to go back to the main login window (main.py)
def logout():
    admin_window.destroy()  # Close the admin window
    subprocess.run(["python", "main.py"])  # Return to main.py using subprocess

# Create the Admin GUI window
admin_window = tk.Tk()
admin_window.title("Quick Cargo | Admin Panel")

# Set window size
admin_window.geometry("400x300")  # Width x Height

# Create a frame for the header (top row)
header_frame = tk.Frame(admin_window)
header_frame.pack(side="top", fill="x")

# Display the username in the header frame (top left corner)
username_label = tk.Label(header_frame, text="Username: Admin")  # Replace "Admin" with actual username
username_label.pack(side="left", padx=10)

# Add a logout button to the header frame (top right corner)
logout_button = tk.Button(header_frame, text="Logout", command=logout)
logout_button.pack(side="right", padx=10)

# Create a frame for the content (center row)
content_frame = tk.Frame(admin_window)
content_frame.pack(side="top", fill="both", expand=True)

# Create buttons for different options in the content frame (center)
manage_cargo_button = tk.Button(content_frame, text="Manage Cargo", command=open_manage_cargo)
manage_cargo_button.pack(side="top", pady=10)

manage_packages_button = tk.Button(content_frame, text="Manage Packages", command=open_manage_packages)
manage_packages_button.pack(side="top", pady=10)

reports_button = tk.Button(content_frame, text="Reports", command=open_reports)
reports_button.pack(side="top", pady=10)

# Start the GUI event loop for the admin window
admin_window.mainloop()
