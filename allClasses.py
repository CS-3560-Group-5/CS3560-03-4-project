## all classes : init and manage all class instances
## 4-18-2026
## imports
import mysql.connector
from machine import machine
from product import product
from maintenanceRequest import maintenanceRequest
from restockRequest import restockRequest
from serviceWorker import serviceWorker
from cardSale import cardSale
from cashSale import cashSale
from machineSlot import machineSlot
from moneyHandler import moneyHandler
from coin import coin
from bill import bill
from perishableItem import perishableItem

## setting up db cursor
machDB = mysql.connector.connect(
    host="localhost",
    user="interface",
    password="password",
    database = "vendingmachine"
)
cursor = machDB.cursor()

# class to init all other classes
# also handles making new instances of classes / rows in the database
class allClasses:
    def __init__(self):
        ## setting up all classes
        self.machineList = []
        self.serviceWorkerList = []
        self.maintenanceRequestList = []
        self.productList = []
        self.cardSaleList = []
        self.cashSaleList = []
        self.machineSlotList = []
        self.restockRequestList = []
        self.moneyHandlerList = []
        self.perishableItemList = []
        self.billList = []
        self.coinList = []

        # setting up machines based on db info
        cursor.execute("SELECT * FROM machine")
        all = cursor.fetchall()     # fetch info
        for row in all:             # put every machine into memory with correct info
            self.machineList.append(machine(row[0], row[1], row[2], row[6], row[4], row[3], row[5]))

        # setting up serviceWorkers based on db info
        #  def __init__(self, idIn: str, nameIn: str, phoneIn: str, emailIn: str, companyIn: str
        cursor.execute("SELECT * FROM serviceworker")
        all = cursor.fetchall()
        for row in all:
            self.serviceWorkerList.append(serviceWorker(row[0], self.machineList[row[1] - 1], row[2], row[3], row[4], row[5], row[6]))

        # setting up maintenanceRequests based on db info
        cursor.execute("SELECT * FROM maintenancerequest")
        all = cursor.fetchall()
        for row in all:
            self.maintenanceRequestList.append(maintenanceRequest(row[0], self.machineList[row[1] - 1], self.serviceWorkerList[row[2] - 1], row[3], row[4], row[5]))

        # setting up product based on db info
        cursor.execute("SELECT * FROM product")
        all = cursor.fetchall()
        for row in all:
            self.productList.append(product(row[0], self.machineList[row[1] - 1], row[2], row[3], row[4], row[5], row[6]))

        # setting up transaction (cardsale and cashsale) based on db info
        cursor.execute("SELECT * FROM `transaction`")
        all = cursor.fetchall()
        for row in all:
            if row[5] != None:      # if cashGiven is none/null, then its a cardsale not a cash sale
                self.cardSaleList.append(cardSale(row[0], self.productList[row[1] - 1], row[2], row[3], row[4], row[5], row[6]))
            else:
                self.cashSaleList.append(cashSale(row[0], self.productList[row[1] - 1], row[2], row[3], row[4], row[7]))

        # setting up moneyHandlers
        cursor.execute("SELECT * FROM moneyhandler")
        all = cursor.fetchall()
        for row in all:
            self.moneyHandlerList.append(moneyHandler(row[0], self.machineList[row[1] - 1], row[2], row[3], row[4], row[5]))


        # setting up restockrequests
        cursor.execute("SELECT * FROM `restockrequest`")
        all = cursor.fetchall()
        for row in all:
            if row[2] != None:      # if the request has no moneyhandler, we don't pass in a money handler from the list
                self.restockRequestList.append(restockRequest(row[0], self.serviceWorkerList[row[1] - 1], self.moneyHandlerList[row[2] - 1], row[3], row[4], row[5]))
            else:
                self.restockRequestList.append(restockRequest(row[0], self.serviceWorkerList[row[1] - 1], None, row[3], row[4], row[5]))

        # setting up machineSlot
        cursor.execute("SELECT * FROM MachineSlot")
        all = cursor.fetchall()
        for row in all:
            if row[1] != None and row[2] != None:
                self.machineSlotList.append(machineSlot(row[0], self.productList[row[1] - 1], self.restockRequestList[row[2] - 1], row[3], row[4], row[5]))
            elif row[1] != None and row[2] == None:
                self.machineSlotList.append(machineSlot(row[0], self.productList[row[1] - 1], None, row[3], row[4], row[5]))
            else:
                self.machineSlotList.append(machineSlot(row[0], None, None, row[3], row[4], row[5]))
        
        # setting up perishableItem
        cursor.execute("SELECT * FROM perishableitem")
        all = cursor.fetchall()
        for row in all:
            # look for the correct index of the machineSlot object. Needed because this key is a string and not an int like the others
            index = 0
            for slot in self.machineSlotList:
                if row[1] == slot.returnNumpadCode():
                    break
                index += 1

            if row[2] != None:
                self.perishableItemList.append(perishableItem(row[0], self.machineSlotList[index], self.restockRequestList[row[2] - 1], row[3], row[4], row[5]))
            else:
                self.perishableItemList.append(perishableItem(row[0], self.machineSlotList[index], None, row[3], row[4], row[5]))

        # setting up currency (coins and bills)
        cursor.execute("SELECT * FROM currency")
        all = cursor.fetchall()
        for row in all:
            if row[3] != None:
                self.coinList.append(coin(row[0], row[1], row[2], row[3], row[4]))
            else:
                self.billList.append(bill(row[0], row[1], row[2], row[4]))

    ### Use case functions. Needed for logic of vending machine / use cases

    ### add functions. use these to add new objects to lists and database
    def addBill(self, moneyHandlerIn: moneyHandler, currAmtIn: int, worthIn: float) -> None:
        cursor.execute("INSERT INTO currency (moneyHandlerID, currentamount, maxamount, currencyworth) values (" + str(moneyHandlerIn.returnMoneyHandlerID()) + "," + str(currAmtIn) + ",NULL," + str(worthIn) + ")")    # add to db
        machDB.commit()
        cursor.execute("SELECT currencyID FROM currency")    # grab auto-gen ID from db
        id = cursor.fetchall()[-1]                           # Id is newest in returned list of IDs
        self.billList.append(bill(id, moneyHandlerIn, currAmtIn, worthIn))

    def addCoin(self, moneyHandlerIn: moneyHandler, currAmtIn: int, maxAmtIn: int, worthIn: float):
        cursor.execute("INSERT INTO currency (moneyHandlerID, currentamount, maxamount, currencyworth) values (" + str(moneyHandlerIn.returnMoneyHandlerID()) + "," + str(currAmtIn) + "," + str(maxAmtIn) +"," + str(worthIn) + ")")    # add to db
        machDB.commit()
        cursor.execute("SELECT currencyID FROM currency")    # grab auto-gen ID from db
        id = cursor.fetchall()[-1]                           # Id is newest in returned list of IDs
        self.coinList.append(coin(id, moneyHandlerIn, currAmtIn, maxAmtIn, worthIn))

    # if restock request is NULL/NONE, pass in a NONE for the request
    # automatically determines what the slot position should be
    def addPerishableItem(self, machineSlotIn: machineSlot, requestIn: restockRequest, dateExpire: str, restockDaysIn: int) -> None: 
        # determine slot pos from data in table
        cursor.execute("SELECT slotposition FROM perishableItem WHERE machineslotID = \"" + machineSlotIn.returnNumpadCode() + "\"")
        slots = cursor.fetchall()
        biggest = 0
        for slot in slots:      # for loop because slotPositions may not be in order (though they should be)
            if int(''.join(map(str, slot))) >= biggest:
                biggest = int(''.join(map(str, slot)))
        slotPos = biggest + 1
        # based on requestIn being none, execute sql
        if requestIn == None:
            cursor.execute("INSERT INTO perishableitem (MachineslotID, restockrequestID, dateexpire, restockdaysbeforeexpire, slotposition) values (\"" + str(machineSlotIn.returnNumpadCode()) + "\",NULL," + "STR_TO_DATE(\"" + dateExpire + "\",\"%m,%d,%Y\")" + "," + str(restockDaysIn) + "," + str(slotPos) + ")")    # add to db
        else:
            cursor.execute("INSERT INTO perishableitem (MachineslotID, restockrequestID, dateexpire, restockdaysbeforeexpire, slotposition) values (\"" + str(machineSlotIn.returnNumpadCode()) + "\"," + str(requestIn.returnRestockRequestID()) + "," + "STR_TO_DATE(\"" + dateExpire + "\",\"%m,%d,%Y\")" + "," + str(restockDaysIn) + "," + str(slotPos) + ")") 
        machDB.commit()
        cursor.execute("SELECT perishableItemID FROM perishableItem")    # grab auto-gen ID from db
        # append new val to list
        id = cursor.fetchall()[-1]                           # Id is newest in returned list of IDs
        self.perishableItemList.append(perishableItem(id, machineSlotIn, requestIn, dateExpire, restockDaysIn, slotPos))

    def addMoneyHandler(self, machineIn: machine, billMaxThreshIn: float, billMaxIn: int, coinMaxThreshIn: float, coinMinThreshIn: float) -> None:
        cursor.execute("INSERT INTO moneyHandler (machineID, billRestockMaxThreshold, billmaxamount, coinrestockmaxthreshold, coinrestockminthreshold) values (" + str(machineIn.returnMachineID()) + "," + str(billMaxThreshIn) + "," + str(billMaxIn) +"," + str(coinMaxThreshIn) + "," + str(coinMinThreshIn) + ")")    # add to db
        machDB.commit()
        cursor.execute("SELECT moneyHandlerID FROM moneyHandler")    # grab auto-gen ID from db
        id = cursor.fetchall()[-1]                           # Id is newest in returned list of IDs
        self.moneyHandlerList.append(moneyHandler(id, machineIn, billMaxThreshIn, billMaxIn, coinMaxThreshIn, coinMinThreshIn))

    # if no moneyhandler or dateresolved, pass in None for them
    def addRestockRequest(self, restockerIn: serviceWorker, moneyHandlerIn: moneyHandler, dateRequestedIn : str, dateResolvedIn : str, reasonIn: str) -> None:
        # running correct sql based on nones
        if moneyHandlerIn != None and dateResolvedIn != None:
            cursor.execute("INSERT INTO restockRequest (serviceworkerid, moneyhandlerid, daterequested, dateresolved, reasonforrequest) values (" + str(restockerIn.returnEmployeeID()) + "," + str(moneyHandlerIn.returnMoneyHandlerID()) + "," + "STR_TO_DATE(\"" + dateRequestedIn + "\",\"%m,%d,%Y\")" +"," + "STR_TO_DATE(\"" + dateResolvedIn + "\",\"%m,%d,%Y\")" + ",\"" + str(reasonIn) + "\")")    # add to db
        elif moneyHandlerIn != None and dateResolvedIn == None:
            cursor.execute("INSERT INTO restockRequest (serviceworkerid, moneyhandlerid, daterequested, dateresolved, reasonforrequest) values (" + str(restockerIn.returnEmployeeID()) + "," + str(moneyHandlerIn.returnMoneyHandlerID()) + "," + "STR_TO_DATE(\"" + dateRequestedIn + "\",\"%m,%d,%Y\")" +",NULL,\"" + str(reasonIn) + "\")")
        elif moneyHandlerIn == None and dateResolvedIn == None:
            cursor.execute("INSERT INTO restockRequest (serviceworkerid, moneyhandlerid, daterequested, dateresolved, reasonforrequest) values (" + str(restockerIn.returnEmployeeID()) + ",NULL," + "STR_TO_DATE(\"" + dateRequestedIn + "\",\"%m,%d,%Y\")" +",NULL,\"" + str(reasonIn) + "\")")
        else:
            cursor.execute("INSERT INTO restockRequest (serviceworkerid, moneyhandlerid, daterequested, dateresolved, reasonforrequest) values (" + str(restockerIn.returnEmployeeID()) + ",NULL," + "STR_TO_DATE(\"" + dateRequestedIn + "\",\"%m,%d,%Y\")" +"," + "STR_TO_DATE(\"" + dateResolvedIn + "\",\"%m,%d,%Y\")" + ",\"" + str(reasonIn) + "\")")
        machDB.commit()
        cursor.execute("SELECT restockRequestID FROM restockRequest")    # grab auto-gen ID from db
        id = cursor.fetchall()[-1]                                   # Id is newest in returned list of IDs
        self.restockRequestList.append(restockRequest(id, restockerIn, moneyHandlerIn, dateRequestedIn, dateResolvedIn, reasonIn))
    
    # if no dateresolved, pass in None for them
    def addMaintenanceRequest(self, machineIn: machine, techIn: serviceWorker, dateRequestedIn : str, dateResolvedIn : str, reasonIn: str) -> None:
        # running sql based in nones
        if dateResolvedIn != None:
            cursor.execute("INSERT INTO maintenancerequest (machineID, serviceWorkerID, daterequested, dateresolved, reasonforrequest) values (" + str(machineIn.returnMachineID()) + "," + str(techIn.returnEmployeeID()) + "," + "STR_TO_DATE(\"" + dateRequestedIn + "\",\"%m,%d,%Y\")" +"," + "STR_TO_DATE(\"" + dateResolvedIn + "\",\"%m,%d,%Y\")" + ",\"" + str(reasonIn) + "\")")    # add to db
        else:
            cursor.execute("INSERT INTO maintenancerequest (machineID, serviceWorkerID, daterequested, dateresolved, reasonforrequest) values (" + str(machineIn.returnMachineID()) + "," + str(techIn.returnEmployeeID()) + "," + "STR_TO_DATE(\"" + dateRequestedIn + "\",\"%m,%d,%Y\")" +",NULL,\"" + str(reasonIn) + "\")")
        machDB.commit()
        cursor.execute("SELECT maintenancerequestID FROM maintenancerequest")    # grab auto-gen ID from db
        id = cursor.fetchall()[-1]                                               # Id is newest in returned list of IDs
        self.maintenanceRequestList.append(maintenanceRequest(id, machineIn, techIn, dateRequestedIn, dateResolvedIn, reasonIn))

    # if no productID, restockRequest, productcount, maxamount, or thresh, pass in None
    def addMachineSlot(self, slotCodeIn: str, productIn: product, requestIn: restockRequest, productCountIn: int, maxAmountIn: int, restockAtThresholdIn: float) -> None:
        # returns early if the slotcode already exists
        for slot in self.machineSlotList:
            if slotCodeIn == slot.returnNumpadCode():
                return
        if productIn != None and requestIn != None:
            cursor.execute("INSERT INTO machineslot values (\"" + str(slotCodeIn) + "\"," + str(productIn.returnProductID()) + "," + str(requestIn.returnRestockRequestID()) + "," + str(productCountIn) + "," + str(maxAmountIn) + "," + str(restockAtThresholdIn) + ")")    # add to db
        elif productIn != None and requestIn == None:
            cursor.execute("INSERT INTO machineslot values (\"" + str(slotCodeIn) + "\"," + str(productIn.returnProductID()) + ",NULL," + str(productCountIn) + "," + str(maxAmountIn) + "," + str(restockAtThresholdIn) + ")")
        else:
            cursor.execute("INSERT INTO machineslot values (\"" + str(slotCodeIn) + "\",NULL,NULL,NULL,NULL,NULL)")  
        machDB.commit()
        self.machineSlotList.append(machineSlot(slotCodeIn, productIn, requestIn, productCountIn, maxAmountIn, restockAtThresholdIn))


    def addCashSale(self) -> None:
        pass # TODO

    def addCardSale(self) -> None:
        pass # TODO

    def addProduct(self) -> None:
        pass # TODO

    def addServiceWorker(self) -> None:
        pass # TODO

    def addMachine(self) -> None:
        pass # TODO

    ### delete functions. used to delete entries from database table and lists
    ### pass in the ID of the row to delete it
    def deleteBill(self) -> None:
        pass # TODO

    def deleteCoin(self) -> None:
        pass # TODO

    def deletePerishableItem(self) -> None:
        pass # TODO

    def deleteMoneyHandler(self) -> None:
        pass # TODO

    def deleteRestockRequest(self) -> None:
        pass # TODO

    def deleteMachineSlot(self) -> None:
        pass # TODO

    def deleteCashSale(self) -> None:
        pass # TODO

    def deleteCardSale(self) -> None:
        pass # TODO

    def deleteProduct(self) -> None:
        pass # TODO

    def deleteMaintenanceRequest(self) -> None:
        pass # TODO

    def deleteServiceWorker(self) -> None:
        pass # TODO

    def deleteMachine(self) -> None:
        pass # TODO


    # list returns
    def returnBillList(self):
        return self.billList
    
    def returnCoinList(self):
        return self.coinList
    
    def returnPerishableItemList(self):
        return self.perishableItemList
    
    def returnMoneyHandlerList(self):
        return self.moneyHandlerList
    
    def returnRestockRequestList(self):
        return self.restockRequestList
    
    def returnMachineSlotList(self):
        return self.machineSlotList
    
    def returnCashSaleList(self):
        return self.cardSaleList
    
    def returnCardSaleList(self):
        return self.cardSaleList
    
    def returnProductList(self):
        return self.productList
    
    def returnMaintenanceRequestList(self):
        return self.maintenanceRequestList
    
    def returnServiceWorkerList(self):
        return self.serviceWorkerList
    
    def returnMachineList(self):
        return self.machineList
