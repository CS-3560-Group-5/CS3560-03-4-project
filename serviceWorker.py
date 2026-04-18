## serviceWorker superclass
from __future__ import annotations
from typing import List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from maintenanceRequest import maintenanceRequest
    from machine import machine
import datetime

class serviceWorker():
    # *Doesnt make a new entry in assigned db table, only inits a class with this data. ID is assumed to correlate to a value inside the db table*
    def __init__(self, idIn: str, assignedMachineIn: machine, nameIn: str, workerTypeIn: str, phoneIn: str, emailIn: str, companyIn: str) -> None:
        self.employeeID: str = idIn
        self.workerType: str = workerTypeIn
        self.assignedMachine: machine = assignedMachineIn
        self.name: str = nameIn
        self.phoneNumber: str = phoneIn
        self.email: str = emailIn
        self.company: str = companyIn

    # functions
    # finds the matching request by ID and stamps it with the resolved date
    def resolveRequest(self, toResolve: maintenanceRequest, dateResolved: datetime) -> None:
        for i in range(len(self.requests)):
            if self.requests[i].returnMaintenanceRequestID() == toResolve.returnMaintenanceRequestID():
                self.requests[i].updateDateResolved(dateResolved)
                break

    # simple update methods
    def updateEmployeeID(self, newID: str) -> None:
        self.employeeID = newID

    def updateName(self, newName: str) -> None:
        self.name = newName

    def updatePhoneNumber(self, newPhone: str) -> None:
        self.phoneNumber = newPhone

    def updateEmail(self, newEmail: str) -> None:
        self.email = newEmail

    def updateCompany(self, newCompany: str) -> None:
        self.company = newCompany

    def updateMachine(self, newMachine: machine) -> None:
        self.assignedMachine = newMachine

    def updateWorkerType(self, newType) -> None:
        self.workerType = newType

    # simple return methods
    def returnEmployeeID(self) -> str:
        return self.employeeID

    def returnName(self) -> str:
        return self.name

    def returnPhoneNumber(self) -> str:
        return self.phoneNumber

    def returnEmail(self) -> str:
        return self.email

    def returnCompany(self) -> str:
        return self.company
    
    def returnAssignedMachine(self) -> machine:
        return self.assignedMachine
    
    def returnWorkerType(self) -> str:
        return self.workerType