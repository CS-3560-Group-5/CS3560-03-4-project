## bill class
## 4-6-2026
from currency import currency

class bill(currency):
    def __init__(self, worthIn: float, currAmtIn: int) -> None:
        super().__init__(worthIn, currAmtIn)
