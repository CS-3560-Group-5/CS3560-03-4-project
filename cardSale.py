## cardSale class
## 3/15/2026

# type hint imports
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from transaction import transaction
    from product import product

# actual imports

# class to implement card transaction recording. inherits transaction class
class cardSale(transaction):
    # init function
    def __init__(self, itemIn: product, feeIn: float, accountIn: str) -> None:
        # used to keep track of the fee charged to the customers card (if any)
        self.cardFee: float = feeIn
        # used to record what account was charged for the transaction
        self.accountCharged: str = accountIn
        # call inherited init
        super().__init__(itemIn)

    ## simple update methods
    def updateCardFee(self, newFee: float) -> None:
        self.cardFee = newFee

    def updateAccountCharged(self, newAccount: str) -> None:
        self.accountCharged = newAccount

    ## simple return methods
    def returnCardFee(self) -> float:
        return self.cardFee

    def returnAccountCharged(self) -> str:
        return self.accountCharged