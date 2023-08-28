import tkinter as tk
from tkinter import messagebox
import subprocess
import dbconnect  # Importing the dbconnect module

# Function to perform database login
def dblogin():
    user = username_entry.get()
    passw = password_entry.get()

    data = {}
    q = "SELECT * FROM login WHERE username=%s AND password=%s"
    values = (user, passw)
    res = dbconnect.select(q, values)  # Pass values to the select function

    if res:
        username = res[0]['username']
        if res[0]['user_type'] == 'admin':
            messagebox.showinfo("Login Successful", "Redirecting to admin page")
            window.destroy()  # Close the login window
            subprocess.run(["python", "admin.py", username])  # Run admin.py using subprocess
        elif res[0]['user_type'] == 'customer':
            messagebox.showinfo("Login Successful", "Redirecting to customer page")
            window.destroy()  # Close the login window
            subprocess.run(["python", "customer.py", username])  # Run customer.py using subprocess
        else:
            messagebox.showerror("Quick Cargo", "Please check the entered username or password and try again")
    else:
        messagebox.showerror("Quick Cargo", "Invalid Login Details!! Please try again")

# Function to open the registration window
def register_customer():
    window.destroy()  # Close the main login window
    subprocess.run(["python", "registercustomer.py"])  # Run register.py using subprocess

# Create the GUI window
window = tk.Tk()
window.title("Quick Cargo | Login")

# Set window size
window.geometry("400x300")  # Width x Height

# Add a stylish heading
heading_label = tk.Label(window, text="Quick Cargo", font=("Helvetica", 20, "bold"))
heading_label.pack(pady=20)

# Create labels, entry fields, and login button
username_label = tk.Label(window, text="Username:")
username_label.pack()

username_entry = tk.Entry(window, width=30)
username_entry.pack()

password_label = tk.Label(window, text="Password:")
password_label.pack()

password_entry = tk.Entry(window, show="*", width=30)
password_entry.pack()

login_button = tk.Button(window, text="Login", command=dblogin, width=10)
login_button.pack()


# Create a frame for the "New Customer? Register" text and the link
new_customer_frame = tk.Frame(window)
new_customer_frame.pack()

new_customer_label = tk.Label(new_customer_frame, text="New Customer?")
new_customer_label.pack(side="left")

register_link = tk.Label(new_customer_frame, text="Register", fg="blue", cursor="hand2")
register_link.pack(side="left")
register_link.bind("<Button-1>", lambda e: register_customer())  # Bind the click event to open_registration()

# Start the GUI event loop
window.mainloop()