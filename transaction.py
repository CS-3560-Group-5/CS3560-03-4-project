# transaction class
# 3/15/2026

# type hint imports
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from product import product
    from machine import machine

# actual imports
from abc import ABC, abstractmethod     # for abstract class implementation
import datetime

# this is an abstract class used in the implementation of the cardSale and cashSale classes
class transaction(ABC):
    @abstractmethod
    # Notes :
    # - a transaction object doesn't keep track of the price of the product bought because the product bought is linked to this class and has the price there
    # - a transaction object can only have one product at a time. this is because customers buy things from a vending machine one at a time.

    # default constructor
    # *Doesnt make a new entry in assigned db table, only inits a class with this data. ID is assumed to correlate to a value inside the db table*
    def __init__(self, saleNumberIn: int, itemIn: product, machineIn: machine, taxIn: float, saleDateTimeIn: datetime) -> None:
        # used to track of what number sale this transaction is and to give each transaction a unique ID
        self.saleNumber: int = saleNumberIn
        # used to track of how much the product was taxed
        self.tax: float = taxIn
        # tracks assigned machine
        self.assignedMachine: machine = machineIn
        # used to track of when the product was bought
        self.saleDateTime: datetime = saleDateTimeIn
        # used to track of what product was bought
        self.item: product = itemIn

    ## use case methods 

    ## simple update methods
    def updateProduct(self, itemBought: product) -> None:
        self.item = product

    def updateTax(self, newTax: float) -> None:
        self.tax = newTax

    def updateSaleNumber(self, newSaleNum: int) -> None:
        self.saleNumber = newSaleNum

    def updateSaleDateTime(self, newSaleDate: datetime) -> None:
        self.saleDateTime = newSaleDate
        
    ## simple return methods
    def returnProduct(self) -> product:
        return self.item

    def returnTax(self) -> float:
        return self.tax

    def returnSaleNumber(self) -> int:
        return self.saleNumber

    def returnSaleDateTime(self) -> datetime:
        return self.saleDateTime
    
