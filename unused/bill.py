## bill class
## 4-6-2026
from __future__ import annotations
from unused.currency import currency
from typing import TYPE_CHECKING

if TYPE_CHECKING: 
    from unused.moneyHandler import moneyHandler

# bill class
# *Doesnt make a new entry in assigned table, only inits a class with this data. ID is assumed to correlate to a value inside the db table*
class bill(currency):
    def __init__(self, selfID: int, moneyHandlerIn: moneyHandler,  currAmtIn: int, worthIn: float) -> None:
        super().__init__(selfID, moneyHandlerIn, currAmtIn, worthIn)
