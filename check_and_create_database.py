import mysql.connector as mc

# Modify these variables to match your MySQL server configuration
username = "root"
password = ""
host = "localhost"
database = "cargo_database"

# Attempt to connect to the MySQL server
try:
    connection = mc.connect(user=username, password=password, host=host)
    cursor = connection.cursor()

    # Check if the database exists
    cursor.execute("SHOW DATABASES LIKE %s", (database,))
    result = cursor.fetchone()

    if result:
        print(f"The '{database}' database already exists. Skipping creation.")
    else:
        # If the database doesn't exist, run the script to create it
        print(f"The '{database}' database does not exist. Creating it...")
        import DATABASE_CARGOSERVICE

except mc.Error as error:
    print(f"Error: {error}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
