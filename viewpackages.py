import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import dbconnect  # Import your dbconnect.py module

# Define tree at the global scope
tree = None

# Get the username from the command line arguments
username = sys.argv[1]

# Function to open the Manage Packages window
def manage_packages():
    messagebox.showinfo("Action Successful", "Redirecting to packages page")
    packages_window.destroy()  # Close the admin window
    subprocess.run(["python", "packages.py", username])  # Run packages.py using subprocess
    
# Function to open the Manage Cargo window
def manage_cargo():
    messagebox.showinfo("Action Successful", "Redirecting to managecargo page")
    packages_window.destroy()  # Close the packages window
    subprocess.run(["python", "managecargo.py", username])  # Run managecargo.py using subprocess

# Function to open the all bookings window
def all_bookings():
    messagebox.showinfo("Action Successful", "Redirecting to allbookings page")
    packages_window.destroy()  # Close the packages window
    subprocess.run(["python", "allbookings.py", username])  # Run allbookings.py using subprocess

# Function to go back to the admin window
def back_to_admin():
    packages_window.destroy()  # Close the packages window
    subprocess.run(["python", "admin.py", username])  # Return to admin.py using subprocess

def view_packages(username, tree):
    # Remove the global declaration for tree
    q = "SELECT * FROM packages"
    res = dbconnect.select(q, ())  # Pass an empty tuple as values
    
    if res:
        # Create a new window for displaying packages
        packages_window = tk.Toplevel()
        packages_window.title("View Packages")

        # Create a Treeview widget
        tree = ttk.Treeview(packages_window)
        tree.pack(pady=10)

        # Define columns and headings
        tree["columns"] = ("pack_id", "packname", "max_weight", "max_height", "max_width", "min_price", "pstatus", "actions")
        tree.heading("pack_id", text="Package ID")
        tree.heading("packname", text="Package Name")
        tree.heading("max_weight", text="Maximum Weight")
        tree.heading("max_height", text="Maximum Height")
        tree.heading("max_width", text="Maximum Width")
        tree.heading("min_price", text="Minimum Price")
        tree.heading("pstatus", text="Status")
        tree.heading("actions", text="Actions")

        # Add data to the Treeview
        for package_data in res:
            pack_id = package_data['pack_id']
            packname = package_data['packname']
            max_weight = package_data['maximum_weight']
            max_height = package_data['maximum_height']
            max_width = package_data['maximum_width']
            min_price = package_data['minimum_price']
            pstatus = package_data['pstatus']

            # Insert data into the Treeview
            item_id = tree.insert("", "end", values=(pack_id, packname, max_weight, max_height, max_width, min_price, pstatus, ""))
            edit_button = tk.Button(packages_window, text="Edit", command=lambda pack_id=pack_id: edit_package(pack_id))
            delete_button = tk.Button(packages_window, text="Delete", command=lambda pack_id=pack_id: delete_package(pack_id))
            tree.set(item_id, "actions", edit_button)

            # Create an additional column for the Delete button
            tree.insert(item_id, "end", values=("", ""), tags=("actions",))
            tree.set(item_id, "actions", delete_button)

# Function to edit a package
def edit_package(pack_id):
    # Create a new window for editing
    edit_window = tk.Toplevel()
    edit_window.title("Edit Package")

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
        package_data = dbconnect.select_one(select_query, select_values)

        if package_data:
            # Populate the entry fields with the current package data
            entry_packname.insert(0, package_data['packname'])
            entry_max_weight.insert(0, package_data['maximum_weight'])
            entry_max_height.insert(0, package_data['maximum_height'])
            entry_max_width.insert(0, package_data['maximum_width'])
            entry_min_price.insert(0, package_data['minimum_price'])
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
            # Delete the package from the database
            delete_query = "DELETE FROM packages WHERE pack_id = %s"
            delete_values = (pack_id,)
            dbconnect.execute(delete_query, delete_values)  # Assuming dbconnect.execute executes the SQL query

            # Refresh the view after deletion
            view_packages(username, tree)

            messagebox.showinfo("Success", "Package deleted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while deleting the package: {str(e)}")

# Function to save changes to a package
def save_package_changes(pack_id, packname, max_weight, max_height, max_width, min_price):
    try:
        # Update the package information in the database
        update_query = "UPDATE packages SET packname = %s, maximum_weight = %s, maximum_height = %s, maximum_width = %s, minimum_price = %s WHERE pack_id = %s"
        update_values = (packname, max_weight, max_height, max_width, min_price, pack_id)
        dbconnect.execute(update_query, update_values)  # Assuming dbconnect.execute executes the SQL query
        messagebox.showinfo("Success", "Package information updated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while updating package information: {str(e)}")

# Create the Packages GUI window
packages_window = tk.Tk()
packages_window.title("Quick Cargo | View Packages")

# Set window size
packages_window.geometry("800x600")  # Width x Height

# Add a stylish heading
quick_cargo_label = tk.Label(packages_window, text="Quick Cargo", font=("Helvetica", 20, "bold"))
quick_cargo_label.pack(pady=10)

# Create a frame for the header (top row)
header_frame = tk.Frame(packages_window)
header_frame.pack(side="top", fill="x")

# Display the username in the header frame (top left corner)
username_label = tk.Label(header_frame, text=f"Username: {username}")
username_label.pack(side="left", padx=10)

# Add a logout button to the header frame (top right corner)
logout_button = tk.Button(header_frame, text="Logout", command=back_to_admin)
logout_button.pack(side="right", padx=10)

heading_label = tk.Label(packages_window, text="View Packages", font=("Helvetica", 16, "bold"))
heading_label.pack()

# Create a button to go back to the admin window
back_button = tk.Button(packages_window, text="Back to Admin", command=back_to_admin)
back_button.pack(pady=10)

# Create a button to add a new package
add_package_button = tk.Button(packages_window, text="Add New Package", command=manage_packages)
add_package_button.pack(pady=10)

# Call the view_packages function to populate the Treeview
view_packages(username, tree)

# Start the GUI event loop for the packages window
packages_window.mainloop()
