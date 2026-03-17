## machineSlot class
## 3-15-2026

# type hint imports
from __future__ import annotations
from typing import TYPE_CHECKING
from typing import List

if TYPE_CHECKING:
    from restockRequest import restockRequest
    from expirationDate import expirationDate

# actual imports

# class used to keep track of what product is in each of the vending machines slots. tracks that slots totals and vitals as well.
class machineSlot:
    # full constructor
    def __init__(self, numpadIn: int, countIn: int, maxIn: int, restockAtThresholdIn: float, expDatesIn: List[expirationDate]) -> None:
        # each slot has its own code that the machine uses. these can include numbers and letters. this is the code thats also used for customers to buy a product.
        self.numpadCode: str = numpadIn
        # how much of a product is in a slot
        self.productCount: int = countIn
        # the max amount of product that can fit in each slot
        self.maxAmount: int = maxIn
        # the threshold at which a product should be restocked. is a percentage
        self.restockAtThreshold: float = restockAtThresholdIn
        # the expiration dates for this slot. not always needed/can be blank because some products never expire (non-food items)
        self.expDates: List[expirationDate] = expDatesIn
        # the restock request for a machine slot. is made blank because its made later on once the restock threshold is hit
        self.request: restockRequest

    ## use case methods 
    # a function that runs to check if a machine slot has fallen below its product threshold. If so, it makes a restock request for itself
    # this function is ran every time a transaction is made
    def checkProductThreshold(self) -> None:
        # TODO : Write check threshold
        return NotImplemented
    
    # a function that checks all expiration dates for ones that need to be restocked
    def checkAllExpirationDates(self) -> None:
        # TODO : implement
        return NotImplemented

    ## update and return methods for list
    # append value to requests
    def appendExpDate(self, newExpDate: expirationDate) -> None:
        self.expDates.append(newExpDate)

    # replace value at index in expDates with expDate
    def replaceExpDate(self, newExpDate: expirationDate, index: int ) -> None:
        self.expDates[index] = newExpDate

    # return value from expDates list at index
    def returnExpDate(self, index: int) -> expirationDate:
        return self.expDates[index]
    
    # return entire expDates list
    def returnExpDates(self) -> List[expirationDate]:
        return self.expDates

    ## simple update methods [doesnt check for bounds!!]
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

