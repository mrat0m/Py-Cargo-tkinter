import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import sys
import dbconnect

# Get the username from the command line arguments
username = sys.argv[1]

# Function to open the Admin window
def back_to_admin():
    all_bookings_window.destroy()  # Close the all bookings window
    subprocess.run(["python", "admin.py", username])  # Return to admin.py using subprocess

# Function to log out and return to the main window
def logout():
    all_bookings_window.destroy()  # Close the all bookings window
    subprocess.run(["python", "main.py"])  # Return to main.py using subprocess

def view_all_bookings():
    q = "SELECT * FROM bookings"
    res = dbconnect.select(q, ())  # Pass an empty tuple as values
    
    if res:
        # Create a new window for displaying bookings
        bookings_window = tk.Toplevel(all_bookings_window)
        bookings_window.title("All Bookings")

        # Create a Treeview widget
        tree = ttk.Treeview(bookings_window)
        tree.pack(pady=10)

        # Define columns and headings
        tree["columns"] = ("booking_id", "customer_id", "booking_date", "from_loc", "toloc", "weight", "length", "width", "amount", "booking_status", "pack_id")
        tree.heading("booking_id", text="Booking ID")
        tree.heading("customer_id", text="Customer ID")
        tree.heading("booking_date", text="Booking Date")
        tree.heading("from_loc", text="From Location")
        tree.heading("toloc", text="To Location")
        tree.heading("weight", text="Weight")
        tree.heading("length", text="Length")
        tree.heading("width", text="Width")
        tree.heading("amount", text="Amount")
        tree.heading("booking_status", text="Booking Status")
        tree.heading("pack_id", text="Package ID")

        # Create horizontal scrollbar
        hsb = ttk.Scrollbar(bookings_window, orient="horizontal", command=tree.xview)
        hsb.pack(side="bottom", fill="x")

        # Configure the treeview to use the horizontal scrollbar
        tree.configure(xscrollcommand=hsb.set)
        
        # Add data to the Treeview
        for booking_data in res:
            booking_id = booking_data['booking_id']
            customer_id = booking_data['customer_id']
            booking_date = booking_data['booking_date']
            from_loc = booking_data['from_loc']
            toloc = booking_data['toloc']
            weight = booking_data['weight']
            length = booking_data['length']
            width = booking_data['width']
            amount = booking_data['amount']
            booking_status = booking_data['booking_status']
            pack_id = booking_data['pack_id']

            tree.insert("", "end", values=(booking_id, customer_id, booking_date, from_loc, toloc, weight, length, width, amount, booking_status, pack_id))

# Create the All Bookings GUI window
all_bookings_window = tk.Tk()
all_bookings_window.title("Quick Cargo | All Bookings")

# Set window size
all_bookings_window.geometry("1200x600")  # Width x Height

# Add a stylish heading
quick_cargo_label = tk.Label(all_bookings_window, text="Quick Cargo",
                            font=("Helvetica", 20, "bold"))
quick_cargo_label.pack(pady=10)

# Create a frame for the header (top row)
header_frame = tk.Frame(all_bookings_window)
header_frame.pack(side="top", fill="x")

# Display the username in the header frame (top left corner)
username_label = tk.Label(header_frame, text=f"Username: {username}")
username_label.pack(side="left", padx=10)

# Add a logout button to the header frame (top right corner)
logout_button = tk.Button(header_frame, text="Logout", command=logout)
logout_button.pack(side="right", padx=10)

heading_label = tk.Label(all_bookings_window, text="All Bookings", font=("Helvetica", 16, "bold"))
heading_label.pack()

# Automatically run the view_all_bookings function
view_all_bookings()

# Create a frame for the buttons (bottom row)
buttons_frame = tk.Frame(all_bookings_window)
buttons_frame.pack(side="bottom", fill="x", pady=10)

# Create buttons for different options in the buttons frame
back_button = tk.Button(buttons_frame, text="Back to Admin", command=back_to_admin)
back_button.pack(side="left", padx=10)

view_all_bookings_button = tk.Button(
    buttons_frame, text="View All Bookings", command=view_all_bookings)
view_all_bookings_button.pack(side="right", padx=10)

# Start the GUI event loop for the all bookings window
all_bookings_window.mainloop()
