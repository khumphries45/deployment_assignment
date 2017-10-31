**Name of Resource:** car

**ATTRIBUTES:**
* owner_name
* year
* make
* model
* color
* platenumber

**DATABASE SCHEMA:**

 ```CREATE TABLE cars (id INTEGER PRIMARY KEY, owner_name VARCHAR(255), year INTEGER, make VARCHAR(255), model VARCHAR(255), color VARCHAR(255), platenumber VARCHAR(255)); ```

** REST ENDPOINTS: **

List | Retrieve | Create | Delete | Update
---- | -------- | -------- | -------- | ------
GET  | GET      | POST     | DELETE   | PUT
/cars | /cars/id | /cars | /cars/id | /cars/id
