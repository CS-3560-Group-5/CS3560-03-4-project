## coin class
## 4-6-2026
from __future__ import annotations
from currency import currency
from typing import TYPE_CHECKING

if TYPE_CHECKING: 
    from moneyHandler import moneyHandler

# coin class
class coin(currency):
    def __init__(self, selfID: int, moneyHandlerIn: moneyHandler,  currAmtIn: int, maxAmtIn: int, worthIn: float) -> None:
        super().__init__(selfID, moneyHandlerIn, currAmtIn, worthIn)
        self.maxAmount: int = maxAmtIn

    # update and return functions
    def updateMaxAmount(self, newMax: int) -> None:
        self.maxAmount = newMax

    def returnMaxAmount(self) -> int:
        return self.maxAmount
