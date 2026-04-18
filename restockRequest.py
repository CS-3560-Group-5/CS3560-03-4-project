## machineSlot class
## 3-15-2026

# type hint imports
from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Union

if TYPE_CHECKING:
    from restocker import restocker
    from moneyHandler import moneyHandler
    from machineSlot import machineSlot
    from expirationDate import expirationDate

# actual imports
import datetime

# class to handle a restockRequest. keeps track of if it was resolved or not.
class restockRequest:
    # full init
    def __init__(self, reasonIn: str, restockerIn: restocker, requestCallerIn: Union[moneyHandler, machineSlot, expirationDate]) -> None:
        # used to track each specific ID for a request. generated automatically by system
        # TODO : fix this ID
        self.maintenanceRequestID: str = "change me"
        # used to track when a request was made. set when maintenanceRequest was made
        self.dateRequested: datetime = datetime.datetime.now()
        # used to track when a request is resolved. Is set to 1-1-1900 till resolved
        self.dateResolved: datetime = datetime.datetime(1900, 1, 1)
        # used to record the reason for a request
        self.reasonForRequest: str = reasonIn
        # the assigned restocker for this request
        self.assignedRestocker: restocker = restockerIn
        # the specific class that the request is related to. can be moneyHandler, machineSlot, or expirationDate
        self.requestCaller: Union[moneyHandler, machineSlot, expirationDate] = requestCallerIn

    ## use case methods
    # function to update the inventory of a request to its new levels. This is done once a request has been resolved
    def updateRequestInventory(self) -> None:
        # TODO : implement
        return NotImplemented

    ## simple update methods
    def updateMaintenanceRequestID(self, newID : str) -> None:
        self.maintenanceRequestID = newID

    def updateDateRequested(self, newDate: datetime) -> None:
        self.dateRequested = newDate

    def updateDateResolved(self, newDate: datetime) -> None:
        self.dateResolved = newDate

    def updateReasonForRequest(self, newReason: str) -> None:
        self.reasonForRequest = newReason

    def updateAssignedRestocker(self, newRestocker: restocker) -> None:
        self.assignedRestocker = newRestocker

    def updateRequestCaller(self, newCaller: Union[moneyHandler, machineSlot, expirationDate]) -> None:
        self.requestCaller = newCaller

    ## simple return methods
    def returnMaintenanceRequestID(self) -> str:
        return self.maintenanceRequestID

    def returnDateRequested(self) -> datetime:
        return self.dateRequested

    def returnDateResolved(self) -> datetime:
        return self.dateResolved

    def returnReasonForRequest(self) -> str:
        return self.reasonForRequest

    def returnAssignedRestocker(self) -> restocker:
        return self.assignedRestocker
