## perishableItem class
## 4-10-2026

# type hint imports
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from restockRequest import restockRequest
    from machineSlot import machineSlot

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

# tracks the date of expiration of an item in a shelf
class perishableItem:
    # constructor
    # *Doesnt make a new entry in assigned table, only inits a class with this data. ID is assumed to correlate to a value inside the db table*
    def __init__(self, selfID: int, slotIn: machineSlot, requestIn: restockRequest, expireIn: str, daysBeforeIn: int, slotPosIn: int) -> None:
        # self ID
        self.perishableItemID: int = selfID
        # the slot class this perishableitem is in
        self.slot: machineSlot = slotIn
        # the request this class can make
        self.request: restockRequest = requestIn
        # expiration date stored in datetime
        self.dateExpires: str = expireIn
        # how many days before something expires should it be restocked
        self.restockDaysBeforeExpire: int = daysBeforeIn
        # the location of the item in the slot. 
        self.slotPosition: int = slotPosIn
        
    ## use case methods 
    # function to check this expiration date to see if its passed its given restock day. If so, it creates a restock request.
    # this should be checked at the beginning of every day
    def checkExpiration(self) -> bool:
        #If the current date is after the expiration date, the item is expired.
        # TODO
        return datetime.datetime.now() > self.dateExpires

    ## simple update methods
    def updateSlot(self, newSlot: machineSlot) -> None:
        self.slot = newSlot
        cursor.execute("UPDATE `perishableitem` SET machineslotID = \"" + str(newSlot.returnNumpadCode()) + "\" WHERE perishableitemID = " + str(self.perishableItemID))
        machDB.commit()

    def updateRequest(self, newRequest: restockRequest) -> None:    # dont pass in None to this, use setRequestNull
        self.request = newRequest
        cursor.execute("UPDATE `perishableitem` SET restockrequestID = \"" + str(newRequest.returnRestockRequestID()) + "\" WHERE perishableitemID = " + str(self.perishableItemID))
        machDB.commit()

    def setRequestNull(self) -> None:
        self.request = None
        cursor.execute("UPDATE `perishableitem` SET restockrequestID = NULL WHERE perishableitemID = " + str(self.perishableItemID))
        machDB.commit()

    def updateSlotPosition(self, newPosition: int) -> None:      # doesnt check logic
        self.slotPosition = newPosition
        cursor.execute("UPDATE `perishableitem` SET slotPosition = \"" + str(newPosition) + "\" WHERE perishableitemID = " + str(self.perishableItemID))
        machDB.commit()

    def updateDateExpires(self, expireNew: str) -> None:
        self.dateExpires = expireNew
        cursor.execute("UPDATE `perishableitem` SET dateexpire = STR_TO_DATE(\"" + expireNew + "\",\"%m,%d,%Y\") WHERE perishableitemID = " + str(self.perishableItemID))
        machDB.commit()

    def updateRestockDaysBeforeExpire(self, newDays: int) -> None:
        self.restockDaysBeforeExpire = newDays
        cursor.execute("UPDATE `perishableitem` SET restockdaysbeforeexpire = \"" + str(newDays) + "\" WHERE perishableitemID = " + str(self.perishableItemID))
        machDB.commit()

    ## simple return method
    def returnPerishableItemID(self) -> int:
        return self.perishableItemID
    
    def returnSlot(self) -> machineSlot:
        return self.slot
    
    def returnRequest(self) -> restockRequest:
        return self.request
    
    def returnSlotPosition(self) -> int:
        return self.slotPosition

    def returnDateExpires(self) -> str:
        return self.dateExpires

    def returnRestockDaysBeforeExpire(self) -> int:
        return self.restockDaysBeforeExpire


