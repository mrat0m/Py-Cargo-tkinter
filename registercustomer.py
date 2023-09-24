import tkinter as tk
from tkinter import messagebox
import subprocess
import dbconnect  # Importing the dbconnect module
from PIL import Image, ImageTk  # Import PIL for image handling

# Function to perform customer registration


def register_customer():
    username = username_entry.get().lower()  # Convert to lowercase
    password = password_entry.get()
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get().lower()  # Convert email to lowercase

    if not username or not password or not first_name or not last_name or not phone or not email:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    # Insert customer registration data into the login table in the database
    login_query = "INSERT INTO login (username, password, user_type) VALUES (%s, %s, 'customer')"
    login_values = (username, password)
    dbconnect.insert(login_query, login_values)

    # Insert customer registration data into the customers table in the database
    customer_query = "INSERT INTO customers (username, first_name, last_name, phone, email) VALUES (%s, %s, %s, %s, %s)"
    customer_values = (username, first_name, last_name, phone, email)
    dbconnect.insert(customer_query, customer_values)

    messagebox.showinfo("Success", "Registration successful!")

    register_window.destroy()  # Close the registration window
    # Run customer.py using subprocess
    subprocess.run(["python", "customer.py", username])

# Function to go back to the main login window (main.py)


def return_to_main():
    register_window.destroy()  # Close the registration window
    subprocess.run(["python", "main.py"])  # Return to main.py using subprocess


# Calculate window width and height
window_width = int(1600 * 0.8)
window_height = int(800 * 0.8)

# Create the registration window
register_window = tk.Tk()
register_window.title("Quick Cargo | Customer Registration")

# Set window size to fit the screen
register_window.geometry(f"{window_width}x{window_height}")

# Load and display the background image
# Replace "img1.jpeg" with the actual filename
bg_image = Image.open("img1.jpeg")
bg_image = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(register_window, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Add a stylish heading with a logo
# Background color for heading frame
heading_frame = tk.Frame(register_window, bg="white")
heading_frame.pack(fill="both", pady=20)  # Increase top padding

# Load and display the logo
# Replace "logo.png" with the actual filename
logo_image = Image.open("logo.png")
logo_image = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(heading_frame, image=logo_image)
logo_label.pack(side="left", padx=10)

# Create the heading label
heading_label = tk.Label(heading_frame, text="Quick Cargo", font=(
    "Helvetica", 30, "bold"), bg="white")
heading_label.pack(pady=15)

# Create labels, entry fields, and register button
username_label = tk.Label(register_window, text="Username:", font=(
    "Helvetica", 14))  # Increased font size
username_label.pack()

username_entry = tk.Entry(register_window, font=(
    "Helvetica", 14), width=20)  # Increased font size and width
username_entry.pack()

password_label = tk.Label(register_window, text="Password:", font=(
    "Helvetica", 14))  # Increased font size
password_label.pack()

# Increased font size and width
password_entry = tk.Entry(register_window, show="*",
                          font=("Helvetica", 14), width=20)
password_entry.pack()

first_name_label = tk.Label(register_window, text="First Name:", font=(
    "Helvetica", 14))  # Increased font size
first_name_label.pack()

first_name_entry = tk.Entry(register_window, font=(
    "Helvetica", 14), width=20)  # Increased font size and width
first_name_entry.pack()

last_name_label = tk.Label(register_window, text="Last Name:", font=(
    "Helvetica", 14))  # Increased font size
last_name_label.pack()

last_name_entry = tk.Entry(register_window, font=(
    "Helvetica", 14), width=20)  # Increased font size and width
last_name_entry.pack()

phone_label = tk.Label(register_window, text="Phone:",
                       font=("Helvetica", 14))  # Increased font size
phone_label.pack()

phone_entry = tk.Entry(register_window, font=(
    "Helvetica", 14), width=20)  # Increased font size and width
phone_entry.pack()

email_label = tk.Label(register_window, text="Email:",
                       font=("Helvetica", 14))  # Increased font size
email_label.pack()

email_entry = tk.Entry(register_window, font=(
    "Helvetica", 14), width=20)  # Increased font size and width
email_entry.pack()

register_button = tk.Button(register_window, text="Register", command=register_customer, font=(
    "Helvetica", 14), width=7)  # Increased font size and button width
register_button.pack()

# Create a frame for the "Existing Customer? Login" text and the link
login_frame = tk.Frame(register_window, bg="white")
login_frame.pack()

login_label = tk.Label(login_frame, text="Existing Customer? ", font=(
    "Helvetica", 14))  # Increased font size
login_label.pack(side="left")

login_link = tk.Label(login_frame, text="Login", fg="blue",
                      cursor="hand2", font=("Helvetica", 14))  # Increased font size
login_link.pack(side="left")
# Bind the click event to return_to_main()
login_link.bind("<Button-1>", lambda e: return_to_main())

# Start the GUI event loop for the registration window
register_window.mainloop()
