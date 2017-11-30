**Name of Resource:** car

**CAR ATTRIBUTES:**
* owner_name
* year
* make
* model
* color
* platenumber


**USER ATTRIBUTES:**
* fname
* lname
* email
* encrypted_password

**CAR DATABASE SCHEMA:**

 ```CREATE TABLE cars (id INTEGER PRIMARY KEY, owner_name VARCHAR(255), year INTEGER, make VARCHAR(255), model VARCHAR(255), color VARCHAR(255), platenumber VARCHAR(255)); ```

 **USERS DATABASE SCHEMA:**

 ```CREATE TABLE users (id INTEGER PRIMARY KEY, fname VARCHAR(255), lname VARCHAR(255), email VARCHAR(255), encrypted_password VARCHAR(255));```

** REST ENDPOINTS: **

List | Retrieve | Create | Delete | Update
---- | -------- | -------- | -------- | ------
GET  | GET      | POST     | DELETE   | PUT
/cars | /cars/id | /cars | /cars/id | /cars/id
      |         | /users |          |
      |         | /sessions |       |

**Password Hashing Method:** passlib bcrypt library

```encrypted_password = bcrypt.encrypt(password)```

```if bcrypt.verify(password, user["encrypted_password"]) == True:```
