# cashSale class
# 3/15/2026

# type hint imports
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from transaction import transaction
    from machine import machine
    import datetime

# actual imports
from transaction import transaction
from product import product

# class to implement cash transaction recording. inherits transaction class
class cashSale(transaction):

    def __init__(self, saleNumberIn: int, itemIn: product, machineIn: machine, taxIn: float, saleDateTimeIn: datetime, cashGivenIn: float) -> None:
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

    ## simple return methods
    def returnCashGiven(self) -> float:
        return self.cashGiven
    
    def returnChangeDispensed(self) -> float:
        return self.changeDispensed