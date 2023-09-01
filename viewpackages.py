import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import dbconnect  # Import your dbconnect.py module

# Get the username from the command line arguments
username = sys.argv[1]

# Function to open the Manage Cargo window
def manage_cargo():
    messagebox.showinfo("Action Successful", "Redirecting to managecargo page")
    view_packages_window.destroy()  # Close the packages window
    subprocess.run(["python", "managecargo.py", username])  # Run managecargo.py using subprocess

# Function to open the all bookings window
def all_bookings():
    messagebox.showinfo("Action Successful", "Redirecting to allbookings page")
    view_packages_window.destroy()  # Close the packages window
    subprocess.run(["python", "allbookings.py", username])  # Run allbookings.py using subprocess

# Function to go back to the admin window
def back_to_admin():
    view_packages_window.destroy()  # Close the packages window
    subprocess.run(["python", "admin.py", username])  # Return to admin.py using subprocess

# Function to log out and return to the main window
def logout():
    view_packages_window.destroy()  # Close the packages window
    subprocess.run(["python", "main.py"])  # Return to main.py using subprocess

def add_package():
    view_packages_window.destroy()  # Close the packages window
    subprocess.run(["python", "packages.py", username])  # Open packages.py using subprocess

# Function to add a View packages from the database
def view_packages():
    q = "SELECT * FROM packages"
    res = dbconnect.select(q, ())  # Pass an empty tuple as values
    
    if res:
        # Create a Treeview widget
        tree = tk.ttk.Treeview(view_packages_window)
        tree.pack(pady=10)
        
        # Define columns and headings
        tree["columns"] = ("packname", "maximum_weight", "maximum_height", "maximum_width", "minimum_price", "pstatus")
        tree.heading("packname", text="Package Name")
        tree.heading("maximum_weight", text="Maximum Weight")
        tree.heading("maximum_height", text="Maximum Height")
        tree.heading("maximum_width", text="Maximum Width")
        tree.heading("minimum_price", text="Minimum Price")
        tree.heading("pstatus", text="Status")
        
        # Add data to the Treeview
        for package_data in res:
            packname = package_data['packname']
            max_weight = package_data['maximum_weight']
            max_height = package_data['maximum_height']
            max_width = package_data['maximum_width']
            min_price = package_data['minimum_price']
            pstatus = package_data['pstatus']
            
            tree.insert("", "end", values=(packname, max_weight, max_height, max_width, min_price, pstatus))

# Create the Packages GUI window
view_packages_window = tk.Tk()
view_packages_window.title("Quick Cargo | View Packages")

# Set window size
view_packages_window.geometry("1200x600")  # Width x Height

# Add a stylish heading
quick_cargo_label = tk.Label(view_packages_window, text="Quick Cargo",
                            font=("Helvetica", 20, "bold"))
quick_cargo_label.pack(pady=10)

# Create a frame for the header (top row)
header_frame = tk.Frame(view_packages_window)
header_frame.pack(side="top", fill="x")

# Display the username in the header frame (top left corner)
username_label = tk.Label(header_frame, text=f"Username: {username}")
username_label.pack(side="left", padx=10)

# Add a logout button to the header frame (top right corner)
logout_button = tk.Button(header_frame, text="Logout", command=logout)
logout_button.pack(side="right", padx=10)

heading_label = tk.Label(view_packages_window, text="View Package", font=("Helvetica", 16, "bold"))
heading_label.pack()

# Create a frame for the buttons (bottom row)
buttons_frame = tk.Frame(view_packages_window)
buttons_frame.pack(side="bottom", fill="x", pady=10)

# Create buttons for different options in the buttons frame
back_button = tk.Button(buttons_frame, text="Back to Admin", command=back_to_admin)
back_button.pack(side="left", padx=10)

manage_cargo_button = tk.Button(
    buttons_frame, text="Manage Cargo", command=manage_cargo)
manage_cargo_button.pack(side="left", padx=10)

all_bookings_button = tk.Button(
    buttons_frame, text="All Bookings", command=all_bookings)
all_bookings_button.pack(side="left", padx=10)

add_package_button = tk.Button(
    buttons_frame, text="Add Package", command=add_package)
add_package_button.pack(side="left", padx=10)

# Start the GUI event loop for the packages window
view_packages_window.mainloop()