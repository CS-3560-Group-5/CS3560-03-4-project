## restocker class
## 3-16-2026
from __future__ import annotations
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from restockRequest import restockRequest
import datetime
from serviceWorker import serviceWorker

class restocker(serviceWorker):
    def __init__(self, idIn: str, nameIn: str, phoneIn: str, emailIn: str, companyIn: str, requestsIn: List[restockRequest]) -> None:
        super().__init__(idIn, nameIn, phoneIn, emailIn, companyIn, requestsIn)

    def resolveRequest(self, toResolve: restockRequest, dateResolved: datetime) -> None:
        # TODO: implement
        return NotImplemented
