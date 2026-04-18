## currency superclass
## Refactored to consolidate shared logic from coin and bill
# imports
from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING: 
    from moneyHandler import moneyHandler

# currency class
class currency(ABC):
    # constructor
    def __init__(self, selfID: int, moneyHandlerIn: moneyHandler,  currAmtIn: int, worthIn: float) -> None:
        self.currencyID: int = selfID
        self.moneyHandlerAssigned: moneyHandler = moneyHandlerIn
        self.worth: float = worthIn
        self.currentAmount: int = currAmtIn

    # update and return functions
    def updateWorth(self, newWorth: float) -> None:
        self.worth = newWorth

    def updateCurrentAmount(self, newAmt: int) -> None:
        self.currentAmount = newAmt

    def returnWorth(self) -> float:
        return self.worth

    def returnCurrentAmount(self) -> int:
        return self.currentAmount
