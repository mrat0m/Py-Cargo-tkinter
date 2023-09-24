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
    packages_window.destroy()  # Close the packages window
    # Run managecargo.py using subprocess
    subprocess.run(["python", "managecargo.py", username])

# Function to open the all bookings window


def all_bookings():
    messagebox.showinfo("Action Successful", "Redirecting to allbookings page")
    packages_window.destroy()  # Close the packages window
    # Run allbookings.py using subprocess
    subprocess.run(["python", "allbookings.py", username])

# Function to go back to the admin window


def back_to_admin():
    packages_window.destroy()  # Close the packages window
    # Return to admin.py using subprocess
    subprocess.run(["python", "admin.py", username])


def view_packages(username):
    packages_window.destroy()  # Close the packages window
    # Run viewpackages.py using subprocess
    subprocess.run(["python", "viewpackages.py", username])

# Function to log out and return to the main window


def logout():
    packages_window.destroy()  # Close the packages window
    subprocess.run(["python", "main.py"])  # Return to main.py using subprocess

# Function to add a new package to the database


def add_package():
    packname = packname_entry.get()
    max_weight = max_weight_entry.get()
    max_height = max_height_entry.get()
    max_width = max_width_entry.get()
    min_price = min_price_entry.get()
    pstatus = "active"

    if not packname or not max_weight or not max_height or not max_width or not min_price:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    # Insert package data into the 'packages' table using dbconnect.insert
    insert_query = "INSERT INTO packages (packname, maximum_weight, maximum_height, maximum_width, minimum_price, pstatus) VALUES (%s, %s, %s, %s, %s, %s)"
    insert_values = (packname, max_weight, max_height,
                     max_width, min_price, pstatus)
    new_package_id = dbconnect.insert(insert_query, insert_values)

    if new_package_id:
        messagebox.showinfo("Success", "Package added to the database!")

        # Clear the entry fields after adding the package
        packname_entry.delete(0, tk.END)
        max_weight_entry.delete(0, tk.END)
        max_height_entry.delete(0, tk.END)
        max_width_entry.delete(0, tk.END)


# Create the Packages GUI window
packages_window = tk.Tk()
packages_window.title("Quick Cargo | Add Packages")

# Set window size
packages_window.geometry("500x400")  # Width x Height

# Add a stylish heading
quick_cargo_label = tk.Label(packages_window, text="Quick Cargo",
                             font=("Helvetica", 20, "bold"))
quick_cargo_label.pack(pady=10)

# Create a frame for the header (top row)
header_frame = tk.Frame(packages_window)
header_frame.pack(side="top", fill="x")

# Display the username in the header frame (top left corner)
username_label = tk.Label(header_frame, text=f"Username: {username}")
username_label.pack(side="left", padx=10)

# Add a logout button to the header frame (top right corner)
logout_button = tk.Button(header_frame, text="Logout", command=logout)
logout_button.pack(side="right", padx=10)

heading_label = tk.Label(packages_window, text="Add New Package",
                         font=("Helvetica", 16, "bold"))
heading_label.pack()

# Create labels and entry fields for package information
packname_label = tk.Label(packages_window, text="Package Name:")
packname_label.pack()

packname_entry = tk.Entry(packages_window, width=30)
packname_entry.pack()

max_weight_label = tk.Label(packages_window, text="Maximum Weight:")
max_weight_label.pack()

max_weight_entry = tk.Entry(packages_window, width=30)
max_weight_entry.pack()

max_height_label = tk.Label(packages_window, text="Maximum Height:")
max_height_label.pack()

max_height_entry = tk.Entry(packages_window, width=30)
max_height_entry.pack()

max_width_label = tk.Label(packages_window, text="Maximum Width:")
max_width_label.pack()

max_width_entry = tk.Entry(packages_window, width=30)
max_width_entry.pack()

min_price_label = tk.Label(packages_window, text="Minimum Price:")
min_price_label.pack()

min_price_entry = tk.Entry(packages_window, width=30)
min_price_entry.pack()

# Create a button to add the package to the database
add_button = tk.Button(
    packages_window, text="Add Package", command=add_package)
add_button.pack(pady=10)

# Create a frame for the buttons (bottom row)
buttons_frame = tk.Frame(packages_window)
buttons_frame.pack(side="bottom", fill="x", pady=10)

# Create buttons for different options in the buttons frame
back_button = tk.Button(
    buttons_frame, text="Back to Admin", command=back_to_admin)
back_button.pack(side="left", padx=10)

manage_cargo_button = tk.Button(
    buttons_frame, text="Manage Cargo", command=manage_cargo)
manage_cargo_button.pack(side="left", padx=10)

all_bookings_button = tk.Button(
    buttons_frame, text="All Bookings", command=all_bookings)
all_bookings_button.pack(side="left", padx=10)

# Create a button to go to the View Packages window
view_packages_button = tk.Button(
    buttons_frame, text="View Packages", command=lambda: view_packages(username))
view_packages_button.pack(side="right", padx=10)

# Start the GUI event loop for the packages window
packages_window.mainloop()
