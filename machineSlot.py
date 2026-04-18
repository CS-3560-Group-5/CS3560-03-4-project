## machineSlot class
## 4/10/2026

# type hint imports
from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from expirationDate import expirationDate

# actual import - needed at runtime for creating restock requests
from restockRequest import restockRequest

# tracks what product is in each vending machine slot, including count, thresholds, and expiration dates
class machineSlot:
    # full constructor
    def __init__(self, numpadIn: str, countIn: int, maxIn: int, restockAtThresholdIn: float, expDatesIn: List[expirationDate], posIn: int) -> None:
        # the code the customer enters to buy this product (e.g. "A1")
        self.numpadCode: str = numpadIn
        # current number of products in this slot
        self.productCount: int = countIn
        # max number of products this slot can hold
        self.maxAmount: int = maxIn
        # percentage threshold - if count/max falls at or below this, trigger a restock request
        self.restockAtThreshold: float = restockAtThresholdIn
        # list of expiration dates for products in this slot (empty if product never expires)
        self.expDates: List[expirationDate] = expDatesIn
        # the active restock request for this slot (set when threshold is hit)
        self.request: restockRequest = None
        # position of this slot in the machine, starts at 1
        self.slotPosition: int = posIn

    ## use case methods

    # checks if the product count has fallen at or below the restock threshold percentage
    # should be called every time a transaction is made
    def checkProductThreshold(self) -> None:
        # calculate current fill percentage and compare to threshold
        if self.productCount / self.maxAmount <= self.restockAtThreshold:
            # create a restock request for this slot (restocker assigned later by machine)
            self.request = restockRequest("Low stock", None, self)

    # checks all expiration dates in this slot and creates a restock request if any are expired
    # should be called at the start of each day
    def checkAllExpirationDates(self) -> None:
        for exp in self.expDates:
            # if any expiration date has passed, make a restock request and stop
            if exp.checkExpiration():
                self.request = restockRequest("Expired product", None, self)
                break

    ## expiration date list methods

    # add a new expiration date to this slot
    def appendExpDate(self, newExpDate: expirationDate) -> None:
        self.expDates.append(newExpDate)

    # replace the expiration date at a given index
    def replaceExpDate(self, newExpDate: expirationDate, index: int) -> None:
        self.expDates[index] = newExpDate

    # return the expiration date at a given index
    def returnExpDate(self, index: int) -> expirationDate:
        return self.expDates[index]

    # return the full expiration date list
    def returnExpDates(self) -> List[expirationDate]:
        return self.expDates

    ## simple update methods

    def updateNumpadCode(self, newCode: str) -> None:
        self.numpadCode = newCode

    def updateProductCount(self, newProductCount: int) -> None:
        self.productCount = newProductCount

    def updateMaxAmount(self, newMax: int) -> None:
        self.maxAmount = newMax

    def updateRestockAtThreshold(self, newThresh: float) -> None:
        self.restockAtThreshold = newThresh

    def updateRequest(self, newRequest: restockRequest) -> None:
        self.request = newRequest

    def updateSlotPosition(self, newPos: int) -> None:
        self.slotPosition = newPos

    ## simple return methods

    def returnNumpadCode(self) -> str:
        return self.numpadCode

    def returnProductCount(self) -> int:
        return self.productCount

    def returnMaxAmount(self) -> int:
        return self.maxAmount

    def returnRestockAtThreshold(self) -> float:
        return self.restockAtThreshold

    def returnRequest(self) -> restockRequest:
        return self.request

    def returnSlotPosition(self) -> int:
        return self.slotPosition
