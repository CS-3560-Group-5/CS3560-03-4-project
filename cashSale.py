# cashSale class
# 3/15/2026

# type hint imports
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from transaction import transaction
    from product import product

# actual imports


# class to implement cash transaction recording. inherits transaction class
class cashSale(transaction):

    def __init__(self, itemIn: product, cashGivenIn: float, changeDisIn: float) -> None:
        # used to keep track of the money the customer gave to the machine
        self.cashGiven: float = cashGivenIn
        # used to record how much change was given back to the customer
        self.changeDispensed: float = changeDisIn
        # call inherited init
        super().__init__(itemIn)

    ## simple update methods
    def updateCashGiven(self, newGiven: float) -> None:
        self.cashGiven = newGiven

    def updateChangeDispensed(self, newChange: float) -> None:
        self.changeDispensed = newChange

    ## simple return methods
    def returnCashGiven(self) -> float:
        return self.cashGiven
    
    def returnChangeDispensed(self) -> float:
        return self.changeDispensed