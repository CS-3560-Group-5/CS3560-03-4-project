## bill class
## 4-6-2026
from __future__ import annotations
from currency import currency
from typing import TYPE_CHECKING

if TYPE_CHECKING: 
    from moneyHandler import moneyHandler

# bill class
class bill(currency):
    def __init__(self, selfID: int, moneyHandlerIn: moneyHandler,  currAmtIn: int, worthIn: float) -> None:
        super().__init__(selfID, moneyHandlerIn, currAmtIn, worthIn)
