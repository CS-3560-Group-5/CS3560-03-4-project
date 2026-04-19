from allClasses import allClasses


temp = allClasses()
monHandList = temp.returnMoneyHandlerList()
machineList = temp.returnMachineList()
machineSlotList = temp.returnMachineSlotList()
workerList = temp.returnServiceWorkerList()

temp.addRestockRequest(workerList[0], monHandList[0], "1,1,2020", None, "aaaaaaaaaaaaaaaaaaaaaaaaaaa")

restockReqList = temp.returnRestockRequestList()
for n in restockReqList:
    print(n.returnAssignedMoneyHandler())
    print(n.returnDateResolved())