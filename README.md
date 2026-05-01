# CS3560-03-4-project

# Team members
Nhat Pham, Preston Thronson, Ethan Juniper, Quan Cao, Khine Hein.
# Overview
A fully functional vending machine management system built with Python and MySQL. 
The application simulates a real-world vending machine environment; handling customer purchases, restocker inventory updates, maintenance tracking, and currency management. All backed by a normalized relational database.
# Tech Stack
We chose Python 3 for our language. We used Tkinter for the GUI. MySQL for our database, and mysql-connector-python for our database connector.
# Features
- **Customer interface** – browse available items, make purchases, and receive change
- **Restocker interface** – view and update product inventory levels
- **Maintenance interface** – track machine status and log service events
- **Currency management** – handles coin/bill input and change calculation
- **MySQL-backed persistence** – all transactions and inventory changes are stored in a relational database
# Database note
## Files rely on the included mysql database to be running and accessable.
Look in the sql file for the exported database in file "VendMachEntireDB". 
Run with MySQL and make sure server is running at location "localhost".
## All files also rely on there being a user within this database called "interface". 
This user needs to have admin level control over the db.
This users password must also be "password".
