## technician class
## 3-15-2026
from __future__ import annotations
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from maintenanceRequest import maintenanceRequest
import datetime
from serviceWorker import serviceWorker

class technician(serviceWorker):
    def __init__(self, idIn: str, nameIn: str, phoneIn: str, emailIn: str, companyIn: str, requestsIn: List[maintenanceRequest]) -> None:
        super().__init__(idIn, nameIn, phoneIn, emailIn, companyIn, requestsIn)

    def resolveRequest(self, toResolve: maintenanceRequest, dateResolved: datetime) -> None:
        # TODO: implement
        return NotImplemented
