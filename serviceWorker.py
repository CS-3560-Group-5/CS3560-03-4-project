## serviceWorker superclass
from __future__ import annotations
from typing import List
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from machine import machine

class serviceWorker(ABC):
    @abstractmethod
    def __init__(self, idIn: str, assignedMachineIn: machine, nameIn: str, phoneIn: str, emailIn: str, companyIn: str) -> None:
        self.employeeID: str = idIn
        self.assignedMachine: machine = assignedMachineIn
        self.name: str = nameIn
        self.phoneNumber: str = phoneIn
        self.email: str = emailIn
        self.company: str = companyIn

    # functions
    def resolveRequest(self, toResolve, dateResolved) -> None:
        pass

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
