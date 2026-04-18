## main method
## 4-18-2026
# imports
import mysql.connector
from typing import List
from machine import machine
from product import product
from maintenanceRequest import maintenanceRequest
from serviceWorker import serviceWorker
from cardSale import cardSale
from cashSale import cashSale
#from coin import coin
#from bill import bill

# setting up db cursor
machDB = mysql.connector.connect(
    host="localhost",
    user="interface",
    password="password",
    database = "vendingmachine"
)
cursor = machDB.cursor()

## setting up all classes
machineList = []
serviceWorkerList = []
maintenenceRequestList = []
productList = []
transactionList = []

# setting up machines based on db info
cursor.execute("SELECT * FROM machine")
all = cursor.fetchall()     # fetch info
for row in all:             # put every machine into memory with correct info
    machineList.append(machine(row[0], row[1], row[2], row[6], row[4], row[3], row[5]))

# setting up serviceWorkers based on db info
#  def __init__(self, idIn: str, nameIn: str, phoneIn: str, emailIn: str, companyIn: str
cursor.execute("SELECT * FROM serviceworker")
all = cursor.fetchall()
for row in all:
    serviceWorkerList.append(serviceWorker(row[0], machineList[row[1] - 1], row[2], row[3], row[4], row[5]))

# setting up maintenanceRequests based on db info
cursor.execute("SELECT * FROM maintenancerequest")
all = cursor.fetchall()
for row in all:
    maintenenceRequestList.append(maintenanceRequest(row[0], machineList[row[1] - 1], serviceWorkerList[row[2] - 1], row[3], row[4], row[5]))

# setting up product based on db info
cursor.execute("SELECT * FROM product")
all = cursor.fetchall()
for row in all:
    productList.append(product(row[0], machineList[row[1] - 1], row[2], row[3], row[4], row[5], row[6]))

# setting up transaction based on db info
cursor.execute("SELECT * FROM `transaction`")
all = cursor.fetchall()
#for row in all:
 #   transactionList.append(transaction(1,1,1,1,1,1))




















