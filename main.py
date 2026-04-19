## main method
## 4-18-2026
## imports
import mysql.connector
from machine import machine
from product import product
from maintenanceRequest import maintenanceRequest
from restockRequest import restockRequest
from serviceWorker import serviceWorker
from cardSale import cardSale
from cashSale import cashSale
from machineSlot import machineSlot
from moneyHandler import moneyHandler
from coin import coin
from bill import bill
from perishableItem import perishableItem

## setting up db cursor
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
maintenanceRequestList = []
productList = []
cardSaleList = []
cashSaleList = []
machineSlotList = []
restockRequestList = []
moneyHandlerList = []
perishableItemList = []
billList = []
coinList = []

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
    serviceWorkerList.append(serviceWorker(row[0], machineList[row[1] - 1], row[2], row[3], row[4], row[5], row[6]))

# setting up maintenanceRequests based on db info
cursor.execute("SELECT * FROM maintenancerequest")
all = cursor.fetchall()
for row in all:
    maintenanceRequestList.append(maintenanceRequest(row[0], machineList[row[1] - 1], serviceWorkerList[row[2] - 1], row[3], row[4], row[5]))

# setting up product based on db info
cursor.execute("SELECT * FROM product")
all = cursor.fetchall()
for row in all:
    productList.append(product(row[0], machineList[row[1] - 1], row[2], row[3], row[4], row[5], row[6]))

# setting up transaction (cardsale and cashsale) based on db info
cursor.execute("SELECT * FROM `transaction`")
all = cursor.fetchall()
for row in all:
    if row[5] != None:      # if cashGiven is none/null, then its a cardsale not a cash sale
        cardSaleList.append(cardSale(row[0], productList[row[1] - 1], row[2], row[3], row[4], row[5], row[6]))
    else:
        cashSaleList.append(cashSale(row[0], productList[row[1] - 1], row[2], row[3], row[4], row[7]))

# setting up moneyHandlers
cursor.execute("SELECT * FROM moneyhandler")
all = cursor.fetchall()
for row in all:
    moneyHandlerList.append(moneyHandler(row[0], machineList[row[1] - 1], row[2], row[3], row[4], row[5]))


# setting up restockrequests
cursor.execute("SELECT * FROM `restockrequest`")
all = cursor.fetchall()
for row in all:
    if row[2] != None:      # if the request has no moneyhandler, we don't pass in a money handler from the list
        restockRequestList.append(restockRequest(row[0], serviceWorkerList[row[1] - 1], moneyHandlerList[row[2] - 1], row[3], row[4], row[5]))
    else:
        restockRequestList.append(restockRequest(row[0], serviceWorkerList[row[1] - 1], None, row[3], row[4], row[5]))

# setting up machineSlot
cursor.execute("SELECT * FROM MachineSlot")
all = cursor.fetchall()
for row in all:
    if row[1] != None and row[2] != None:
        machineSlotList.append(machineSlot(row[0], productList[row[1] - 1], restockRequestList[row[2] - 1], row[3], row[4], row[5]))
    elif row[1] != None and row[2] == None:
        machineSlotList.append(machineSlot(row[0], productList[row[1] - 1], None, row[3], row[4], row[5]))
    else:
        machineSlotList.append(machineSlot(row[0], None, None, row[3], row[4], row[5]))
  
# setting up perishableItem
cursor.execute("SELECT * FROM perishableitem")
all = cursor.fetchall()
for row in all:
    # look for the correct index of the machineSlot object. Needed because this key is a string and not an int like the others
    index = 0
    for slot in machineSlotList:
        if row[1] == slot.returnNumpadCode():
            break
        index += 1

    if row[2] != None:
        perishableItemList.append(perishableItem(row[0], machineSlotList[index], restockRequestList[row[2] - 1], row[3], row[4], row[5]))
    else:
        perishableItemList.append(perishableItem(row[0], machineSlotList[index], None, row[3], row[4], row[5]))

# setting up currency (coins and bills)
cursor.execute("SELECT * FROM currency")
all = cursor.fetchall()
for row in all:
    if row[3] != None:
        coinList.append(coin(row[0], row[1], row[2], row[3], row[4]))
    else:
        billList.append(bill(row[0], row[1], row[2], row[4]))


# test
machineList[0].updateDaysBetweenServices(1234565555)
