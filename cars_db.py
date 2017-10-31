import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class CarsDB:

    def __init__(self):
        self.connection = sqlite3.connect('cars_db.db')
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def createCar(self, owner_name, year, make, model, color, platenumber):
        self.cursor.execute(" INSERT INTO cars (owner_name, year, make, model, color, platenumber) VALUES (?, ?, ?, ?, ?, ?)", (owner_name, year, make, model, color, platenumber))
        self.connection.commit()


    def getCars(self):
        self.cursor.execute("SELECT * FROM cars")
        rows = self.cursor.fetchall()
        return rows

    def getCar(self, id):
        self.cursor.execute("SELECT * FROM cars WHERE id=?", (id,))
        self.connection.commit()
        row = self.cursor.fetchone()
        return row

    def getUpdate(self, id, owner_name, year, make, model, color, platenumber):
        self.cursor.execute("UPDATE cars SET owner_name=?, year=?, make=?, model=?, color=?, platenumber=? WHERE id=?", (owner_name, year, make, model, color, platenumber, id))
        self.connection.commit()
        return

    def getDelete(self, id):
        self.cursor.execute("DELETE FROM cars WHERE id=?", (id,))
        self.connection.commit()
        return
