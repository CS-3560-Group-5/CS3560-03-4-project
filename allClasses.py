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

### Important DB Note
# allClasses expects all tables to have at least 1 row of info each when initalized 
# also expects the initial data to have IDs in numberical order
# run VendMachEntireDB.sql on db before running python
# TODO : Fix these quirks

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
                self.coinList.append(coin(row[0], self.moneyHandlerList[row[1] - 1], row[2], row[3], row[4]))
            else:
                self.billList.append(bill(row[0], self.moneyHandlerList[row[1] - 1], row[2], row[4]))

    ### Use case functions. Needed for logic of vending machine / use cases

    ### add functions. use these to add new objects to lists and database
    ### none of these take user defined IDS except for addMachineSlot
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
            cursor.execute("INSERT INTO maintenancerequest (machineID, serviceWorkerID, daterequested, dateresolved, reasonforrequest) values (" + str(machineIn.returnMachineID()) + "," + str(techIn.returnEmployeeID()) + "," + "STR_TO_DATE(\"" + dateRequestedIn + "\",\"%m,%d,%Y\")" + "," + "STR_TO_DATE(\"" + dateResolvedIn + "\",\"%m,%d,%Y\")" + ",\"" + str(reasonIn) + "\")")    # add to db
        else:
            cursor.execute("INSERT INTO maintenancerequest (machineID, serviceWorkerID, daterequested, dateresolved, reasonforrequest) values (" + str(machineIn.returnMachineID()) + "," + str(techIn.returnEmployeeID()) + "," + "STR_TO_DATE(\"" + dateRequestedIn + "\",\"%m,%d,%Y\")" + ",NULL,\"" + str(reasonIn) + "\")")
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

    # expects date to be passed as numbers in the string form "month,day,year,hour,minute,second" like "1,1,2000,5,10,1"
    def addCashSale(self, itemIn: product, machineIn: machine, taxIn: float, saleDateTimeIn: str, cashGivenIn: float) -> None:
        cursor.execute("INSERT INTO transaction (ProductID, MachineID, Tax, SaleDateTime, CashGiven) values (" + str(itemIn.returnProductID()) + "," + str(machineIn.returnMachineID()) + "," + str(round(taxIn, 2)) + "," + "STR_TO_DATE(\"" + saleDateTimeIn + "\",\"%m,%d,%Y,%h,%i,%s\")" + "," + str(round(cashGivenIn, 2)) + ")")    # add to db
        machDB.commit()
        cursor.execute("SELECT saleNumber FROM transaction")    # grab auto-gen ID from db
        id = cursor.fetchall()[-1]                              # Id is newest in returned list of IDs
        self.cashSaleList.append(cashSale(id, itemIn, machineIn, taxIn, saleDateTimeIn, cashGivenIn))

    def addCardSale(self, itemIn: product, machineIn: machine, taxIn: float, saleDateTimeIn: str, feeIn: float, accountIn: str) -> None:
        cursor.execute("INSERT INTO transaction (ProductID, MachineID, Tax, SaleDateTime, CardFee, AccountCharged) values (" + str(itemIn.returnProductID()) + "," + str(machineIn.returnMachineID()) + "," + str(round(taxIn, 2)) + "," + "STR_TO_DATE(\"" + saleDateTimeIn + "\",\"%m,%d,%Y,%h,%i,%s\")" + "," + str(round(feeIn, 2)) + ",\"" + str(accountIn) + "\")")    # add to db
        machDB.commit()
        cursor.execute("SELECT saleNumber FROM transaction")    # grab auto-gen ID from db
        id = cursor.fetchall()[-1]                              # Id is newest in returned list of IDs
        self.cardSaleList.append(cardSale(id, itemIn, machineIn, taxIn, saleDateTimeIn, feeIn, accountIn))

    def addProduct(self, assignedMachineIn : machine, nameIn: str,  descIn: str, nutritIn: str, ingredIn: str, priceIn: float) -> None:
        cursor.execute("INSERT INTO product (MachineID, Name, Description, NutritionFacts, Ingredients, Price) values (" + str(assignedMachineIn.returnMachineID()) + ",\"" + str(nameIn) + "\",\"" + str(descIn) + "\",\"" + str(nutritIn) + "\",\"" + str(ingredIn) + "\"," + str(round(priceIn, 2)) + ")")    # add to db
        machDB.commit()
        cursor.execute("SELECT productID FROM product")       # grab auto-gen ID from db
        id = cursor.fetchall()[-1]                              # Id is newest in returned list of IDs
        self.productList.append(product(id, assignedMachineIn, nameIn, descIn, nutritIn, ingredIn, priceIn))

    def addServiceWorker(self, assignedMachineIn: machine, nameIn: str, workerTypeIn: str, phoneIn: str, emailIn: str, companyIn: str) -> None:
        cursor.execute("INSERT INTO serviceWorker (MachineID, Name, WorkerType, PhoneNumber, Email, Company) values (" + str(assignedMachineIn.returnMachineID()) + ",\"" + str(nameIn) + "\",\"" + str(workerTypeIn) + "\",\"" + str(phoneIn) + "\",\"" + str(emailIn) + "\",\""  + str(companyIn) + "\")")    # add to db
        machDB.commit()
        cursor.execute("SELECT workerID FROM serviceWorker")       # grab auto-gen ID from db
        id = cursor.fetchall()[-1]                              # Id is newest in returned list of IDs
        self.serviceWorkerList.append(serviceWorker(id, assignedMachineIn, nameIn, workerTypeIn, phoneIn, emailIn, companyIn))

    def addMachine(self, addressIn: str, modelNumIn: str, maxSlotsIn: int, lastServicedIn: str, currStateIn: str, daysBetweenSerIn: int) -> None:
        cursor.execute("INSERT INTO machine (address, modelNumber, currentState, dateLastServiced, daysBetweenServices, MaxProductSlots) values (\"" + str(addressIn) + "\",\"" + str(modelNumIn) + "\",\"" + str(currStateIn) + "\"," + "STR_TO_DATE(\"" + lastServicedIn + "\",\"%m,%d,%Y\")" + "," + str(daysBetweenSerIn) + "," + str(maxSlotsIn) + ")")    # add to db
        machDB.commit()
        cursor.execute("SELECT machineID FROM machine")       # grab auto-gen ID from db
        id = cursor.fetchall()[-1]                            # Id is newest in returned list of IDs
        self.machineList.append(machine(id, addressIn, modelNumIn, maxSlotsIn, lastServicedIn, currStateIn, daysBetweenSerIn))

    ### delete functions. used to delete entries from database table and lists
    ### pass in the ID of the row to delete it
    def deleteBill(self, idIn: int) -> None:
        # make sure this is a bill being deleted
        for obj in self.billList:
            if obj.returnCurrencyID() == idIn:
                break
        else:
            return
        # remove row from db
        cursor.execute("DELETE FROM currency WHERE currencyID = " + str(idIn))
        machDB.commit()
        # remove from list
        for obj in self.billList:
            if obj.returnCurrencyID() == idIn:
                self.billList.remove(obj)
                break

    def deleteCoin(self, idIn: int) -> None:
        # make sure this is a coin being deleted
        for obj in self.coinList:
            if obj.returnCurrencyID() == idIn:
                break
        else:
            return
        # remove row from db
        cursor.execute("DELETE FROM currency WHERE currencyID = " + str(idIn))
        machDB.commit()
        # remove from list
        for obj in self.coinList:
            if obj.returnCurrencyID() == idIn:
                self.coinList.remove(obj)
                break

    def deletePerishableItem(self, idIn: int) -> None:
        # remove row from db
        cursor.execute("DELETE FROM perishableItem WHERE perishableitemid = " + str(idIn))
        machDB.commit()
        # remove from list
        for obj in self.perishableItemList:
            if obj.returnPerishableItemID() == idIn:
                self.perishableItemList.remove(obj)
                break

    # !!WARNING!!
    # to delete a moneyHandler all coins, bills, and restockRequests associated with this moneyhandler must be deleted as well.
    # function deletes all associated coins, bills, and restockRequests to do this
    def deleteMoneyHandler(self, idIn: int) -> None:
        # delete all associated currency and restockrequest
        cursor.execute("DELETE FROM currency WHERE moneyhandlerid = " + str(idIn))
        cursor.execute("DELETE FROM restockrequest WHERE moneyhandlerid = " + str(idIn))
        # remove row from db
        cursor.execute("DELETE FROM moneyhandler WHERE moneyhandlerid = " + str(idIn))
        machDB.commit()
        # remove from all lists
        temp = []
        for obj in self.moneyHandlerList:
            if obj.returnMoneyHandlerID() == idIn:
                temp.append(obj)
        for rem in temp:
            self.moneyHandlerList.remove(rem)

        temp = []
        for obj in self.coinList:
            if obj.returnMoneyHandlerAssigned().returnMoneyHandlerID() == idIn:
                temp.append(obj)
        for rem in temp:
            self.coinList.remove(rem)

        temp = []
        for obj in self.billList:
            if obj.returnMoneyHandlerAssigned().returnMoneyHandlerID() == idIn:
                temp.append(obj)
        for rem in temp:
            self.billList.remove(rem)

        temp = []
        for obj in self.restockRequestList:
            if obj.returnAssignedMoneyHandler() != None and obj.returnAssignedMoneyHandler().returnMoneyHandlerID() == idIn:
                temp.append(obj)
        for rem in temp:
            self.restockRequestList.remove(rem)

    def deleteRestockRequest(self, idIn: int) -> None:
        # remove row from db
        cursor.execute("DELETE FROM restockRequest WHERE restockrequestID = " + str(idIn))
        machDB.commit()
        # remove from list
        for obj in self.restockRequestList:
            if obj.returnRestockRequestID() == idIn:
                self.restockRequestList.remove(obj)
                break

    # !!WARNING!!
    # to delete a machineSlot all perishableItems associated with this machineSlot must be deleted as well.
    # function deletes all associated perishableItems to do this
    def deleteMachineSlot(self, idIn: str) -> None:
        # delete all associated perishableItems
        cursor.execute("DELETE FROM perishableItem WHERE machineSlotID = \"" + str(idIn) + "\"")
        # remove row from db
        cursor.execute("DELETE FROM machineSlot WHERE slotCode = \"" + str(idIn) + "\"")
        machDB.commit()
        # remove from all lists
        temp = []
        for obj in self.machineSlotList:
            if obj.returnNumpadCode() == idIn:
                temp.append(obj)
        for rem in temp:
            self.machineSlotList.remove(rem)

        temp = []
        for obj in self.perishableItemList:
            if obj.returnSlot().returnNumpadCode() == idIn:
                temp.append(obj)
        for rem in temp:
            self.perishableItemList.remove(rem)



    def deleteCashSale(self, idIn: int) -> None:
        # make sure this is a cashSale being deleted
        for obj in self.cashSaleList:
            if obj.returnSaleNumber() == idIn:
                break
        else:
            return
        # remove row from db
        cursor.execute("DELETE FROM `transaction` WHERE salenumber = " + str(idIn))
        machDB.commit()
        # remove from list
        for obj in self.cashSaleList:
            if obj.returnSaleNumber() == idIn:
                self.cashSaleList.remove(obj)
                break

    def deleteCardSale(self, idIn: int) -> None:
        # make sure this is a cardSale being deleted
        for obj in self.cardSaleList:
            if obj.returnSaleNumber() == idIn:
                break
        else:
            return
        # remove row from db
        cursor.execute("DELETE FROM `transaction` WHERE salenumber = " + str(idIn))
        machDB.commit()
        # remove from list
        for obj in self.cardSaleList:
            if obj.returnSaleNumber() == idIn:
                self.cardSaleList.remove(obj)
                break

    # !!WARNING!!
    # to delete a product all transactions  associated with this product must be deleted as well.
    # also, all machineslots associated need to have their productID set to null
    def deleteProduct(self, idIn: int) -> None:
        # delete all associated transactions
        cursor.execute("DELETE FROM `transaction` WHERE ProductID = " + str(idIn))
        # set machineslot row to null/none
        cursor.execute("UPDATE machineslot SET productID = NULL WHERE ProductID = " + str(idIn))
        # remove row from db
        machDB.commit()
        cursor.execute("DELETE FROM `product` WHERE productID = " + str(idIn))
        machDB.commit()

        # remove from all lists
        temp = []
        for obj in self.productList:
            if obj.returnProductID() == idIn:
                temp.append(obj)
        for rem in temp:
            self.productList.remove(rem)

        temp = []
        for obj in self.cashSaleList:
            if obj.returnProduct().returnProductID() == idIn:
                temp.append(obj)
        for rem in temp:
            self.cashSaleList.remove(rem)

        temp = []
        for obj in self.cardSaleList:
            if obj.returnProduct().returnProductID() == idIn:
                temp.append(obj)
        for rem in temp:
            self.cardSaleList.remove(rem)

        # update machineSlot list
        for obj in self.machineSlotList:
            if obj.returnProductHeld() != None and obj.returnProductHeld().returnProductID() == idIn:
                obj.updateProduct(None)

    def deleteMaintenanceRequest(self, idIn: int) -> None:
        # remove row from db
        cursor.execute("DELETE FROM maintenanceRequest WHERE maintenanceRequestID = " + str(idIn))
        machDB.commit()
        # remove from list
        for obj in self.maintenanceRequestList:
            if obj.returnMaintenanceRequestID() == idIn:
                self.maintenanceRequestList.remove(obj)
                break

    # !!WARNING!!
    # to delete a serviceworker all restockRequests and maintenanceRequests associated with this product must be deleted as well.
    # function deletes all associated restockRequests and maintenanceRequests to do this
    def deleteServiceWorker(self) -> None:
        pass # TODO

    # !!WARNING!!
    # to delete a machine, all associated information must be deleted as well
    # this cascades to deleting ALL classes associated with this machine, which is a lot
    def deleteMachine(self) -> None:
        pass # TODO


    ### list returns
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
