# cashSale class
# 3/15/2026

# type hint imports
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unused.transaction import transaction
    from unused.machine import machine

# actual imports
from unused.transaction import transaction
from unused.product import product
import mysql.connector

## setting up db cursor
machDB = mysql.connector.connect(
    host="localhost",
    user="interface",
    password="password",
    database = "vendingmachine"
)
cursor = machDB.cursor()

# class to implement cash transaction recording. inherits transaction class
class cashSale(transaction):
    # *Doesnt make a new entry in assigned db table, only inits a class with this data. ID is assumed to correlate to a value inside the db table*
    def __init__(self, saleNumberIn: int, itemIn: product, machineIn: machine, taxIn: float, saleDateTimeIn: str, cashGivenIn: float) -> None:
        # used to keep track of the money the customer gave to the machine
        self.cashGiven: float = cashGivenIn
        # used to record how much change was given back to the customer
        self.changeDispensed: float = round(cashGivenIn - (itemIn.returnPrice() + taxIn), 2)
        # call inherited init
        super().__init__(saleNumberIn, itemIn, machineIn, taxIn, saleDateTimeIn)

    ## simple update methods
    def updateCashGiven(self, newGiven: float) -> None:
        self.cashGiven = newGiven
        self.changeDispensed = round(newGiven - (self.item.price + self.tax), 2)
        cursor.execute("UPDATE `Transaction` SET cashgiven = " + str(round(newGiven, 2)) + " WHERE saleNumber = " + str(self.returnSaleNumber()))
        machDB.commit()

    def updateTax(self, newTax: float) -> None:
        self.tax = newTax
        self.changeDispensed = round(self.cashGiven - (self.item.price + newTax), 2)
        cursor.execute("UPDATE `Transaction` SET tax = " + str(round(newTax, 2)) + " WHERE saleNumber = " + str(self.returnSaleNumber()))
        machDB.commit()

    ## simple return methods
    def returnCashGiven(self) -> float:
        return self.cashGiven
    
    def returnChangeDispensed(self) -> float:
        return self.changeDispensed