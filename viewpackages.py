import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import dbconnect  # Import your dbconnect.py module

# Create a dictionary to store references to all windows
windows = {}

# Get the username from the command line arguments
username = sys.argv[1]

# Function to open the Manage Cargo window
def manage_cargo():
    windows["view_package_window"].destroy()
    subprocess.run(["python", "managecargo.py", username])

# Function to open the All Bookings window
def all_bookings():
    windows["view_package_window"].destroy()
    subprocess.run(["python", "allbookings.py", username])

# Function to log out and return to the main window
def logout():
    windows["view_package_window"].destroy()
    subprocess.run(["python", "main.py"])

def back_to_admin():
    if "view_package_window" in windows:
        print("Destroying view_package_window")
        windows["view_package_window"].destroy()
    else:
        print("view_package_window not found in windows dictionary")
    # Return to admin.py using subprocess
    subprocess.run(["python", "admin.py", username])

def create_window(window_name, title, size):
    if window_name in windows:
        return windows[window_name]

    new_window = tk.Toplevel()
    new_window.title(title)
    new_window.geometry(size)
    windows[window_name] = new_window  # Store a reference to the new window
    return new_window

# Function to view packages
def view_packages(username):
    q = "SELECT * FROM packages"
    res = dbconnect.select(q, ())  # Assuming this function fetches data from the database

    # Create a new view_package_window each time
    create_window("view_package_window", "Package Details", "800x800")
        
    view_package_window = windows["view_package_window"]

    # Clear the previous content in the window (if any)
    for widget in view_package_window.winfo_children():
        widget.destroy()

    # Add a stylish heading
    heading_label = tk.Label(
        view_package_window, text="Quick Cargo", font=("Helvetica", 20, "bold"))
    heading_label.pack(pady=15)

    # Create a frame for the top row (username, home button, and logout button)
    top_frame = tk.Frame(view_package_window)
    top_frame.pack(fill="x")

    # Create a logout button on the top-right corner
    logout_button = tk.Button(top_frame, text="Logout", command=logout)
    logout_button.pack(side="right", padx=10, pady=5)

    # Create a "Home" button on the top-right corner next to the logout button
    home_button = tk.Button(top_frame, text="Back to admin", command=back_to_admin)
    home_button.pack(side="right", padx=10, pady=5)

    # Display the username at the top-left corner
    username_label = tk.Label(
        top_frame, text="Username: " + username, font=("Helvetica", 10))
    username_label.pack(side="left", padx=10, pady=5)

    # Add a title to the package details window in the middle
    title_label = tk.Label(
        view_package_window, text="Package Details", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)

    # Create a canvas with a scrollbar
    canvas = tk.Canvas(view_package_window)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(view_package_window, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to hold the package details
    package_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=package_frame, anchor="nw")

    for packages in res:
        pack_id = packages["pack_id"]
        packname = packages["packname"]
        maximum_weight = packages["maximum_weight"]
        maximum_height = packages["maximum_height"]
        maximum_width = packages["maximum_width"]
        minimum_price = packages["minimum_price"]
        pstatus = packages["pstatus"]

        # Add package details to the frame
        tk.Label(package_frame, text="Package ID: " + str(pack_id)).pack(anchor=tk.W)
        tk.Label(package_frame, text="Package Name: " + packname).pack(anchor=tk.W)
        tk.Label(package_frame, text="Maximum Weight: " + maximum_weight).pack(anchor=tk.W)
        tk.Label(package_frame, text="Maximum Height: " + maximum_height).pack(anchor=tk.W)
        tk.Label(package_frame, text="Maximum Width: " + maximum_width).pack(anchor=tk.W)
        tk.Label(package_frame, text="Minimum Price: " + minimum_price).pack(anchor=tk.W)
        tk.Label(package_frame, text="Status: " + pstatus).pack(anchor=tk.W)

        # Create a button to edit the selected package
        edit_button = tk.Button(package_frame, text="Edit", command=lambda p=pack_id: edit_package(p))
        edit_button.pack(anchor=tk.W)
        # Create a button to delete the selected package
        delete_button = tk.Button(package_frame, text="Delete", command=lambda p=pack_id: delete_package(p))
        delete_button.pack(anchor=tk.W)


        package_frame.update_idletasks()  # Update the canvas

        # Configure the canvas scroll region
        canvas.config(scrollregion=canvas.bbox("all"))

# Function to edit a package
def edit_package(pack_id):
    # Create a new window for editing
    edit_window = create_window("view_package_window", "Package Details", "800x800")

    # Create labels and entry fields for editing package information
    label_packname = tk.Label(edit_window, text="Package Name:")
    label_packname.pack()
    entry_packname = tk.Entry(edit_window)
    entry_packname.pack()

    label_max_weight = tk.Label(edit_window, text="Maximum Weight:")
    label_max_weight.pack()
    entry_max_weight = tk.Entry(edit_window)
    entry_max_weight.pack()

    label_max_height = tk.Label(edit_window, text="Maximum Height:")
    label_max_height.pack()
    entry_max_height = tk.Entry(edit_window)
    entry_max_height.pack()

    label_max_width = tk.Label(edit_window, text="Maximum Width:")
    label_max_width.pack()
    entry_max_width = tk.Entry(edit_window)
    entry_max_width.pack()

    label_min_price = tk.Label(edit_window, text="Minimum Price:")
    label_min_price.pack()
    entry_min_price = tk.Entry(edit_window)
    entry_min_price.pack()

    try:
        # Fetch the current package details from the database
        select_query = "SELECT * FROM packages WHERE pack_id = %s"
        select_values = (pack_id,)
        package_data = dbconnect.select(select_query, select_values)

        if package_data:
            # Populate the entry fields with the current package data
            entry_packname.insert(0, package_data[0]['packname'])
            entry_max_weight.insert(0, package_data[0]['maximum_weight'])
            entry_max_height.insert(0, package_data[0]['maximum_height'])
            entry_max_width.insert(0, package_data[0]['maximum_width'])
            entry_min_price.insert(0, package_data[0]['minimum_price'])
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while fetching package details: {str(e)}")

    # Create a button to save changes
    save_button = tk.Button(edit_window, text="Save Changes", command=lambda: save_package_changes(pack_id, entry_packname.get(), entry_max_weight.get(), entry_max_height.get(), entry_max_width.get(), entry_min_price.get()))
    save_button.pack(pady=10)

# Function to delete a package
def delete_package(pack_id):
    try:
        # Confirm the deletion with a message box
        confirmation = messagebox.askyesno("Delete Package", "Are you sure you want to delete this package?")
        if confirmation:
            # Delete the package from the database based on the pack_id
            delete_query = "DELETE FROM packages WHERE pack_id = %s"
            delete_values = (pack_id,)
            dbconnect.delete(delete_query, delete_values)  

            messagebox.showinfo("Success", "Package deleted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while deleting the package: {str(e)}")

# Function to save changes to a package
def save_package_changes(pack_id, packname, max_weight, max_height, max_width, min_price):
    try:
        # Update the package information in the database
        q = "UPDATE packages SET packname = %s, maximum_weight = %s, maximum_height = %s, maximum_width = %s, minimum_price = %s WHERE pack_id = %s"
        values = (packname, max_weight, max_height, max_width, min_price, pack_id)
        dbconnect.update(q, values)  
        messagebox.showinfo("Success", "Package information updated successfully!")
        # edit_window.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while updating package information: {str(e)}")

