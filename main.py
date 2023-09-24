import tkinter as tk
from tkinter import messagebox
import subprocess
import dbconnect  # Importing the dbconnect module
from PIL import Image, ImageTk  # Import PIL for image handling
# import ctypes

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
            messagebox.showinfo("Login Successful",
                                "Redirecting to admin page")
            window.destroy()  # Close the login window
            # Run admin.py using subprocess
            subprocess.run(["python", "admin.py", username])
        elif res[0]['user_type'] == 'customer':
            messagebox.showinfo("Login Successful",
                                "Redirecting to customer page")
            window.destroy()  # Close the login window
            # Run customer.py using subprocess
            subprocess.run(["python", "customer.py", username])
        else:
            messagebox.showerror(
                "Quick Cargo", "Please check the entered username or password and try again")
    else:
        messagebox.showerror(
            "Quick Cargo", "Invalid Login Details!! Please try again")

# Function to open the registration window


def register_customer():
    window.destroy()  # Close the main login window
    # Run register.py using subprocess
    subprocess.run(["python", "registercustomer.py"])

# Get the screen width and height
# user32 = ctypes.windll.user32
# screen_width = user32.GetSystemMetrics(0)
# screen_height = user32.GetSystemMetrics(1)

# Calculate window width and height
# window_width = int(screen_width * 0.8)
# window_height = int(screen_height * 0.8)


# Calculate window width and height
window_width = int(1600 * 0.8)
window_height = int(800 * 0.8)

# Create the GUI window
window = tk.Tk()
window.title("Quick Cargo | Login")

# Set window size to fit the screen
window.geometry(f"{window_width}x{window_height}")

# Load and display the background image
# Replace "img1.jpeg" with the actual filename
bg_image = Image.open("img1.jpeg")
bg_image = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(window, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Add a stylish heading with a logo
# Background color for heading frame
heading_frame = tk.Frame(window, bg="white")
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

# Create a frame to center the login form
login_frame = tk.Frame(window, bg="white")
login_frame.pack(pady=20)

# Create labels, entry fields, and login button
username_label = tk.Label(
    login_frame, text="Username:", font=("Helvetica", 14))
username_label.pack()

username_entry = tk.Entry(login_frame, font=("Helvetica", 14), width=30)
username_entry.pack()

password_label = tk.Label(
    login_frame, text="Password:", font=("Helvetica", 14))
password_label.pack()

password_entry = tk.Entry(login_frame, show="*",
                          font=("Helvetica", 14), width=30)
password_entry.pack()

login_button = tk.Button(login_frame, text="Login",
                         command=dblogin, width=7, font=("Helvetica", 14))
login_button.pack()

# Create a frame for the "New Customer? Register" text and the link
new_customer_frame = tk.Frame(window, bg="white")
new_customer_frame.pack()

new_customer_label = tk.Label(
    new_customer_frame, text="New Customer?", font=("Helvetica", 14))
new_customer_label.pack(side="left")

register_link = tk.Label(new_customer_frame, text="Register",
                         fg="blue", cursor="hand2", font=("Helvetica", 14))
register_link.pack(side="left")
# Bind the click event to open_registration()
register_link.bind("<Button-1>", lambda e: register_customer())

# Start the GUI event loop
window.mainloop()
