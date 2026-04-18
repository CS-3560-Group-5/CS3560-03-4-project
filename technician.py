## technician class
## 4-6-2026

from __future__ import annotations
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from maintenanceRequest import maintenanceRequest
    from machine import machine
import datetime
from serviceWorker import serviceWorker

class technician(serviceWorker):
    # constructor - passes all args up to serviceWorker
    #  def __init__(self, idIn: str, nameIn: str, phoneIn: str, emailIn: str, companyIn: str
    def __init__(self, idIn: str, machineAssignedIn: machine, nameIn: str, phoneIn: str, emailIn: str, companyIn: str) -> None:
        super().__init__(idIn, machineAssignedIn, nameIn, phoneIn, emailIn, companyIn)

    # finds the matching request by ID and stamps it with the resolved date
    def resolveRequest(self, toResolve: maintenanceRequest, dateResolved: datetime) -> None:
        for i in range(len(self.requests)):
            if self.requests[i].returnMaintenanceRequestID() == toResolve.returnMaintenanceRequestID():
                self.requests[i].updateDateResolved(dateResolved)
                break
