## moneyHandler class
## 3-16-2026

# type hint imports
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from machine import machine

# actual import
import mysql.connector


## setting up db cursor
machDB = mysql.connector.connect(
    host="localhost",
    user="interface",
    password="password",
    database = "vendingmachine"
)
cursor = machDB.cursor()

# this class handles all the the money in a vending machine
class moneyHandler:
    # init function for all values
    # *Doesnt make a new entry in assigned db table, only inits a class with this data. ID is assumed to correlate to a value inside the db table*
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

    def updateAssignedMachine(self, newMachine: machine) -> None:
        self.assignedMachine = newMachine
        cursor.execute("UPDATE `moneyhandler` SET machineID = " + str(newMachine.returnMachineID()) + " WHERE moneyHandlerID = " + str(self.moneyHandlerID))
        machDB.commit()

    def updateBillRestockMaxThreshold(self, newMaxThresh: float) -> None:
        self.billRestockMaxThreshold = newMaxThresh
        cursor.execute("UPDATE `moneyhandler` SET billrestockMaxthreshold = " + str(newMaxThresh) + " WHERE moneyHandlerID = " + str(self.moneyHandlerID))
        machDB.commit()

    def updateBillMaxAmount(self, newBillMax: int) -> None:
        self.billMaxAmount = newBillMax
        cursor.execute("UPDATE `moneyhandler` SET billmaxamount = " + str(newBillMax) + " WHERE moneyHandlerID = " + str(self.moneyHandlerID))
        machDB.commit()

    def updateCoinRestockMinThreshold(self, newMinThresh: float) -> None:
        self.coinRestockMinThreshold = newMinThresh
        cursor.execute("UPDATE `moneyhandler` SET coinrestockminthreshold = " + str(newMinThresh) + " WHERE moneyHandlerID = " + str(self.moneyHandlerID))
        machDB.commit()

    def updateCoinRestockMaxThreshold(self, newMaxThresh: float) -> None:
        self.coinRestockMaxThreshold = newMaxThresh
        cursor.execute("UPDATE `moneyhandler` SET coinrestockmaxthreshold = " + str(newMaxThresh) + " WHERE moneyHandlerID = " + str(self.moneyHandlerID))
        machDB.commit()

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



