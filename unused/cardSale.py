## cardSale class
## 3/15/2026

# type hint imports
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unused.product import product
    from unused.machine import machine

# actual imports
from unused.transaction import transaction
import mysql.connector

## setting up db cursor
machDB = mysql.connector.connect(
    host="localhost",
    user="interface",
    password="password",
    database = "vendingmachine"
)
cursor = machDB.cursor()

# class to implement card transaction recording. inherits transaction class
class cardSale(transaction):
    # init function
    # *Doesnt make a new entry in assigned db table, only inits a class with this data. ID is assumed to correlate to a value inside the db table*
    def __init__(self, saleNumberIn: int, itemIn: product, machineIn: machine, taxIn: float, saleDateTimeIn: str, feeIn: float, accountIn: str) -> None:
        # used to keep track of the fee charged to the customers card (if any)
        self.cardFee: float = feeIn
        # used to record what account was charged for the transaction
        self.accountCharged: str = accountIn
        # call inherited init
        super().__init__(saleNumberIn, itemIn, machineIn, taxIn, saleDateTimeIn)

    ## simple update methods
    def updateCardFee(self, newFee: float) -> None:
        self.cardFee = newFee
        cursor.execute("UPDATE `Transaction` SET cardfee = " + str(round(newFee, 2)) + " WHERE saleNumber = " + str(self.returnSaleNumber()))
        machDB.commit()

    def updateAccountCharged(self, newAccount: str) -> None:
        self.accountCharged = newAccount
        cursor.execute("UPDATE `Transaction` SET accountcharged = " + str(newAccount) + " WHERE saleNumber = " + str(self.returnSaleNumber()))
        machDB.commit()

    def updateTax(self, newTax: float) -> None:
        self.tax = newTax
        cursor.execute("UPDATE `Transaction` SET tax = " + str(round(newTax, 2)) + " WHERE saleNumber = " + str(self.returnSaleNumber()))
        machDB.commit()

    ## simple return methods
    def returnCardFee(self) -> float:
        return self.cardFee

    def returnAccountCharged(self) -> str:
        return self.accountCharged