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

    ## simple update methods
    def updateDateRequested(self, newDateRequested: str) -> None:
        self.dateRequested = newDateRequested

    def updateDateResolved(self, newDateResolved: str) -> None:
        self.dateResolved = newDateResolved

    def updateReasonForRequest(self, newReason: str) -> None:
        self.reasonForRequest = newReason

    def updateAssignedTechnician(self, newTech: serviceWorker) -> None:
        self.assignedTechnician = newTech

    def updateAssignedMachine(self, newMachine: machine) -> None:
        self.assignedMachine = newMachine

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