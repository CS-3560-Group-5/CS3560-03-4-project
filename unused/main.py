# main
# 4/19/2026
from unused.allClasses import allClasses
from unused.machine import machine

classes = allClasses()
cardSaleList = classes.returnCardSaleList()
cashSaleList = classes.returnCashSaleList()
machineList = classes.returnMachineList()
productList = classes.returnProductList()

classes.deleteAll()

classes.addProduct(machine(1,"1","1",1,"1,1,2000","a",1), "a", "a", "a", "A", 1)