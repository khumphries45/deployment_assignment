import sqlite3
from passlib.hash import bcrypt
import os
import psycopg2
import psycopg2.extras
import urllib.parse



class CarsDB:

    def __init__(self):
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

        self.connection = psycopg2.connect(
            cursor_factory=psycopg2.extras.RealDictCursor,
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )

        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

        #deployment
    def createCarTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS cars (id SERIAL PRIMARY KEY, owner_name VARCHAR(255), year VARCHAR(255), make VARCHAR(255), model VARCHAR(255), color VARCHAR(255), platenumber VARCHAR(255))")
        self.connection.commit()

    def createCar(self, owner_name, year, make, model, color, platenumber):
        self.cursor.execute(" INSERT INTO cars (owner_name, year, make, model, color, platenumber) VALUES (%s, %s, %s, %s, %s, %s)", (owner_name, year, make, model, color, platenumber))
        self.connection.commit()


    def getCars(self):
        self.cursor.execute("SELECT * FROM cars")
        rows = self.cursor.fetchall()
        return rows

    def getCar(self, id):
        self.cursor.execute("SELECT * FROM cars WHERE id=%s", (id,))
        self.connection.commit()
        row = self.cursor.fetchone()
        return row

    def getUpdate(self, id, owner_name, year, make, model, color, platenumber):
        self.cursor.execute("UPDATE cars SET owner_name=%s, year=%s, make=%s, model=%s, color=%s, platenumber=%s WHERE id=%s", (owner_name, year, make, model, color, platenumber, id))
        self.connection.commit()
        return

    def getDelete(self, id):
        self.cursor.execute("DELETE FROM cars WHERE id=%s", (id,))
        self.connection.commit()
        return

    def createUser(self, fname, lname, email, password):
        encrypted_password = bcrypt.encrypt(password)
        self.cursor.execute(" INSERT INTO users (fname,lname,email,encrypted_password) VALUES (%s, %s, %s, %s)", (fname,lname,email,encrypted_password))
        self.connection.commit()

    #deployment for User TABLE
    def createUserTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, fname VARCHAR(255), lname VARCHAR(255), email VARCHAR(255), encrypted_password VARCHAR(255))")
        self.connection.commit()


    def getUserbyEmail(self, email):
        self.cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        row = self.cursor.fetchone()
        return row


    def getUserbyID(self, id):
        self.cursor.execute("SELECT * FROM users where id=%s", (id,))
        row = self.cursor.fetchone()
        return row
