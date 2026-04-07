## serviceWorker superclass
## Refactored to consolidate shared logic from restocker and technician
from __future__ import annotations
from typing import List
from abc import ABC, abstractmethod

class serviceWorker(ABC):
    def __init__(self, idIn: str, nameIn: str, phoneIn: str, emailIn: str, companyIn: str, requestsIn: List) -> None:
        self.employeeID: str = idIn
        self.name: str = nameIn
        self.phoneNumber: str = phoneIn
        self.email: str = emailIn
        self.company: str = companyIn
        self.requests: List = requestsIn

    @abstractmethod
    def resolveRequest(self, toResolve, dateResolved) -> None:
        pass

    def appendRequest(self, newRequest) -> None:
        self.requests.append(newRequest)

    def replaceRequest(self, newRequest, index: int) -> None:
        self.requests[index] = newRequest

    def returnRequest(self, index: int):
        return self.requests[index]

    def returnRequests(self) -> List:
        return self.requests

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
