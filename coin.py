## coin class
## 4-6-2026
from currency import currency
import mysql.connector

# setting up DB cursor
machDB = mysql.connector.connect(
    host="localhost",
    user="interface",
    password="password",
    database = "vendingmachine"
)
cursor = machDB.cursor()

# coin class
class coin(currency):
    def __init__(self, worthIn: float, maxAmtIn: int, curAmtIn: int) -> None:
        super().__init__(worthIn, curAmtIn)
        self.maxAmount: int = maxAmtIn

    def updateMaxAmount(self, newMax: int) -> None:
        self.maxAmount = newMax

    def returnMaxAmount(self) -> int:
        return self.maxAmount
