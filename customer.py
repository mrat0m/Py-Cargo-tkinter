import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

# Get the username from the command line arguments
username = sys.argv[1]

# Function to open the Book Cargo Service window
def book_cargo_service():
    # Add the code to open the Book Cargo Service window here
    pass

# Function to open the View Cargo Service window
def view_cargo_service():
    # Add the code to open the View Cargo Service window here
    pass

# Function to go back to the main login window (main.py)
def logout():
    customer_window.destroy()  # Close the customer window
    subprocess.run(["python", "main.py"])  # Return to main.py using subprocess

# Create the Customer GUI window
customer_window = tk.Tk()
customer_window.title("Quick Cargo | Customer Panel")

# Set window size
customer_window.geometry("400x300")  # Width x Height

# Create a frame for the header (top row)
header_frame = tk.Frame(customer_window)
header_frame.pack(side="top", fill="x")

# Display the username in the header frame (top left corner)
username_label = tk.Label(header_frame, text="Username: " + username)
username_label.pack(side="left", padx=10)

# Add a logout button to the header frame (top right corner)
logout_button = tk.Button(header_frame, text="Logout", command=logout)
logout_button.pack(side="right", padx=10)

# Create a frame for the content (center row)
content_frame = tk.Frame(customer_window)
content_frame.pack(side="top", fill="both", expand=True)

# Create buttons for different options in the content frame (center)
book_cargo_button = tk.Button(content_frame, text="Book Cargo Service", command=book_cargo_service)
book_cargo_button.pack(side="top", pady=10)

view_cargo_button = tk.Button(content_frame, text="View Cargo Service", command=view_cargo_service)
view_cargo_button.pack(side="top", pady=10)

# Start the GUI event loop for the customer window
customer_window.mainloop()