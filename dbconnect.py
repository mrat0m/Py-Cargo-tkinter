import mysql.connector

password = ""
database = "cargo_database"

def select(q, values):
    cnx = mysql.connector.connect(user="root", password=password, host="localhost", database=database)
    cur = cnx.cursor(dictionary=True)
    cur.execute(q, values)  # Pass values to the execute method
    result = cur.fetchall()
    cur.close()
    cnx.close()
    return result

def update(q):
    cnx = mysql.connector.connect(user="root", password=password, host="localhost", database=database)
    cur = cnx.cursor(dictionary=True)
    cur.execute(q)
    cnx.commit()
    result = cur.rowcount
    cur.close()
    cnx.close()
    return result

def delete(q):
    cnx = mysql.connector.connect(user="root", password=password, host="localhost", database=database)
    cur = cnx.cursor(dictionary=True)
    cur.execute(q)
    cnx.commit()
    result = cur.rowcount
    cur.close()
    cnx.close()
    return result

def insert(q, values):
    cnx = mysql.connector.connect(user="root", password=password, host="localhost", database=database)
    cur = cnx.cursor(dictionary=True)
    cur.execute(q, values)
    cnx.commit()
    result = cur.lastrowid
    cur.close()
    cnx.close()
    return result