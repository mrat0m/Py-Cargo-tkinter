import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import sys
import datetime
import dbconnect  # Import your dbconnect.py module

# Get the username from the command line arguments
username = sys.argv[1]

# Function to go back to the main login window (main.py)
def logout():
    customer_window.destroy()  # Close the customer window
    subprocess.run(["python", "main.py"])  # Return to main.py using subprocess

# Function to go back to the customer.py window
def go_back_to_customer():
    customer_window.destroy()  # Close the home window
    subprocess.run(["python", "customer.py", username])  # Return to customer.py using subprocess

# Function to fetch and display package details
def fetch_package_details():
    # Create a new window to display package details
    package_details_window = tk.Toplevel(customer_window)
    package_details_window.title("Package Details")

    # Fetch package details from the database
    q = "SELECT pack_id, packname, maximum_weight, maximum_height, maximum_width, minimum_price, pstatus FROM packages"
    res = dbconnect.select(q, ())

    for package in res:
        pack_id = package["pack_id"]
        packname = package["packname"]
        maximum_weight = package["maximum_weight"]
        maximum_height = package["maximum_height"]
        maximum_width = package["maximum_width"]
        minimum_price = package["minimum_price"]
        pstatus = package["pstatus"]

        # Create a frame for each package with its details and a book button
        package_frame = tk.Frame(package_details_window, padx=10, pady=10)
        package_frame.pack(fill=tk.BOTH)

        # Add package details to the frame
        tk.Label(package_frame, text="Package Name: " + packname).pack(anchor=tk.W)
        tk.Label(package_frame, text="Maximum Weight: " + maximum_weight).pack(anchor=tk.W)
        tk.Label(package_frame, text="Maximum Height: " + maximum_height).pack(anchor=tk.W)
        tk.Label(package_frame, text="Maximum Width: " + maximum_width).pack(anchor=tk.W)
        tk.Label(package_frame, text="Minimum Price: " + minimum_price).pack(anchor=tk.W)
        tk.Label(package_frame, text="Status: " + pstatus).pack(anchor=tk.W)

        # Create a button to book the selected package
        book_button = tk.Button(package_frame, text="Book", command=lambda p=pack_id, name=packname: book_package(p, name))
        book_button.pack(anchor=tk.W)

# Function to book a package
def book_package(pack_id, packname):
    # Create a new window to book a package
    book_package_window = tk.Toplevel(customer_window)
    book_package_window.title("Book Package")

    book_package_window.geometry("400x300")

    tk.Label(book_package_window, text=f"Selected Package: {packname}").pack(pady=5)

    tk.Label(book_package_window, text="From Location:").pack(pady=5)
    from_loc_entry = tk.Entry(book_package_window)
    from_loc_entry.pack()

    tk.Label(book_package_window, text="To Location:").pack(pady=5)
    to_loc_entry = tk.Entry(book_package_window)
    to_loc_entry.pack()

    # Function to confirm the booking
    def confirm_booking():
        from_loc = from_loc_entry.get()
        to_loc = to_loc_entry.get()

        # Fetch customer_id dynamically based on the username
        customer_id = dbconnect.get_customer_id(username)

        # Get the current date and time
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Fetch package details to calculate the amount
        q = "SELECT maximum_weight, maximum_height, maximum_width, minimum_price FROM packages WHERE pack_id = %s"
        selected_package_details = dbconnect.select(q, (pack_id,))[0]

        maximum_weight = selected_package_details["maximum_weight"]
        maximum_height = selected_package_details["maximum_height"]
        maximum_width = selected_package_details["maximum_width"]
        minimum_price = selected_package_details["minimum_price"]

        # Calculate the amount (assuming it's based on the minimum price)
        amount = minimum_price

        # Insert the booking into the database with package details
        q = "INSERT INTO bookings (customer_id, from_loc, toloc, weight, length, width, amount, booking_status, pack_id, booking_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (customer_id, from_loc, to_loc, maximum_weight, maximum_height, maximum_width, amount, "Booked", pack_id , current_datetime)
        dbconnect.insert(q, values)

        messagebox.showinfo("Booking Confirmation", "Booking successful!")  # Use messagebox here
        book_package_window.destroy()  # Close the booking window

    # Create a button to confirm the booking
    confirm_button = tk.Button(book_package_window, text="Confirm Booking", command=confirm_booking)
    confirm_button.pack(pady=10)

def view_bookings():
    # Create a new window to display bookings
    bookings_window = tk.Toplevel(customer_window)
    bookings_window.title("My Bookings")

    # Fetch bookings associated with the current user from the database
    q = "SELECT * FROM bookings WHERE customer_id = %s"
    customer_id = dbconnect.get_customer_id(username)
    bookings = dbconnect.select(q, (customer_id,))

    # Create a Treeview widget to display bookings
    tree = ttk.Treeview(bookings_window)
    tree.pack(padx=10, pady=10)

    # Define columns
    tree["columns"] = ("booking_id", "booking_date", "from_loc", "toloc", "weight", "amount", "booking_status")

    # Set column headings
    tree.heading("booking_id", text="Booking ID")
    tree.heading("booking_date", text="Booking Date")
    tree.heading("from_loc", text="From Location")
    tree.heading("toloc", text="To Location")
    tree.heading("weight", text="Weight")
    tree.heading("amount", text="Amount")
    tree.heading("booking_status", text="Status")

    # Populate the Treeview with booking details
    for booking in bookings:
        booking_id = booking["booking_id"]
        booking_date = booking["booking_date"]
        from_loc = booking["from_loc"]
        toloc = booking["toloc"]
        weight = booking["weight"]
        amount = booking["amount"]
        booking_status = booking["booking_status"]

        tree.insert("", "end", values=(booking_id, booking_date, from_loc, toloc, weight, amount, booking_status))

# Create the Customer GUI window
customer_window = tk.Tk()
customer_window.title("Quick Cargo | Customer Panel")

# Set window size
customer_window.geometry("400x300")  # Width x Height

# Add a stylish heading
heading_label = tk.Label(customer_window, text="Quick Cargo", font=("Helvetica", 20, "bold"))
heading_label.pack(pady=15)

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
fetch_package_details_button = tk.Button(content_frame, text="Book a Package", command=fetch_package_details)
fetch_package_details_button.pack(side="top", pady=10)

# Create a button to view bookings
view_bookings_button = tk.Button(content_frame, text="View My Bookings", command=view_bookings)
view_bookings_button.pack(side="top", pady=10)

# Create a "Home" button to go back to the customer.py window
home_button = tk.Button(content_frame, text="Home", command=go_back_to_customer)
home_button.pack(side="bottom", pady=10)

# Start the GUI event loop for the customer window
customer_window.mainloop()
