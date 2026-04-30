## machineSlot class
## 3-15-2026

# type hint imports
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unused.serviceWorker import serviceWorker
    from unused.moneyHandler import moneyHandler

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


# class to handle a restockRequest. keeps track of if it was resolved or not.
class restockRequest:
    # full init
    # *Doesnt make a new entry in assigned db table, only inits a class with this data. ID is assumed to correlate to a value inside the db table*
    def __init__(self, selfIDin: int, restockerIn : serviceWorker, moneyHandlerIn: moneyHandler, dateRequestedIn : str, dateResolvedIn : str, reasonIn: str) -> None:
        # used to track each specific ID for a request. generated automatically by system
        # TODO : fix this ID
        self.restockRequestID: int = selfIDin
        # used to track when a request was made. set when maintenanceRequest was made
        self.dateRequested: str = dateRequestedIn
        # used to track when a request is resolved. Is set to 1-1-1900 till resolved
        self.dateResolved: str = dateResolvedIn
        # used to record the reason for a request
        self.reasonForRequest: str = reasonIn
        # the assigned restocker for this request
        self.assignedRestocker: serviceWorker = restockerIn
        # the moneyhandler of the assigned machine
        self.assignedMoneyHandler: moneyHandler = moneyHandlerIn


    ## use case methods
    # function to update the inventory of a request to its new levels. This is done once a request has been resolved
    def updateRequestInventory(self) -> None:
        # TODO : implement
        return NotImplemented
    
    # changes dateResolved to the current date
    def markAsResolved(self) -> None:
        date = datetime.datetime.now()
        self.updateDateResolved(date.strftime("%m") + "," + date.strftime("%d") + "," + date.strftime("%Y"))

    # changes dateResolved to None/Null
    def markAsUnresolved(self) -> None:
        cursor.execute("UPDATE `restockrequest` SET dateresolved = NULL WHERE RestockRequestID = " + str(self.restockRequestID))
        machDB.commit()

    ## simple update methods
    def updateDateRequested(self, newDate: str) -> None:        # expects date to be passed as numbers in the string form "month,day,year" like "1,1,2000"
        self.dateRequested = newDate
        cursor.execute("UPDATE `restockrequest` SET daterequested = STR_TO_DATE(\"" + newDate + "\",\"%m,%d,%Y\") WHERE RestockRequestID = " + str(self.restockRequestID))
        machDB.commit()

    def updateDateResolved(self, newDate: str) -> None:         # expects date to be passed as numbers in the string form "month,day,year" like "1,1,2000"
        self.dateResolved = newDate
        cursor.execute("UPDATE `restockrequest` SET dateresolved = STR_TO_DATE(\"" + newDate + "\",\"%m,%d,%Y\") WHERE RestockRequestID = " + str(self.restockRequestID))
        machDB.commit()

    def updateReasonForRequest(self, newReason: str) -> None:
        self.reasonForRequest = newReason
        cursor.execute("UPDATE `restockrequest` SET reasonforrequest = \"" + str(newReason) + "\" WHERE RestockRequestID = " + str(self.restockRequestID))
        machDB.commit()

    def updateAssignedRestocker(self, newRestocker: serviceWorker) -> None:
        self.assignedRestocker = newRestocker
        cursor.execute("UPDATE `restockrequest` SET serviceworkerID = \"" + str(newRestocker.returnEmployeeID()) + "\" WHERE RestockRequestID = " + str(self.restockRequestID))
        machDB.commit()

    ## simple return methods
    def returnRestockRequestID(self) -> str:
        return self.restockRequestID
    
    def returnAssignedMoneyHandler(self) -> moneyHandler:
        return self.assignedMoneyHandler

    def returnDateRequested(self) -> str:
        return self.dateRequested

    def returnDateResolved(self) -> str:
        return self.dateResolved

    def returnReasonForRequest(self) -> str:
        return self.reasonForRequest

    def returnAssignedRestocker(self) -> serviceWorker:
        return self.assignedRestocker
