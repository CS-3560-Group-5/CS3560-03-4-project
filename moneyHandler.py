## moneyHandler class
## 3-16-2026

# type hint imports
from __future__ import annotations
from typing import TYPE_CHECKING
from typing import List

if TYPE_CHECKING:
    from machine import machine

# actual imports

# this class handles all the the money in a vending machine
class moneyHandler:
    # init function for all values
    def __init__(self, selfID: int, machineIn: machine, billMaxThreshIn: float, billMaxAmtIn: int, coinMaxThreshIn: float, coinMinThreshIn: float) -> None:
        # this handlers ID
        self.moneyHandlerID: int = selfID
        # assigned machine
        self.assignedMachine: machine = machineIn
        # holds the max threshold for a bill restock. this should be a percentage, which is used to calculate the bounds dynamically from billMax
        # there is no min threshold for a bill restock because change is given in coins only. there can be no bills in the machine and it can still operate with the correct change.
        self.billRestockMaxThreshold: float = billMaxThreshIn
        # holds the max bill amount, which is the maximum amount of bills the machine can hold.
        self.billMaxAmount: int = billMaxAmtIn
        # holds the min threshhold for a coin restock. this should be a percentage, which is used to calculate the bounds dynamically from a coins coinMax
        self.coinRestockMinThreshold: float = coinMinThreshIn
        # holds the max threshhold for a coin restock. this should be a percentage, which is used to calculate the bounds dynamically from a coins coinMax
        self.coinRestockMaxThreshold: float = coinMaxThreshIn

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

    ## simple update methods [doesnt check for bounds!!]
    def updateMoneyHandlerID(self, newID) -> None:
        self.moneyHandlerID = newID

    def updateAssignedMachine(self, newMachine: machine) -> None:
        self.assignedMachine = newMachine

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
    
    def returnMoneyHandlerID(self) -> int:
        return self.moneyHandlerID
    
    def returnAssignedMachine(self) -> machine:
        return self.assignedMachine



