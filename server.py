from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json
from cars_db import CarsDB
import sys
import sqlite3

class MyHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Header", "Content-type")
        self.end_headers()
        return

    def do_GET(self):
        print("GET path: ", self.path)
        if self.path == "/cars":
            self.HandleCarList()
        elif self.path.startswith("/cars/"):
            c = self.path.split("/")
            handlec=(c[2])
            self.HandleCarRetrieve(handlec)
        else:
            self.Handle404()

    def do_POST(self):
        print("POST path: ", self.path)
        if self.path == "/cars":
            self.HandleCarCreation()
        else:
            self.Handle404()

    def do_PUT(self):
        print("POST path: ", self.path)
        if self.path.startswith("/cars/"):
            c = self.path.split("/")
            handlec=(c[2])
            self.HandleCarUpdate(handlec)
        else:
            self.Handle404()

    def do_DELETE(self):
        print("POST path: ", self.path)
        if self.path.startswith("/cars/"):
            c = self.path.split("/")
            handlec=(c[2])
            self.HandleCarDeletion(handlec)
        else:
            self.Handle404()

    def HandleCarList(self):
        db = CarsDB()
        cars = db.getCars()
        json_string = json.dumps(cars)
        print("JSON String", json_string)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(bytes(json_string, "utf-8"))
        return

    def HandleCarRetrieve(self,id):
        db = CarsDB()
        car = db.getCar(id)
        if car == None:
            self.Handle404()
            return
        json_string = json.dumps(car)
        print("JSON String", json_string)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(bytes(json_string, "utf-8"))
        return

    def HandleCarCreation(self):
        length = int(self.headers["Content-length"])
        body = self.rfile.read(length).decode("utf-8")
        parsed_body = parse_qs(body)
        db = CarsDB()

        owner_name = parsed_body['owner_name'][0]
        year = parsed_body['year'][0]
        make = parsed_body['make'][0]
        model = parsed_body['model'][0]
        color = parsed_body['color'][0]
        platenumber = parsed_body['platenumber'][0]

        db.createCar(owner_name,year,make,model,color,platenumber)

        self.send_response(201)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(bytes("Created", "utf-8"))
        return

    def HandleCarUpdate(self, id):
        length = int(self.headers["Content-length"])
        body = self.rfile.read(length).decode("utf-8")
        parsed_body = parse_qs(body)
        db = CarsDB()

        if db.getCar(id) == None:
            self.Handle404()
            return

        owner_name = parsed_body['owner_name'][0]
        year = parsed_body['year'][0]
        make = parsed_body['make'][0]
        model = parsed_body['model'][0]
        color = parsed_body['color'][0]
        platenumber = parsed_body['platenumber'][0]

        db.getUpdate(id,owner_name,year,make,model,color,platenumber)

        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(bytes("Updated", "utf-8"))
        return

    def HandleCarDeletion(self,id):
        db = CarsDB()
        car = db.getCar(id)
        if car == None:
            self.Handle404()
            return
        deleted = db.getDelete(id)
        json_string = json.dumps(deleted)
        print("JSON String", json_string)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(bytes(json_string, "utf-8"))
        return

    def Handle404(self):
        self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes("Not Found", "utf-8"))

def main():
    listen = ("0.0.0.0", 8080)
    server = HTTPServer(listen, MyHandler)

    print("Listening...")
    server.serve_forever()

main()
