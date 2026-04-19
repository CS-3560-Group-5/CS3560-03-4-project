## maintenance class
## 3-15-2026

# type hint imports
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from serviceWorker import serviceWorker
    from machine import machine

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

# used to generate maintenance requests
class maintenanceRequest:

    # full contructor
    # *Doesnt make a new entry in assigned db table, only inits a class with this data. ID is assumed to correlate to a value inside the db table*
    def __init__(self, selfIDin: int, machineIn : machine, techIn : serviceWorker, dateRequestedIn : str, dateResolvedIn : str, reason: str) -> None:
        # used to track each request
        self.maintenanceRequestID: int = selfIDin
        # used to track the machine this machine is with. only the machines ID
        self.assignedMachine: machine = machineIn
        # used to track when a request was made. set when maintenanceRequest was made
        self.dateRequested: str = dateRequestedIn
        # used to track when a request is resolved. Is set to null until resolved
        self.dateResolved: str = dateResolvedIn
        # used to record the reason for a request
        self.reasonForRequest: str = reason
        # used to track what technician goes with this maintenanceRequest. only the techs ID
        self.assignedTechnician: serviceWorker = techIn

    ## functions
    def updateDateResolved(self, newDateResolved: str) -> None:# expects date to be passed as numbers in the string form "month,day,year" like "1,1,2000"
        self.dateResolved = newDateResolved
        cursor.execute("UPDATE `maintenancerequest` SET dateResolved = STR_TO_DATE(\"" + newDateResolved + "\",\"%m,%d,%Y\") WHERE MaintencanceRequestID = " + str(self.maintenanceRequestID))
        machDB.commit()
    
    # changes dateResolved to the current date
    def markAsResolved(self) -> None:
        date = datetime.datetime.now()
        self.updateDateResolved(date.strftime("%m") + "," + date.strftime("%d") + "," + date.strftime("%Y"))

    # changes dateResolved to None/Null
    def markAsUnresolved(self) -> None:
        cursor.execute("UPDATE `maintenancerequest` SET dateresolved = NULL WHERE MaintencanceRequestID = " + str(self.maintenanceRequestID))
        machDB.commit()

    ## simple update methods
    def updateDateRequested(self, newDateRequested: str) -> None:       # expects date to be passed as numbers in the string form "month,day,year" like "1,1,2000"
        self.dateRequested = newDateRequested
        cursor.execute("UPDATE `maintenancerequest` SET daterequested = STR_TO_DATE(\"" + newDateRequested + "\",\"%m,%d,%Y\") WHERE MaintencanceRequestID = " + str(self.maintenanceRequestID))
        machDB.commit()

    def updateReasonForRequest(self, newReason: str) -> None:
        self.reasonForRequest = newReason
        cursor.execute("UPDATE `maintenancerequest` SET reasonforrequest = \"" + str(newReason) + "\" WHERE MaintencanceRequestID = " + str(self.maintenanceRequestID))
        machDB.commit()

    def updateAssignedTechnician(self, newTech: serviceWorker) -> None:
        self.assignedTechnician = newTech
        cursor.execute("UPDATE `maintenancerequest` SET serviceworkerID = " + str(newTech.returnEmployeeID()) + " WHERE MaintencanceRequestID = " + str(self.maintenanceRequestID))
        machDB.commit()

    def updateAssignedMachine(self, newMachine: machine) -> None:
        self.assignedMachine = newMachine
        cursor.execute("UPDATE `maintenancerequest` SET machineID = " + str(newMachine.returnMachineID()) + " WHERE MaintencanceRequestID = " + str(self.maintenanceRequestID))
        machDB.commit()

    ## simple return methods
    def returnMaintenanceRequestID(self) -> str:
        return self.maintenanceRequestID

    def returnDateRequested(self) -> str:
        return self.dateRequested

    def returnDateResolved(self) -> str:
        return self.dateResolved

    def returnReasonForRequest(self) -> str:
        return self.reasonForRequest

    def returnAssignedTechnician(self) -> serviceWorker:
        return self.assignedTechnician
    
    def returnAssignedMachine(self) -> machine:
        return self.assignedMachine