## currency superclass
## Refactored to consolidate shared logic from coin and bill
from abc import ABC

class currency(ABC):
    def __init__(self, worthIn: float, currAmtIn: int) -> None:
        self.worth: float = worthIn
        self.currentAmount: int = currAmtIn

    def updateWorth(self, newWorth: float) -> None:
        self.worth = newWorth

    def updateCurrentAmount(self, newAmt: int) -> None:
        self.currentAmount = newAmt

    def returnWorth(self) -> float:
        return self.worth

    def returnCurrentAmount(self) -> int:
        return self.currentAmount
