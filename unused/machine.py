## machine class
## 3-15-2026

# Note : This project is using pythons type hint functionality. this is purely for commenting purposes and DOES NOT DO ANYTHING except for adding notation. This will not enforce types or error check for you.
# type hint imports
from __future__ import annotations
from typing import TYPE_CHECKING
from typing import List

if TYPE_CHECKING:      # This if statement is needed at the top of each file to avoid circular imports made by type hinting. Put all imported classes for type hinting within this if statement
    from unused.serviceWorker import serviceWorker
    from unused.transaction import transaction
    from unused.product import product
    from unused.maintenanceRequest import maintenanceRequest
    from unused.cardSale import cardSale
    from unused.cashSale import cashSale
    from unused.coin import coin
    from unused.bill import bill

# actual imports
import mysql.connector
import datetime

## setting up db cursor
machDB = mysql.connector.connect(
    host="localhost",
    user="interface",
    password="password",
    database = "vendingmachine"
)
cursor = machDB.cursor()

# handles the tracking of when maintenance requests are sent, via the service date aproaching or the machine having a malfunction
# also connects classes
class machine:
    # basic contructor. takes in basic info about machine. also sets up all links to other classes
    # *Doesnt make a new entry in assigned db table, only inits a class with this data. ID is assumed to correlate to a value inside the db table*
    def __init__(self, machIDIn: int, addressIn: str, modelNumIn: str, maxSlotsIn: int, lastServicedIn: str, currStateIn: str, daysBetweenSerIn: int) -> None:
        ## basic attributes
        # stores database ID for machine
        self.machID: int = machIDIn
        # stores the full address of the machine
        self.address: str = addressIn
        # stores the model number of the machine
        self.modelNumber: str = modelNumIn
        # stores the maximum amount of slots the machine has to fit products in
        self.maxProductSlots: int = maxSlotsIn
        # stores the current operational state of the machine
        self.currentState: str = currStateIn
        # stores the date that the machine was last serviced
        self.dateLastServiced: str = lastServicedIn
        # stores the days between each machine service
        self.daysbetweenServices: int = daysBetweenSerIn

    ## Use case functions
    # TODO : Update to work with new code
    # function called when a machine malfunction is detected. this creates a new maintenanceRequest for one of the machines assigned technicians
    # currently assigns to the technician with the least current requests
    def malfunctionDetected(self, techAssigned: serviceWorker) -> None:
        #Initializing the values to find the technician with the least requests
        currentMin = len(self.technicians[i].returnRequest())
        minInd = 0

        #Traversing through the list to find the technician with the least requests
        for i in range(len(self.technicians)):
            if len(self.technicians[i].returnRequest()) < currentMin:
                minInd = i
                currentMin = len(self.technicians[i].returnRequest())
        
        #Creating a new request and appending it to both the machine's and the technician's request lists
        newReq = maintenanceRequest("Malfunction", self.technicians[i])
        self.technicians[i].appendRequest(newReq)
        self.requests.append(newReq)
    
    # function called to check scheduled service date. if service date has been reached, a new maintenanceRequest is made for a technician
    # TODO : Update to work with new code
    # this should be ran at the beginning of each day
    # checks and assigns technician similar to the above function
    def checkServiceDate(self, techAssigned: serviceWorker) -> None:
        
        currentDate = datetime.now()
        timeSinceLast = int(currentDate - self.dateLastServiced)
        
        if timeSinceLast >= self.daysBetweenServices:
            #Initializing the values to find the technician with the least requests
            self.currentState = "Requires Service"
            currentMin = len(self.technicians[i].returnRequest())
            minInd = 0
    
            #Traversing through the list to find the technician with the least requests
            for i in range(len(self.technicians)):
                if len(self.technicians[i].returnRequest()) < currentMin:
                    minInd = i
                    currentMin = len(self.technicians[i].returnRequest())
        
            #Creating a new request and appending it to both the machine's and the technician's request lists
            newReq = maintenanceRequest("Service", self.technicians[i])
            self.technicians[i].appendRequest(newReq)
            self.requests.append(newReq)
    
    # functions called to record a transaction, depending on the type
    # TODO : Update to work with new code
    def recordTransaction(self, productPurchased: product, sale: cardSale) -> None:
        self.transactions.append(sale)

    # TODO : Update to work with new code
    def recordTransaction(self, productPurchased: product, sale: cashSale) -> None:
        self.transactions.append(sale)
        
    # function called to update machine inventory
    def updateInventory(self, productChanged: product) -> None:
        # TODO : implement
        return NotImplemented
    
    # function called to update the amount of cash in the machine
    # a list of the bills and coins are given. these are referenced against the moneyHandlers bills and coins. If they match, their values are added together. If not, error thrown
    # can be positive or negative coin/bill amounts. Error will be thrown if the amount of bills/coins the machine can hold is exceeded.
    def updateCash(self, coinUpdate: List[coin], billUpdate: List[bill]) -> None:
        # TODO : implement
        return NotImplemented
    
    # "Admin updates machine information" case is handled with the simple update methods below
    ## simple update methods
    def updateAddress(self, newAddress: str) -> None:
        self.address = newAddress
        cursor.execute("UPDATE `machine` SET address = \"" + str(newAddress) + "\" WHERE machineID = \"" + str(self.machID) + "\"")
        machDB.commit()
    
    def updateModelNumber(self, newModelNum: str) -> None:
        self.modelNumber = newModelNum
        cursor.execute("UPDATE `machine` SET modelNumber = \"" + str(newModelNum) + "\" WHERE machineID = \"" + str(self.machID) + "\"")
        machDB.commit()

    def updateMaxProductSlots(self, newMaxSlots: int) -> None:
        self.maxProductSlots = newMaxSlots
        cursor.execute("UPDATE `machine` SET maxproductslots = \"" + str(newMaxSlots) + "\" WHERE machineID = \"" + str(self.machID) + "\"")
        machDB.commit()

    def updateCurrentState(self, newState: str) -> None:
        self.currentState = newState
        cursor.execute("UPDATE `machine` SET currentstate = \"" + str(newState) + "\" WHERE machineID = \"" + str(self.machID) + "\"")
        machDB.commit()
    
    def updateDateLastServiced(self, newLastServiced: str) -> None:
        self.dateLastServiced = newLastServiced
        cursor.execute("UPDATE `machine` SET datelastserviced = STR_TO_DATE(\"" + newLastServiced + "\",\"%m,%d,%Y\") WHERE machineID = " + str(self.machID))
        machDB.commit()
        

    def updateDaysBetweenServices(self, newDaysBetween: int) -> None:
        self.daysbetweenServices = newDaysBetween
        cursor.execute("UPDATE `machine` SET daysbetweenservices = \"" + str(newDaysBetween) + "\" WHERE machineID = \"" + str(self.machID) + "\"")
        machDB.commit()

    ## simple return methods
    def returnMachineID(self) -> int:
        return self.machID

    def returnAddress(self) -> str:
        return self.address
    
    def returnModelNumber(self) -> str:
        return self.modelNumber

    def returnMaxProductSlots(self) -> int:
        return self.maxProductSlots
    
    def returnCurrentState(self) -> str:
        return self.currentState
    
    def returnDateLastServiced(self) -> str:
        return self.dateLastServiced
    
    def returnDaysBetweenServices(self) -> int:
        return self.daysbetweenServices
