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

# Function to add a View packages from the database
def view_packages():
    q = "SELECT * FROM packages"
    res = dbconnect.select(q, ())  # Pass an empty tuple as values
    if res:
        package_frame = tk.Frame(view_packages_window)
        package_frame.pack(pady=10)
        print(res)  # Print the result to the console

        for package_data in res:
            # Extract package data and display using labels (as you have in your code)
            packname = package_data['packname']
            max_weight = package_data['maximum_weight']
            max_height = package_data['maximum_height']
            max_width = package_data['maximum_width']
            min_price = package_data['minimum_price']
            pstatus = package_data['pstatus']

            packname_label = tk.Label(package_frame, text=f"Package Name: {packname}")
            packname_label.pack()

            max_weight_label = tk.Label(package_frame, text=f"Maximum Weight: {max_weight}")
            max_weight_label.pack()

            max_height_label = tk.Label(package_frame, text=f"Maximum Height: {max_height}")
            max_height_label.pack()

            max_width_label = tk.Label(package_frame, text=f"Maximum Width: {max_width}")
            max_width_label.pack()

            min_price_label = tk.Label(package_frame, text=f"Minimum Price: {min_price}")
            min_price_label.pack()

            pstatus_label = tk.Label(package_frame, text=f"Status: {pstatus}")
            pstatus_label.pack()

# Create the Packages GUI window
view_packages_window = tk.Tk()
view_packages_window.title("Quick Cargo | View Packages")

# Set window size
view_packages_window.geometry("500x400")  # Width x Height

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

# Start the GUI event loop for the packages window
view_packages_window.mainloop()