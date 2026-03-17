## coin class
## 3-16-2026

# this class handles what a coin is and how much of that coin can be in the vending machine
# there are a wide range of coins possible, so a single flexible class is made instead of making a class for each possible coin
# also used, in the moneyHandler class, to determine what kinds of coins can be put into the machine
class coin:
    # init function
    def __init__(self, worthIn: float, maxAmtIn: int, curAmtIn: int) -> None:
        # coins are anywhere from .01 to 1.00 in worth, so worth is a float
        self.coinWorth: float = worthIn
        # tracks the max amount of this coin the machine can hold at once
        self.maxAmount: int = maxAmtIn
        # tracks the current amount of this coin the machine currently holds
        self.currentAmount: int = curAmtIn

    ## simple update methods [doesnt check for bounds!!]
    def updateCoinWorth(self, newWorth: float) -> None:
        self.coinWorth = newWorth

    def updateMaxAmount(self, newMax: int) -> None:
        self.maxAmount = newMax

    def updateCurrentAmount(self, newCurrent: int) -> None :
        self.currentAmount = newCurrent

    ## simple return methods
    def returnCoinWorth(self) -> float:
        return self.coinWorth

    def returnMaxAmount(self) -> int:
        return self.maxAmount

    def returnCurrentAmount(self) -> int:
        return self.currentAmount


