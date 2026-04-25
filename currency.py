## currency superclass
## Refactored to consolidate shared logic from coin and bill
# imports
from __future__ import annotations
import mysql.connector
from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING: 
    from moneyHandler import moneyHandler

## setting up db cursor
machDB = mysql.connector.connect(
    host="localhost",
    user="interface",
    password="password",
    database = "vendingmachine"
)
cursor = machDB.cursor()

# currency class
class currency(ABC):
    # constructor 
    # *Doesnt make a new entry in assigned table, only inits a class with this data. ID is assumed to correlate to a value inside the db table*
    def __init__(self, selfID: int, moneyHandlerIn: moneyHandler,  currAmtIn: int, worthIn: float) -> None:
        self.currencyID: int = selfID
        self.moneyHandlerAssigned: moneyHandler = moneyHandlerIn
        self.worth: float = worthIn
        self.currentAmount: int = currAmtIn

    # update and return functions. affects needed table values when done
    def updateWorth(self, newWorth: float) -> None:
        self.worth = newWorth
        cursor.execute("UPDATE Currency SET CurrencyWorth = " + str(round(newWorth, 2)) + " WHERE currencyID = " + str(self.currencyID))
        machDB.commit()

    def updateCurrentAmount(self, newAmt: int) -> None:
        self.currentAmount = newAmt
        cursor.execute("UPDATE Currency SET CurrentAmount = " + str(newAmt) + " WHERE currencyID = " + str(self.currencyID))
        machDB.commit()

    def updateMoneyHandlerAssigned(self, newHandler: moneyHandler) -> None:
        self.moneyHandlerAssigned = newHandler
        cursor.execute("UPDATE Currency SET CurrentAmount = " + str(newHandler.returnMoneyHandlerID()) + " WHERE currencyID = " + str(self.currencyID))
        machDB.commit()

    def returnWorth(self) -> float:
        return self.worth

    def returnCurrentAmount(self) -> int:
        return self.currentAmount
    
    def returnCurrencyID(self) -> int:
        return self.currencyID
    
    def returnMoneyHandlerAssigned(self) -> moneyHandler:
        return self.moneyHandlerAssigned
