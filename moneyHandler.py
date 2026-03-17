## moneyHandler class
## 3-16-2026

# type hint imports
from __future__ import annotations
from typing import TYPE_CHECKING
from typing import List

if TYPE_CHECKING:
    from coin import coin
    from bill import bill
    from restockRequest import restockRequest

# actual imports

# this class handles all the the money in a vending machine
class moneyHandler:
    # init function for all values
    def __init__(self, billMaxThreshIn: float, billMaxAmtIn: int, coinMinThreshIn: float, coinMaxThreshIn: float, coinsIn: List[coin], billsIn: List[bill], requestsIn: List[restockRequest]) -> None:
        # holds the max threshold for a bill restock. this should be a percentage, which is used to calculate the bounds dynamically from billMax
        # there is no min threshold for a bill restock because change is given in coins only. there can be no bills in the machine and it can still operate with the correct change.
        self.billRestockMaxThreshold: float = billMaxThreshIn
        # holds the max bill amount, which is the maximum amount of bills the machine can hold.
        self.billMaxAmount: int = billMaxAmtIn
        # holds the min threshhold for a coin restock. this should be a percentage, which is used to calculate the bounds dynamically from a coins coinMax
        self.coinRestockMinThreshold: float = coinMinThreshIn
        # holds the max threshhold for a coin restock. this should be a percentage, which is used to calculate the bounds dynamically from a coins coinMax
        self.coinRestockMaxThreshold: float = coinMaxThreshIn
        # init list of coins with given array
        self.coins: List[coin] = coinsIn
        # init list of bills with given array
        self.bills: List[bill] = billsIn
        # init list of restock requests
        self.requests: List[restockRequest] = requestsIn

    # init function for all values minus all arrays
    def __init__(self, billMaxThreshIn: float, billMaxAmtIn: int, coinMinThreshIn: float, coinMaxThreshIn: float) -> None:
        self.billRestockMaxThreshold: float = billMaxThreshIn
        self.billMaxAmount: int = billMaxAmtIn
        self.coinRestockMinThreshold: float = coinMinThreshIn
        self.coinRestockMaxThreshold: float = coinMaxThreshIn
        # init all lists to empty
        self.coins: List[coin] = []
        self.bills: List[bill] = []
        self.requests: List[restockRequest] = []

    ## use case functions
    # function to check if the bill storage has reached its capacity. If so, it makes a new restock request
    # this should be ran any time any bill is updated
    def checkBillCapacity(self) -> None:
        # TODO : implement
        return NotImplemented

    # function to check if the change storage has reached its minimum/maximum. If so, it makes a new restock request
    # a different restock request is made for each individual coin that has reached its min/max
    # this should be ran any time any coin is updated
    def checkChangeLevels(self) -> None:
        # TODO : implement
        return NotImplemented
    
    # function to return the total amount of money currently in the machine
    def getTotalProfit(self) -> float:
        # TODO : implement
        return NotImplemented

    ## update and return methods for lists
    # append value to coins
    def appendCoin(self, newCoin: coin) -> None:
        self.coins.append(newCoin)

    # replace value at index in coins with coin
    def replaceCoin(self, newCoin: coin, index: int) -> None:
        self.coins[index] = newCoin

    # return value from coin list at index
    def returnCoin(self, index: int) -> coin:
        return self.coins[index]

    # return entire coin list
    def returnCoins(self) -> List[coin]:
        return self.coins

    # append value to bills
    def appendCoin(self, newBill: bill) -> None:
        self.bills.append(newBill)

    # replace value at index in bills with bill
    def replaceBill(self, newBill: bill, index: int) -> None:
        self.bills[index] = newBill

    # return value from coin list at index
    def returnBill(self, index: int) -> bill:
        return self.bills[index]
    
    # return entire bill list
    def returnBills(self) -> List[bill]:
        return self.bills
    
    # append value to requests
    def appendRequest(self, newRequest: restockRequest) -> None:
        self.requests.append(newRequest)

    # replace value at index in requests with request
    def replaceRequest(self, newRequest: restockRequest, index: int) -> None:
        self.requests[index] = newRequest

    # return value from requsts list at index
    def returnRequest(self, index: int) -> restockRequest:
        return self.requests[index]

    # return entire requests list
    def returnRequests(self) -> List[restockRequest]:
        return self.requests

    ## simple update methods [doesnt check for bounds!!]
    def updateBillRestockMaxThreshold(self, newMaxThresh: float) -> None:
        self.billRestockMaxThreshold = newMaxThresh

    def updateBillMaxAmount(self, newBillMax: int) -> None:
        self.billMaxAmount = newBillMax

    def updateCoinRestockMinThreshold(self, newMinThresh: float) -> None:
        self.coinRestockMinThreshold = newMinThresh

    def updateCoinRestockMaxThreshold(self, newMaxThresh: float) -> None:
        self.coinRestockMaxThreshold = newMaxThresh

    ## simple return methods
    def returnBillRestockMaxThreshold(self) -> float:
        return self.billRestockMaxThreshold

    def returnBillMaxAmount(self) -> int:
        return self.billMaxAmount

    def returnCoinRestockMinThreshold(self) -> float:
        return self.coinRestockMinThreshold

    def returnCoinRestockMaxThreshold(self) -> float:
        return self.coinRestockMaxThreshold



