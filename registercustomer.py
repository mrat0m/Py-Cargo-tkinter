# registercustomer.py
import tkinter as tk
from tkinter import messagebox
import dbconnect  # Importing the dbconnect module
import subprocess

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
    subprocess.run(["python", "customer.py", username])  # Run customer.py using subprocess

# Function to go back to the main login window (main.py)
def return_to_main():
    register_window.destroy()  # Close the registration window
    subprocess.run(["python", "main.py"])  # Return to main.py using subprocess

# Create the registration window
register_window = tk.Tk()
register_window.title("Quick Cargo | Customer Registration")

# Set window size
register_window.geometry("400x400")  # Width x Height

# Create labels, entry fields, and register button
username_label = tk.Label(register_window, text="Username:")
username_label.pack()

username_entry = tk.Entry(register_window, width=30)
username_entry.pack()

password_label = tk.Label(register_window, text="Password:")
password_label.pack()

password_entry = tk.Entry(register_window, show="*", width=30)
password_entry.pack()

first_name_label = tk.Label(register_window, text="First Name:")
first_name_label.pack()

first_name_entry = tk.Entry(register_window, width=30)
first_name_entry.pack()

last_name_label = tk.Label(register_window, text="Last Name:")
last_name_label.pack()

last_name_entry = tk.Entry(register_window, width=30)
last_name_entry.pack()

phone_label = tk.Label(register_window, text="Phone:")
phone_label.pack()

phone_entry = tk.Entry(register_window, width=30)
phone_entry.pack()

email_label = tk.Label(register_window, text="Email:")
email_label.pack()

email_entry = tk.Entry(register_window, width=30)
email_entry.pack()

register_button = tk.Button(register_window, text="Register", command=register_customer, width=10)
register_button.pack()

# Create a frame for the "Existing Customer? Login" text and the link
login_frame = tk.Frame(register_window)
login_frame.pack()

login_label = tk.Label(login_frame, text="Existing Customer? ")
login_label.pack(side="left")

login_link = tk.Label(login_frame, text="Login", fg="blue", cursor="hand2")
login_link.pack(side="left")
login_link.bind("<Button-1>", lambda e: return_to_main())  # Bind the click event to return_to_main()

# Start the GUI event loop for the registration window
register_window.mainloop()
