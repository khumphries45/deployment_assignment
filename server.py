from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json
from cars_db import CarsDB
import sys
import sqlite3
from http import cookies
from session_store_example import SessionStore
gSessionStore = SessionStore()
from passlib.hash import bcrypt


class MyHandler(BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_cookie()
        self.send_header("Access-Control-Allow-Origin",
        self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        BaseHTTPRequestHandler.end_headers(self)


    def do_OPTIONS(self):
        self.load_session()
        self.send_response(200)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Header", "Content-type")
        self.end_headers()
        return

    def do_GET(self):
        self.load_session()
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
        self.load_session()
        print("POST path: ", self.path)
        if self.path == "/cars":
            self.HandleCarCreation()
        elif self.path == "/sessions":
            self.HandleSessionCreation()
        elif self.path == "/users":
            self.HandleUserCreation()
        else:
            self.Handle404()

    def do_PUT(self):
        self.load_session()
        print("POST path: ", self.path)
        if self.path.startswith("/cars/"):
            c = self.path.split("/")
            handlec=(c[2])
            self.HandleCarUpdate(handlec)
        else:
            self.Handle404()

    def do_DELETE(self):
        self.load_session()
        print("POST path: ", self.path)
        if self.path.startswith("/cars/"):
            c = self.path.split("/")
            handlec=(c[2])
            self.HandleCarDeletion(handlec)
        else:
            self.Handle404()



    def HandleCarList(self):
        if "userId" not in self.session:
            self.Handle401()
            return
        db = CarsDB()
        cars = db.getCars()
        json_string = json.dumps(cars)
        print("JSON String", json_string)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json_string, "utf-8"))
        return

    def HandleCarRetrieve(self,id):
        if "userId" not in self.session:
            self.Handle401()
            return
        db = CarsDB()
        car = db.getCar(id)
        if car == None:
            self.Handle404()
            return
        json_string = json.dumps(car)
        print("JSON String", json_string)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json_string, "utf-8"))
        return

    def HandleCarCreation(self):
        if "userId" not in self.session:
            self.Handle401()
            return
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
        self.end_headers()
        self.wfile.write(bytes("Created", "utf-8"))
        return

    def HandleCarUpdate(self, id):
        if "userId" not in self.session:
            self.Handle401()
            return
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
        self.end_headers()
        self.wfile.write(bytes("Updated", "utf-8"))
        return

    def HandleCarDeletion(self,id):
        if "userId" not in self.session:
            self.Handle401()
            return
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
        self.end_headers()
        self.wfile.write(bytes(json_string, "utf-8"))
        return



    def load_session(self):
        # load the cookie object
        self.load_cookie()
        # find if session_id in cookies?
        if "sessionId" in self.cookie:
            sessionId = self.cookie["sessionId"].value
            sessionData = gSessionStore.getSession(sessionId)
            # find session_id in session store
            if sessionData is not None:
                # load / return the session updatemake
                self.session = sessionData
            else:
                # create new session_id
                sessionId = gSessionStore.createSession()
                # assign session_id in cookie
                self.cookie["sessionId"] = sessionId
                # create empty session data in session store
                self.session = gSessionStore.getSession(sessionId)
        else:
            sessionId = gSessionStore.createSession()
            # assign session_id in cookie
            self.cookie["sessionId"] = sessionId
            # create empty session data in session store
            self.session = gSessionStore.getSession(sessionId)


    def load_cookie(self):
        if "Cookie" in self.headers:
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            self.cookie = cookies.SimpleCookie()

    def send_cookie(self):
        for morsel in self.cookie.values():
            #all of the values that this cookie has
            self.send_header("Set-Cookie", morsel.OutputString())


    def HandleSessionCreation(self):
        length = int(self.headers["Content-length"])
        body = self.rfile.read(length).decode("utf-8")
        parsed_body = parse_qs(body)
        db = CarsDB()

        email = parsed_body['email'][0]
        password = parsed_body['password'][0]

        user=db.getUserbyEmail(email)
        if user != None:
            print(user)
            if bcrypt.verify(password, user["encrypted_password"]) == True:
                self.session["userId"] = user["id"]
                self.send_response(201)
                self.send_cookie()
                self.end_headers()
                self.wfile.write(bytes(json.dumps(user), "utf-8"))
            else:
                self.Handle401()
        else:
            self.Handle401()

        return

    #def getUsers(self):
        #if "userId" in self.session:
            #then do whatever you were doing
        #else:
            #self.Handle404()

    def HandleUserCreation(self):
        length = int(self.headers["Content-length"])
        body = self.rfile.read(length).decode("utf-8")
        parsed_body = parse_qs(body)
        db = CarsDB()

        fname = parsed_body['fname'][0]
        lname = parsed_body['lname'][0]
        email = parsed_body['email'][0]
        password = parsed_body['password'][0]

        user = db.getUserbyEmail(email)

        if user == None:


            db.createUser(fname, lname, email, password)

            self.send_response(201)
            self.end_headers()
            self.wfile.write(bytes("Created", "utf-8"))

        else:
            self.Handle422()


    def Handle401(self):
        self.send_response(401)
        self.end_headers()
        self.wfile.write(bytes("Unauthorized", "utf-8"))


    def Handle404(self):
        self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes("Not Found", "utf-8"))

    def Handle422(self):
        self.send_response(422)
        self.end_headers()
        self.wfile.write(bytes("Unprocessable", "utf-8"))

def main():
    listen = ("0.0.0.0", 8080)
    server = HTTPServer(listen, MyHandler)

    print("Listening...")
    server.serve_forever()

main()
