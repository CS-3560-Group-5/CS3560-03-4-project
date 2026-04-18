## machineSlot class
## 3-15-2026

# type hint imports
from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Union

if TYPE_CHECKING:
    from serviceWorker import serviceWorker
    from moneyHandler import moneyHandler

# actual imports
import datetime

# class to handle a restockRequest. keeps track of if it was resolved or not.
class restockRequest:
    # full init
    # *Doesnt make a new entry in assigned db table, only inits a class with this data. ID is assumed to correlate to a value inside the db table*
    def __init__(self, selfIDin: int, restockerIn : serviceWorker, moneyHandlerIn: moneyHandler, dateRequestedIn : datetime, dateResolvedIn : datetime, reasonIn: str) -> None:
        # used to track each specific ID for a request. generated automatically by system
        # TODO : fix this ID
        self.restockRequestID: int = selfIDin
        # used to track when a request was made. set when maintenanceRequest was made
        self.dateRequested: datetime = dateRequestedIn
        # used to track when a request is resolved. Is set to 1-1-1900 till resolved
        self.dateResolved: datetime = dateResolvedIn
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

    ## simple update methods
    def updateMaintenanceRequestID(self, newID : str) -> None:
        self.maintenanceRequestID = newID

    def updateDateRequested(self, newDate: datetime) -> None:
        self.dateRequested = newDate

    def updateDateResolved(self, newDate: datetime) -> None:
        self.dateResolved = newDate

    def updateReasonForRequest(self, newReason: str) -> None:
        self.reasonForRequest = newReason

    def updateAssignedRestocker(self, newRestocker: serviceWorker) -> None:
        self.assignedRestocker = newRestocker

    ## simple return methods
    def returnMaintenanceRequestID(self) -> str:
        return self.maintenanceRequestID

    def returnDateRequested(self) -> datetime:
        return self.dateRequested

    def returnDateResolved(self) -> datetime:
        return self.dateResolved

    def returnReasonForRequest(self) -> str:
        return self.reasonForRequest

    def returnAssignedRestocker(self) -> serviceWorker:
        return self.assignedRestocker
