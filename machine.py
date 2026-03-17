## machine class
## 3-15-2026

# Note : This project is using pythons type hint functionality. this is purely for commenting purposes and DOES NOT DO ANYTHING except for adding notation. This will not enforce types or error check for you.
# type hint imports
from __future__ import annotations
from typing import TYPE_CHECKING
from typing import List

if TYPE_CHECKING:      # This if statement is needed at the top of each file to avoid circular imports made by type hinting. Put all imported classes for type hinting within this if statement
    from technician import technician
    from restocker import restocker
    from transaction import transaction
    from product import product
    from maintenanceRequest import maintenanceRequest
    from coin import coin
    from bill import bill

# actual imports
import datetime

# handles the tracking of when maintenance requests are sent, via the service date aproaching or the machine having a malfunction
# also connects classes
class machine:
    # basic contructor. takes in basic info about machine. also sets up all links to other classes
    def __init__(self, addressIn: str, modelNumIn: str, maxSlotsIn: int, lastServicedIn: datetime, currStateIn: str, daysBetweenSerIn: int, techIn: List[technician], restockersIn: List[restocker], requestsIn: List[maintenanceRequest], transactionsIn: List[transaction], productsIn: List[product]) -> None:
        ## basic attributes
        # stores the full address of the machine
        self.address: str = addressIn
        # stores the model number of the machine
        self.modelNumber: str = modelNumIn
        # stores the maximum amount of slots the machine has to fit products in
        self.maxProductSlots: int = maxSlotsIn
        # stores the current operational state of the machine
        self.currentState: str = currStateIn
        # stores the date that the machine was last serviced
        self.dateLastServiced: datetime = lastServicedIn
        # stores the days between each machine service
        self.daysbetweenServices: int = daysBetweenSerIn

        ## other class instances
        # the list of technicians assigned to this machine
        self.technicians: List[technician] = techIn
        # the list of restockers assigned to this machine
        self.restockers: List[restocker] = restockersIn
        # the list of made maintenance requests for this machine
        self.requests: List[maintenanceRequest] = requestsIn
        # the list of made transactions at this machine
        self.transactions: List[transaction] = transactionsIn
        # the list of products in this machine
        self.products: List[product] = productsIn

    ## Use case functions
    # function called when a machine malfunction is detected. this creates a new maintenanceRequest for one of the machines assigned technicians
    def malfunctionDetected(self, techAssigned: technician) -> None:
        # TODO : implement
        return NotImplemented
    
    # function called to check scheduled service date. if service date has been reached, a new maintenanceRequest is made for a technician
    # this should be ran at the beginning of each day
    def checkServiceDate(self, techAssigned: technician) -> None:
        # TODO : implement
        return NotImplemented
    
    # function called to record a transaction 
    def recordTransaction(self, productPurchased: product, saleType: str) -> None:
        # TODO : implement. also fix saleType input type
        return NotImplemented
    
    # function called to update machine inventory
    def updateInventory(self, productDecremented: product) -> None:
        # TODO : implement
        return NotImplemented
    
    # function called to update the amount of cash in the machine
    # a list of the bills and coins are given. these are referenced against the moneyHandlers bills and coins. If they match, their values are added together. If not, error thrown
    # can be positive or negative coin/bill amounts. Error will be thrown if the amount of bills/coins the machine can hold is exceeded.
    def updateCash(self, coinUpdate: List[coin], billUpdate: List[bill]) -> None:
        # TODO : implement
        return NotImplemented
    
    # "Admin updates machine information" case is handled with the simple update methods below

    ## List methods for technicians
    # append value
    def appendTechnician(self, newTech: technician) -> None:
        self.technicians.append(newTech)

    # replace value at index
    def replaceTechnician(self, newTech: technician, index: int) -> None:
        self.technicians[index] = technician

    # return specific value of index
    def returnTechnician(self, index: int) -> technician:
        return self.technicians[index]
    
    # return whole list
    def returnTechnicians(self) -> List[technician]:
        return self.technicians

    ## List methods for restockers
    # append value
    def appendRestocker(self, newRestocker: restocker) -> None:
        self.restockers.append(newRestocker)

    # replace value at index
    def replaceRestocker(self, newRestocker: restocker, index: int) -> None:
        self.restockers[index] = newRestocker

    # return specific value of index
    def returnRestocker(self, index: int) -> restocker:
        return self.restockers[index]

    # return whole list
    def returnRestockers(self) -> List[restocker]:
        return self.restockers

    ## List methods for requests
    # append value 
    def appendRequest(self, newRequest: maintenanceRequest) -> None:
        self.requests.append(newRequest)

    # replace value at index
    def replaceRequest(self, newRequest: maintenanceRequest, index: int) -> None:
        self.requests[index] = newRequest

    # return value at index
    def returnRequest(self, index: int) -> maintenanceRequest:
        return self.requests[index]

    # return entire list
    def returnRequests(self) -> List[maintenanceRequest]:
        return self.requests

    ## List methods for transactions
    # append value
    def appendTransaction(self, newTransaction: transaction) -> None:
        self.transactions.append(newTransaction)

    # replace value at index
    def replaceTransaction(self, newTransaction: transaction, index: int) -> None:
        self.transactions[index] = newTransaction

    # return specific value of index
    def returnTransaction(self, index: int) -> transaction:
        return self.transactions[index]

    # return whole list
    def returnTransactions(self, index: int) -> List[transaction]:
        return self.transactions

    ## List methods for products
    # append value
    def appendProduct(self, newProduct: product) -> None:
        self.products.append(newProduct)

    # replace value at index
    def replaceProduct(self, newProduct: product, index: int) -> None:
        self.products[index] = newProduct

    # return specific value of index
    def returnProduct(self, index: int) -> product:
        return self.products[index]

    # return whole list
    def returnProducts(self) -> List[product]:
        return self.products

    ## simple update methods
    def updateAddress(self, newAddress: str) -> None:
        self.address = newAddress
    
    def updateModelNumber(self, newModelNum: str) -> None:
        self.modelNumber = newModelNum

    def updateMaxProductSlots(self, newMaxSlots: int) -> None:
        self.maxProductSlots = newMaxSlots

    def updateCurrentState(self, newState: str) -> None:
        self.currentState = newState
    
    def updateDateLastServiced(self, newLastServiced: datetime) -> None:
        self.dateLastServiced = newLastServiced

    def updateDaysBetweenServices(self, newDaysBetween: int) -> None:
        self.daysbetweenServices = newDaysBetween

    ## simple return methods
    def returnAddress(self) -> str:
        return self.address
    
    def returnModelNumber(self) -> str:
        return self.modelNumber

    def returnMaxProductSlots(self) -> int:
        return self.maxProductSlots
    

    def returnCurrentState(self) -> str:
        return self.currentState
    
    def returnDateLastServiced(self) -> datetime:
        return self.dateLastServiced
    
    def returnDaysBetweenServices(self) -> int:
        return self.daysbetweenServices