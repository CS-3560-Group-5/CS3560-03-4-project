## technician class
## 3-15-2026

# type hint imports
from __future__ import annotations
from typing import TYPE_CHECKING
from typing import List

if TYPE_CHECKING:
    from maintenanceRequest import maintenanceRequest

# actual imports
import datetime

# this class is used to track the technicians for a vending machine
class technician:
    # full constructor
    def __init__(self, idIn: str, nameIn: str, phoneIn: str, emailIn: str, companyIn: str, requestsIn: List[maintenanceRequest]) -> None:
        # employee ID is a unique ID for each employee. this ID is given by the admin
        self.employeeID: str = idIn
        # employee full name 
        self.name: str = nameIn
        # employee phone number
        self.phoneNumber: str = phoneIn
        # employee email
        self.email: str = emailIn
        # employee company (who they work for. you sometimes are hiring outside help for this)
        self.company: str = companyIn
        # the technicians assigned maintenanceRequests, in list form
        self.requests: List[maintenanceRequest] = requestsIn

    ## use case methods
    # function to declare a technicians maintenanceRequest as resolved (updating its resolved date)
    def closeMaintenanceTicket(self, toResolve: maintenanceRequest, dateResolved: datetime) -> None:
        # TODO : implement
        return NotImplemented

    ## update and return methods for lists
    # append value to requests
    def appendRequest(self, newRequest: maintenanceRequest) -> None:
        self.requests.append(newRequest)

    # replace value at index in requests with request
    def replaceRequest(self, newRequest: maintenanceRequest, index: int) -> None:
        self.requests[index] = newRequest

    # return value from requsts list at index
    def returnRequest(self, index: int) -> maintenanceRequest:
        return self.requests[index]

    # return entire requests list
    def returnRequests(self) -> List[maintenanceRequest]:
        return self.requests

    ## simple update methods
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

    ## simple return methods
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
