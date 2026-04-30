## coin class
## 4-6-2026
from __future__ import annotations
from unused.currency import currency
from typing import TYPE_CHECKING
import mysql.connector

if TYPE_CHECKING: 
    from unused.moneyHandler import moneyHandler

## setting up db cursor
machDB = mysql.connector.connect(
    host="localhost",
    user="interface",
    password="password",
    database = "vendingmachine"
)
cursor = machDB.cursor()

# coin class
# *Doesnt make a new entry in assigned table, only inits a class with this data. ID is assumed to correlate to a value inside the db table*
class coin(currency):
    def __init__(self, selfID: int, moneyHandlerIn: moneyHandler,  currAmtIn: int, maxAmtIn: int, worthIn: float) -> None:
        super().__init__(selfID, moneyHandlerIn, currAmtIn, worthIn)
        self.maxAmount: int = maxAmtIn

    # update and return functions
    def updateMaxAmount(self, newMax: int) -> None:
        self.maxAmount = newMax
        cursor.execute("UPDATE Currency SET maxamount = " + str(newMax) + " WHERE currencyID = " + str(self.currencyID))
        machDB.commit()

    def returnMaxAmount(self) -> int:
        return self.maxAmount
