import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import sys
import datetime
import dbconnect  # Import your dbconnect.py module

# Get the username from the command line arguments
username = sys.argv[1]

# Create a dictionary to store references to all windows
windows = {}

# Initialize customer_window as None
customer_window = None

# Create the main customer window
customer_window = tk.Tk()
customer_window.title("Quick Cargo | Customer Panel")
customer_window.geometry("400x400")  # Set the size of the customer window
windows["customer_window"] = customer_window  # Store a reference to the customer window

# Function to go back to the main login window (main.py)
def logout():
    global customer_window  # Declare customer_window as global
    if customer_window:
        customer_window.destroy()  # Close the customer window if it exists
    subprocess.run(["python", "main.py"])  # Return to main.py using subprocess

# Function to create a new window, add it to the dictionary, and set its size
def create_window(window_name, title, size):
    new_window = tk.Toplevel()
    new_window.title(title)
    new_window.geometry(size)
    windows[window_name] = new_window  # Store a reference to the new window
    return new_window

# Function to create a "Home" button in a window
def create_home_button(window):
    home_button = tk.Button(window, text="Home", command=lambda w=window: go_to_customer_window(w))
    home_button.pack(side="bottom", pady=10)

# Modify the go_to_customer_window function to accept two arguments
def go_to_customer_window(current_window, parent_window):
    current_window.destroy()  # Destroy the current window
    parent_window.deiconify()  # Show the parent window
    windows["current_window"] = parent_window  # Set the current window as the parent window

def update_booking_status(booking_id, new_status):
    # Update the booking status in the database for the given booking_id
    q = "UPDATE bookings SET booking_status = %s WHERE booking_id = %s"
    values = (new_status, booking_id)
    dbconnect.update(q, values)

# Function to fetch and display package details
def fetch_package_details():
    package_details_window = create_window("package_details_window", "Package Details", "400x400")

    # Add a stylish heading
    heading_label = tk.Label(package_details_window, text="Quick Cargo", font=("Helvetica", 20, "bold"))
    heading_label.pack(pady=15)

    # Create a frame for the top row (username, home button, and logout button)
    top_frame = tk.Frame(package_details_window)
    top_frame.pack(fill="x")

    # Create a logout button on the top-right corner
    logout_button = tk.Button(top_frame, text="Logout", command=logout)
    logout_button.pack(side="right", padx=10, pady=5)

    # Create a "Home" button on the top-right corner next to the logout button
    home_button = tk.Button(top_frame, text="Home", command=lambda: go_to_customer_window(package_details_window))
    home_button.pack(side="right", padx=10, pady=5)

    # Display the username at the top-left corner
    username_label = tk.Label(top_frame, text="Username: " + username, font=("Helvetica", 10))
    username_label.pack(side="left", padx=10, pady=5)

    # Add a title to the package details window in the middle
    title_label = tk.Label(package_details_window, text="Package Details", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)

    # Create a canvas with a scrollbar
    canvas = tk.Canvas(package_details_window)
    canvas.pack(side="left", fill="both", expand=True)  # Change 'side' to 'left'

    scrollbar = ttk.Scrollbar(package_details_window, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to hold the package details
    package_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=package_frame, anchor="nw")


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

        # Add package details to the frame
        tk.Label(package_frame, text="Package Name: " + packname).pack(anchor=tk.W)
        tk.Label(package_frame, text="Maximum Weight: " + maximum_weight).pack(anchor=tk.W)
        tk.Label(package_frame, text="Maximum Height: " + maximum_height).pack(anchor=tk.W)
        tk.Label(package_frame, text="Maximum Width: " + maximum_width).pack(anchor=tk.W)
        tk.Label(package_frame, text="Minimum Price: " + minimum_price).pack(anchor=tk.W)
        # tk.Label(package_frame, text="Status: " + pstatus).pack(anchor=tk.W)

        # Create a button to book the selected package
        book_button = tk.Button(package_frame, text="Book", command=lambda p=pack_id, name=packname: book_package(p, name, package_details_window))
        book_button.pack(anchor=tk.W)

    package_frame.update_idletasks()  # Update the canvas

    # Configure the canvas scroll region
    canvas.config(scrollregion=canvas.bbox("all"))

