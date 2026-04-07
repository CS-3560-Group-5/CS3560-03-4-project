## expirationDate class
## 3-15-2026

# type hint imports
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from restockRequest import restockRequest

# actual imports
import datetime

# tracks the date of expiration of an item in a shelf
class expirationDate:
    # constructor
    def __init__(self, expireIn: datetime,  daysBeforeExpireIn: int) -> None:
        # expiration date stored in datetime
        self.dateExpires: datetime = expireIn
        # how many days before something expires should it be restocked
        self.restockDaysBeforeExpire: int = daysBeforeExpireIn
        
    ## use case methods 
    # function to check this expiration date to see if its passed its given restock day. If so, it creates a restock request.
    # this should be checked at the beginning of every day
    def checkExpiration() -> bool:
        #If the current date is after the expiration date, the item is expired.
        return ((datetime.now() - self.dateExpires) > 0)

    ## simple update method
    def updateDateExpires(self, expireNew: datetime) -> None:
        self.dateExpires = expireNew

    def updateRestockDaysBeforeExpire(self, newDays: int) -> None:
        self.restockDaysBeforeExpire = newDays


    ## simple return method
    def returnDateExpires(self) -> datetime:
        return self.dateExpires

    def returnRestockDaysBeforeExpire(self) -> int:
        return self.restockDaysBeforeExpire


