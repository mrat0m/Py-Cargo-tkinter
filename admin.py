import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

# Get the username from the command line arguments
username = sys.argv[1]

# Function to open the Manage Packages window
def manage_packages():
    messagebox.showinfo("Action Successful", "Redirecting to packages page")
    admin_window.destroy()  # Close the admin window
    subprocess.run(["python", "packages.py", username])  # Run packages.py using subprocess

# Function to open the Manage Cargo window
def manage_cargo():
    admin_window.destroy()  # Close the admin window
    subprocess.run(["python", "managecargo.py", username])  # Run managecargo.py using subprocess

# Function to open the all bookings window
def view_all_bookings():
    messagebox.showinfo("Action Successful", "Redirecting to allbookings page")
    admin_window.destroy()  # Close the admin window
    subprocess.run(["python", "allbookings.py", username])  # Run allbookings.py using subprocess

# Function to go back to the main login window (main.py)
def logout():
    admin_window.destroy()  # Close the admin window
    subprocess.run(["python", "main.py"])  # Return to main.py using subprocess

# Create the Admin GUI window
admin_window = tk.Tk()
admin_window.title("Quick Cargo | Admin Panel")

# Set window size
admin_window.geometry("400x300")  # Width x Height

# Add a stylish heading
heading_label = tk.Label(admin_window, text="Quick Cargo",
                         font=("Helvetica", 20, "bold"))
heading_label.pack(pady=15)

# Create a frame for the header (top row)
header_frame = tk.Frame(admin_window)
header_frame.pack(side="top", fill="x")

# Display the username in the header frame (top left corner)
username_label = tk.Label(header_frame, text=f"Username: {username}")
username_label.pack(side="left", padx=10)

# Add a logout button to the header frame (top right corner)
logout_button = tk.Button(header_frame, text="Logout", command=logout)
logout_button.pack(side="right", padx=10)

# Create a frame for the content (center row)
content_frame = tk.Frame(admin_window)
content_frame.pack(side="top", fill="both", expand=True)

# Create buttons for different options in the content frame (center)
manage_packages_button = tk.Button(
    content_frame, text="Manage Packages", command=manage_packages)
manage_packages_button.pack(side="top", pady=10)

manage_cargo_button = tk.Button(
    content_frame, text="Manage Cargo", command=manage_cargo)
manage_cargo_button.pack(side="top", pady=10)

reports_button = tk.Button(
    content_frame, text="All Bookings", command=view_all_bookings)
reports_button.pack(side="top", pady=10)

# Start the GUI event loop for the admin window
admin_window.mainloop()