# Function to book a package
def book_package(pack_id, packname, parent_window):
    parent_window.withdraw()  # Hide the parent window

    book_package_window = create_window("book_package_window", "Book Package", "400x300")
    create_home_button(book_package_window)  # Add a "Home" button to this window

    tk.Label(book_package_window, text=f"Selected Package: {packname}").pack(pady=5)

    tk.Label(book_package_window, text="From Location:").pack(pady=5)
    from_loc_entry = tk.Entry(book_package_window)
    from_loc_entry.pack()

    tk.Label(book_package_window, text="To Location:").pack(pady=5)
    to_loc_entry = tk.Entry(book_package_window)
    to_loc_entry.pack()

    def confirm_booking():
        from_loc = from_loc_entry.get()
        to_loc = to_loc_entry.get()

        customer_id = dbconnect.get_customer_id(username)

        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        q = "SELECT maximum_weight, maximum_height, maximum_width, minimum_price FROM packages WHERE pack_id = %s"
        selected_package_details = dbconnect.select(q, (pack_id,))[0]

        maximum_weight = selected_package_details["maximum_weight"]
        maximum_height = selected_package_details["maximum_height"]
        maximum_width = selected_package_details["maximum_width"]
        minimum_price = selected_package_details["minimum_price"]

        amount = minimum_price

        q = "INSERT INTO bookings (customer_id, from_loc, toloc, weight, length, width, amount, booking_status, pack_id, booking_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (customer_id, from_loc, to_loc, maximum_weight, maximum_height, maximum_width, amount, "Processing", pack_id , current_datetime)
        booking_id = dbconnect.insert(q, values)

        # Update the booking status to "Processing"
        update_booking_status(booking_id, "Processing")

        messagebox.showinfo("Booking Confirmation", "Redirecting to payment portal!! WARNING: this is development phone never share orginal card details!")
        
         # Destroy the "Book Package" window
        book_package_window.destroy()
        
        # Redirect to the payment page
        create_payment_window(amount, booking_id, book_package_window)

    confirm_button = tk.Button(book_package_window, text="Confirm Booking", command=confirm_booking)
    confirm_button.pack(pady=10)

    def create_payment_window(amount, booking_id, parent_window):
        payment_window = create_window("payment_window", "Card Payment", "500x400")
        create_home_button(payment_window)  # Add a "Home" button to this window

        tk.Label(payment_window, text=f"Amount to Pay: ₹{amount}/-").pack(pady=5)

        tk.Label(payment_window, text="Card Number:").pack(pady=5)
        card_number_entry = tk.Entry(payment_window)
        card_number_entry.pack()

        tk.Label(payment_window, text="Name on Card:").pack(pady=5)
        name_on_card_entry = tk.Entry(payment_window)
        name_on_card_entry.pack()

        tk.Label(payment_window, text="Expiry Date:").pack(pady=5)
        exp_date_entry = tk.Entry(payment_window)
        exp_date_entry.pack()

        tk.Label(payment_window, text="CVV:").pack(pady=5)
        cvv_entry = tk.Entry(payment_window)
        cvv_entry.pack()

        def process_payment():
            card_number = card_number_entry.get()
            name_on_card = name_on_card_entry.get()
            exp_date = exp_date_entry.get()
            cvv = cvv_entry.get()

            # Here, you can implement the actual payment processing logic
            # (e.g., connecting to a payment gateway).

            # For demonstration purposes, simply close the payment window and show a confirmation message.
            payment_window.destroy()
            messagebox.showinfo("Payment Confirmation", f"Payment of ₹{amount}/- for Booking ID {booking_id} is confirmed!")

            # Insert payment record into the database
            q = "INSERT INTO payment (booking_id, amount_paid, payment_date) VALUES (%s, %s, %s)"
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            dbconnect.insert(q, (booking_id, amount, current_datetime))

            # Update the booking status to "Paid"
            update_booking_status(booking_id, "Paid")

            # Redirect back to the customer window
            go_to_customer_window(payment_window, parent_window)

        pay_button = tk.Button(payment_window, text="Pay", command=process_payment)
        pay_button.pack(pady=10)

# Function to view bookings
def view_bookings():
    bookings_window = create_window("bookings_window", "My Bookings", "1000x500")
    create_home_button(bookings_window)  # Add a "Home" button to this window

    q = "SELECT * FROM bookings WHERE customer_id = %s"
    customer_id = dbconnect.get_customer_id(username)
    bookings = dbconnect.select(q, (customer_id,))

    frame = tk.Frame(bookings_window)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tree = ttk.Treeview(frame, columns=("booking_id", "booking_date", "from_loc", "toloc", "weight", "amount", "booking_status"))
    tree.heading("booking_id", text="Booking ID")
    tree.heading("booking_date", text="Booking Date")
    tree.heading("from_loc", text="From Location")
    tree.heading("toloc", text="To Location")
    tree.heading("weight", text="Weight")
    tree.heading("amount", text="Amount")
    tree.heading("booking_status", text="Status")

    tree.column("#0", width=0, stretch=tk.NO)  # Hide the first column

    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)

    # Add data to the Treeview
    for booking in bookings:
        booking_id = booking["booking_id"]
        booking_date = booking["booking_date"]
        from_loc = booking["from_loc"]
        toloc = booking["toloc"]
        weight = booking["weight"]
        amount = booking["amount"]
        booking_status = booking["booking_status"]

        tree.insert("", "end", values=(booking_id, booking_date, from_loc, toloc, weight, amount, booking_status))

    # Pack the Treeview and scrollbar
    tree.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")

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

# Start the GUI event loop for the customer window
customer_window.mainloop()
