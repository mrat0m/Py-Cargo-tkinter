import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import sys
import dbconnect  # dbconnect.py

# Function to go back to the admin window
def back_to_admin():
    manage_cargo_window.destroy()  # Close the manage cargo window
    subprocess.run(["python", "admin.py", username])  # Return to admin.py using subprocess

# Function to log out and return to the main window
def logout():
    manage_cargo_window.destroy()  # Close the manage cargo window
    subprocess.run(["python", "main.py"])  # Return to main.py using subprocess

# Function to view cargo status
def view_cargo_status():
    # Create a new window to display cargo status
    cargo_status_window = tk.Toplevel(manage_cargo_window)
    cargo_status_window.title("Cargo Status")

    # Create a Treeview widget to display cargo status
    tree = ttk.Treeview(cargo_status_window)
    tree.pack(padx=10, pady=10)

    # Define columns
    tree["columns"] = ("status_id", "booking_id", "place_name", "status_date_time", "actions")
    tree.heading("status_id", text="Status ID")
    tree.heading("booking_id", text="Booking ID")
    tree.heading("place_name", text="Place Name")
    tree.heading("status_date_time", text="Status Date & Time")
    tree.heading("actions", text="Actions")

    # Fetch cargo status data from the database
    q = "SELECT * FROM cargo_status"
    res = dbconnect.select(q, ())  # Pass an empty tuple as values

    # Populate the Treeview with cargo status data
    for cargo in res:
        status_id = cargo["status_id"]
        booking_id = cargo["booking_id"]
        place_name = cargo["place_name"]
        status_date_time = cargo["status_date_time"]

        # Insert data into the Treeview
        item_id = tree.insert("", "end", values=(status_id, booking_id, place_name, status_date_time, ""))
        edit_button = tk.Button(cargo_status_window, text="Edit", command=lambda status_id=status_id: edit_cargo_status(status_id, tree))
        tree.set(item_id, "actions", edit_button)

# Function to open the edit cargo status window
def edit_cargo_status(status_id, tree):
    # Create a new window for editing cargo status
    edit_cargo_window = tk.Toplevel(manage_cargo_window)
    edit_cargo_window.title("Edit Cargo Status")

    # Create labels and entry fields for editing cargo status
    label_place_name = tk.Label(edit_cargo_window, text="Place Name:")
    label_place_name.pack()
    entry_place_name = tk.Entry(edit_cargo_window)
    entry_place_name.pack()

    try:
        # Fetch the current cargo status details from the database
        select_query = "SELECT * FROM cargo_status WHERE status_id = %s"
        select_values = (status_id,)
        cargo_data = dbconnect.select_one(select_query, select_values)

        if cargo_data:
            # Populate the entry field with the current place_name
            entry_place_name.insert(0, cargo_data['place_name'])
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while fetching cargo status details: {str(e)}")

    # Create a button to save changes
    save_button = tk.Button(edit_cargo_window, text="Save Changes", command=lambda: save_cargo_status_changes(status_id, entry_place_name.get(), tree))
    save_button.pack(pady=10)

# Function to save changes to cargo status
def save_cargo_status_changes(status_id, place_name, tree):
    try:
        # Update the cargo status information in the database
        update_query = "UPDATE cargo_status SET place_name = %s WHERE status_id = %s"
        update_values = (place_name, status_id)
        dbconnect.execute(update_query, update_values)  # Assuming dbconnect.execute executes the SQL query
        messagebox.showinfo("Success", "Cargo status updated successfully!")

        # Update the Treeview with the new place_name
        item_id = tree.selection()[0]  # Get the selected item in the Treeview
        tree.item(item_id, values=(status_id, place_name, tree.item(item_id, "status_date_time"), ""))

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while updating cargo status: {str(e)}")

# Get the username from the command line arguments
username = sys.argv[1]

# Create the Manage Cargo GUI window
manage_cargo_window = tk.Tk()
manage_cargo_window.title("Quick Cargo | Manage Cargo")

# Set window size
manage_cargo_window.geometry("800x600")  # Width x Height

# Add a stylish heading
heading_label = tk.Label(manage_cargo_window, text="Quick Cargo | Manage Cargo",
                         font=("Helvetica", 20, "bold"))
heading_label.pack(pady=15)

# Create a frame for the header (top row)
header_frame = tk.Frame(manage_cargo_window)
header_frame.pack(side="top", fill="x")

# Display the username in the header frame (top left corner)
username_label = tk.Label(header_frame, text=f"Username: {username}")
username_label.pack(side="left", padx=10)

# Add a logout button to the header frame (top right corner)
logout_button = tk.Button(header_frame, text="Logout", command=logout)
logout_button.pack(side="right", padx=10)

# Call the view_cargo_status function to populate cargo status when the window is created
view_cargo_status()

# Create a frame for the content (center row)
content_frame = tk.Frame(manage_cargo_window)
content_frame.pack(side="top", fill="both", expand=True)

# Create a button to go back to the admin window
back_button = tk.Button(content_frame, text="Back to Admin", command=back_to_admin)
back_button.pack(side="left", padx=10)

# Start the GUI event loop for the manage cargo window
manage_cargo_window.mainloop()
