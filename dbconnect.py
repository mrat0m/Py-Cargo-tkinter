import mysql.connector as mc

# password = "root"
password = ""
database = "cargo_database"

def select(q, values):
    c = mc.connect(user="root", password=password, host="localhost", database=database)
    cur = c.cursor(dictionary=True)
    cur.execute(q, values)  # Pass values to the execute method
    result = cur.fetchall()
    cur.close()
    c.close()
    return result

def update(q):
    c = mc.connect(user="root", password=password, host="localhost", database=database)
    cur = c.cursor(dictionary=True)
    cur.execute(q)
    c.commit()  # Commit the changes using the database connection 'c'
    result = cur.rowcount
    cur.close()
    c.close()
    return result

def delete(q):
    c = mc.connect(user="root", password=password, host="localhost", database=database)
    cur = c.cursor(dictionary=True)
    cur.execute(q)
    c.commit()  # Commit the changes using the database connection 'c'
    result = cur.rowcount
    c.close()
    c.close()
    return result

def insert(q, values):
    c = mc.connect(user="root", password=password, host="localhost", database=database)
    cur = c.cursor(dictionary=True)
    cur.execute(q, values)
    c.commit()  # Commit the changes using the database connection 'c'
    result = cur.lastrowid
    cur.close()
    c.close()
    return result
