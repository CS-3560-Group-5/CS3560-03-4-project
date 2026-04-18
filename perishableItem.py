## perishableItem class
## 4-10-2026

# type hint imports
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from restockRequest import restockRequest
    from machineSlot import machineSlot

# actual imports
import datetime

# tracks the date of expiration of an item in a shelf
class perishableItem:
    # constructor
    # *Doesnt make a new entry in assigned table, only inits a class with this data. ID is assumed to correlate to a value inside the db table*
    def __init__(self, selfID: int, slotIn: machineSlot, requestIn: restockRequest, expireIn: datetime, daysBeforeIn: int, slotPosIn: int) -> None:
        # self ID
        self.perishableItemID: int = selfID
        # the slot class this perishableitem is in
        self.slot: machineSlot = slotIn
        # the request this class can make
        self.request: restockRequest = requestIn
        # expiration date stored in datetime
        self.dateExpires: datetime = expireIn
        # how many days before something expires should it be restocked
        self.restockDaysBeforeExpire: int = daysBeforeIn
        # the location of the item in the slot. 
        self.slotPosition: int = slotPosIn
        
    ## use case methods 
    # function to check this expiration date to see if its passed its given restock day. If so, it creates a restock request.
    # this should be checked at the beginning of every day
    def checkExpiration(self) -> bool:
        #If the current date is after the expiration date, the item is expired.
        return datetime.datetime.now() > self.dateExpires

    ## simple update method
    def updatePerishableItemID(self, newID: int) -> None:
        self.perishableItemID = newID


    def updateSlot(self, newSlot: machineSlot) -> None:
        self.slot = newSlot

    def updateRequest(self, newRequest) -> None:
        self.request = newRequest

    def updateSlotPosition(self, newPosition) -> None:
        self.slotPosition = newPosition

    def updateDateExpires(self, expireNew: datetime) -> None:
        self.dateExpires = expireNew

    def updateRestockDaysBeforeExpire(self, newDays: int) -> None:
        self.restockDaysBeforeExpire = newDays

    ## simple return method
    def returnPerishableItemID(self) -> int:
        return self.perishableItemID
    
    def returnSlot(self) -> machineSlot:
        return self.slot
    
    def returnRequest(self) -> restockRequest:
        return self.request
    
    def returnSlotPosition(self) -> int:
        return self.slotPosition

    def returnDateExpires(self) -> datetime:
        return self.dateExpires

    def returnRestockDaysBeforeExpire(self) -> int:
        return self.restockDaysBeforeExpire


