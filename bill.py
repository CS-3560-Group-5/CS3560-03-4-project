## bill class
## 3-16-2026


# this class handles what a paper bill is and how much of it is in the machine
# also used, in the moneyHandler class, to determine what bills can be fed into the machine
class bill:
    # init function
    def __init__(self, worthIn: float, currAmtIn: int) -> None:
        # bills are typically whole numbers, but worth should be a float so that later money operations can be handled correctly
        self.billWorth: float = worthIn
        # tracks how much of this bill is currently in the machine
        self.currentAmount: int = currAmtIn
        # the max amount of bills is held within the moneyHandler class. this is because each bill is the same size and doesnt go to a different holding chamber. putting max amount in this class would cause extra operations to determine how many bills can be in the machine at once

    ## simple update methods [doesnt check for bounds!!]
    def updateBillWorth(self, newWorth: float) -> None:
        self.billWorth = newWorth

    def updateCurrentAmount(self, newAmt: int) -> None:
        self.currentAmount = newAmt

    ## simple return methods
    def returnBillWorth(self) -> float:
        return self.billWorth

    def returnCurrentAmount(self) -> int:
        return self.currentAmount

