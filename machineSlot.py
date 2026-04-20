## machineSlot class
## 4/10/2026

# type hint imports
from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from product import product
    from restockRequest import restockRequest


# actual imports
import mysql.connector
from restockRequest import restockRequest

## setting up db cursor
machDB = mysql.connector.connect(
    host="localhost",
    user="interface",
    password="password",
    database = "vendingmachine"
)
cursor = machDB.cursor()

# tracks what product is in each vending machine slot, including count, thresholds, and expiration dates
class machineSlot:
    # full constructor
    def __init__(self, numpadIn: str, productIn: product, restockRequestIn: restockRequest, countIn: int, maxIn: int, restockAtThresholdIn: float) -> None:
        # the code the customer enters to buy this product (e.g. "A1")
        self.numpadCode: str = numpadIn
        # the product at this slot
        self.productHeld: product = productIn
        # the restock request for this slot (set when threshold is hit)
        self.request: restockRequest = restockRequestIn
        # current number of products in this slot
        self.productCount: int = countIn
        # max number of products this slot can hold
        self.maxAmount: int = maxIn
        # percentage threshold - if count/max falls at or below this, trigger a restock request
        self.restockAtThreshold: float = restockAtThresholdIn

    ## use case methods

    # checks if the product count has fallen at or below the restock threshold percentage
    # should be called every time a transaction is made
    # TODO : Update to work with new code
    def checkProductThreshold(self) -> None:
        # calculate current fill percentage and compare to threshold
        if self.productCount / self.maxAmount <= self.restockAtThreshold:
            # create a restock request for this slot (restocker assigned later by machine)
            self.request = restockRequest("Low stock", None, self)

    # checks all expiration dates in this slot and creates a restock request if any are expired
    # should be called at the start of each day
    # TODO : Update to work with new code
    def checkAllExpirationDates(self) -> None:
        for exp in self.expDates:
            # if any expiration date has passed, make a restock request and stop
            if exp.checkExpiration():
                self.request = restockRequest("Expired product", None, self)
                break

    ## simple update methods
    def updateProduct(self, newProduct: product) -> None:
        self.productHeld = newProduct
        cursor.execute("UPDATE `machineSlot` SET productID = \"" + str(newProduct.returnProductID()) + "\" WHERE slotcode = \"" + str(self.numpadCode + "\""))
        machDB.commit()

    def updateProductCount(self, newProductCount: int) -> None:
        self.productCount = newProductCount
        cursor.execute("UPDATE `machineSlot` SET productcount = \"" + str(newProductCount) + "\" WHERE slotcode = \"" + str(self.numpadCode + "\""))
        machDB.commit()

    def updateMaxAmount(self, newMax: int) -> None:
        self.maxAmount = newMax
        cursor.execute("UPDATE `machineSlot` SET maxamount = \"" + str(newMax) + "\" WHERE slotcode = \"" + str(self.numpadCode + "\""))
        machDB.commit()

    def updateRestockAtThreshold(self, newThresh: float) -> None:
        self.restockAtThreshold = newThresh
        cursor.execute("UPDATE `machineSlot` SET restockatthreshold = \"" + str(round(newThresh, 2)) + "\" WHERE slotcode = \"" + str(self.numpadCode + "\""))
        machDB.commit()

    def updateRequest(self, newRequest: restockRequest) -> None:
        self.request = newRequest
        cursor.execute("UPDATE `machineSlot` SET restockRequestID = \"" + str(newRequest.returnRestockRequestID()) + "\" WHERE slotcode = \"" + str(self.numpadCode + "\""))
        machDB.commit()


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
    
    def returnProductHeld(self) -> product:
        return self.productHeld
