## maintenance class
## 3-15-2026

# type hint imports
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from serviceWorker import serviceWorker
    from machine import machine

# actual imports
import datetime


# used to generate maintenance requests
class maintenanceRequest:

    # full contructor
    def __init__(self, selfIDin: int, machineIn : machine, techIn : serviceWorker, dateRequestedIn : datetime, dateResolvedIn : datetime, reason: str) -> None:
        # used to track each request
        self.maintenanceRequestID: int = selfIDin
        # used to track the machine this machine is with. only the machines ID
        self.assignedMachine: machine = machineIn
        # used to track when a request was made. set when maintenanceRequest was made
        self.dateRequested: datetime = dateRequestedIn
        # used to track when a request is resolved. Is set to null until resolved
        self.dateResolved: datetime = dateResolvedIn
        # used to record the reason for a request
        self.reasonForRequest: str = reason
        # used to track what technician goes with this maintenanceRequest. only the techs ID
        self.assignedTechnician: serviceWorker = techIn

    ## simple update methods
    def updateMaintenanceRequestID(self, newID: str) -> None:
        self.maintenanceRequestID = newID

    def updateDateRequested(self, newDateRequested: datetime) -> None:
        self.dateRequested = newDateRequested

    def updateDateResolved(self, newDateResolved: datetime) -> None:
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

    def returnDateRequested(self) -> datetime:
        return self.dateRequested

    def returnDateResolved(self) -> datetime:
        return self.dateResolved

    def returnReasonForRequest(self) -> str:
        return self.reasonForRequest

    def returnAssignedTechnician(self) -> serviceWorker:
        return self.assignedTechnician
    
    def returnAssignedMachine(self) -> machine:
        return self.assignedMachine