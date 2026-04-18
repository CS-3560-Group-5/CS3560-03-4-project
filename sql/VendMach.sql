-- 4/12/2026
-- sql for vending machine cs3560 project
-- main table making and foreign key linking
-- doesn't add any sample data

-- make vending machine database
CREATE DATABASE IF NOT EXISTS `VendingMachine`;

-- create commands for all tables
-- create in this order : machine, serviceworker, product, moneyhandler, transaction, maintenancerequest, currency, restockrequest, machineslot, perishableitem
-- Machine table. where general info is stored for the vending machine.
CREATE TABLE IF NOT EXISTS `Machine` (
	-- private keys
	`MachineID` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT, -- pk
    PRIMARY KEY(`MachineID`),
    -- attributes
	`Address` VARCHAR(255),
    `ModelNumber` VARCHAR(127),
    `CurrentState` VARCHAR(63),
    `DateLastServiced` Date,
    `DaysBetweenServices` INTEGER,
	`MaxProductSlots` INTEGER
);

-- ServiceWorker table
CREATE TABLE IF NOT EXISTS `ServiceWorker` (
	-- private/foreign keys
	`WorkerID` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT, -- pk. both specification classes have been collapsed into a single workerID attribute
    PRIMARY KEY(`WorkerID`),
    `MachineID` INTEGER UNSIGNED NOT NULL, -- fk
	FOREIGN KEY(`MachineID`) REFERENCES `Machine`(`MachineID`),
    -- attributes
    `Name` VARCHAR(63),
    `PhoneNumber` VARCHAR(31),
    `Email` VARCHAR(63),
    `Company` VARCHAR(255)
);

-- Product table
CREATE TABLE IF NOT EXISTS `Product` (
	-- private/foreign keys
	`ProductID` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT, -- pk
    PRIMARY KEY(`ProductID`),
    `MachineID` INTEGER UNSIGNED NOT NULL, -- fk
    FOREIGN KEY(`MachineID`) REFERENCES `Machine`(`MachineID`),
    -- attributes
    `Name` VARCHAR(127),
    `Description` MEDIUMTEXT,
    `NutritionFacts` MEDIUMTEXT,
    `Ingredients` MEDIUMTEXT,
    `Price` DOUBLE
);

-- MoneyHandler table
-- all thresholds are held in percents. They are to be applied to the max num of that currency to find the max values
CREATE TABLE IF NOT EXISTS `MoneyHandler` (
	-- private/foreign keys
	`MoneyHandlerID` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT, -- pk
	PRIMARY KEY(`MoneyHandlerID`),
    `MachineID` INTEGER UNSIGNED NOT NULL, -- fk
	FOREIGN KEY(`MachineID`) REFERENCES `Machine`(`MachineID`),
    -- attributes
    `BillRestockMaxThreshold` DOUBLE,
    `BillMaxAmount` INTEGER,
    `CoinRestockMaxThreshold` DOUBLE,
    `CoinRestockMinThreshold` DOUBLE
);

-- Transaction table
CREATE TABLE IF NOT EXISTS `Transaction` (
	-- private/foreign keys
	`SaleNumber` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT, -- pk
    PRIMARY KEY(`SaleNumber`),
    `ProductID` INTEGER UNSIGNED NOT NULL, -- fk1
	`MachineID` INTEGER UNSIGNED NOT NULL, -- fk2
	FOREIGN KEY(`ProductID`) REFERENCES `Product`(`ProductID`),
	FOREIGN KEY(`MachineID`) REFERENCES `Machine`(`MachineID`),
    -- attributes
    `Tax` DOUBLE,
    `SaleDateTime` DateTime,
    -- spec. class cardSale attributes
    `CardFee` DOUBLE,
    `AccountCharged` VARCHAR(127),
    -- spec. class cashSale attributes
    `CashGiven` DOUBLE -- customer can give dollars or coins in change, so this a double
);

-- MaintenanceRequest Table
CREATE TABLE IF NOT EXISTS `MaintenanceRequest` (
	-- private/foreign keys
	`MaintencanceRequestID` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT, -- pk
    PRIMARY KEY(`MaintencanceRequestID`),
    `MachineID` INTEGER UNSIGNED NOT NULL, -- fk1
	`ServiceWorkerID` INTEGER UNSIGNED NOT NULL, -- fk2
	FOREIGN KEY(`MachineID`) REFERENCES `Machine`(`MachineID`),
	FOREIGN KEY(`ServiceWorkerID`) REFERENCES `ServiceWorker`(`WorkerID`),
   -- attributes
    `DateRequested` Date,
    `DateResolved` Date, -- when a MaintenanceRequest isn't resolved, its DateResolved value will be null. this is how you know a maintenance request is still open
    `ReasonForRequest` MEDIUMTEXT
);

-- Currency table
CREATE TABLE IF NOT EXISTS `Currency` (
	-- private/foreign key
	`CurrencyID` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT, -- pk
	PRIMARY KEY(`CurrencyID`),
   `MoneyHandlerID` INTEGER UNSIGNED NOT NULL, -- fk
	FOREIGN KEY(`MoneyHandlerID`) REFERENCES `MoneyHandler`(`MoneyHandlerID`),
   -- attributes
    `CurrentAmount` INTEGER,
    `MaxAmount`	INTEGER,
    `CurrencyWorth` DOUBLE -- the spec. class coin and bill worth attributes have been collapsed into a single "CurrencyWorth" attribute
);

-- RestockRequest table
CREATE TABLE IF NOT EXISTS `RestockRequest` (
	-- private/foreign keys
	`RestockRequestID` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT, -- pk
    PRIMARY KEY(`RestockRequestID`),
    `ServiceWorkerID` INTEGER UNSIGNED NOT NULL, -- fk1
	`MoneyHandlerID` INTEGER UNSIGNED, -- fk2
	FOREIGN KEY(`MoneyHandlerID`) REFERENCES `MoneyHandler`(`MoneyHandlerID`),
	FOREIGN KEY(`ServiceWorkerID`) REFERENCES `ServiceWorker`(`WorkerID`),
    -- attributes
	`DateRequested` Date,
    `DateResolved` Date, -- when a RestockRequest isn't resolved, its DateResolved value will be null. this is how you know a maintenance request is still open
    `ReasonForRequest` MEDIUMTEXT
);

-- MachineSlot table
-- all thresholds are held in percents
CREATE TABLE IF NOT EXISTS `MachineSlot` (
	-- private/foreign keys
	`SlotCode` VARCHAR(15) NOT NULL, -- pk
	PRIMARY KEY(`SlotCode`),
    `ProductID` INTEGER UNSIGNED, -- fk1
	`RestockRequestID` INTEGER UNSIGNED, -- fk2
	FOREIGN KEY(`RestockRequestID`) REFERENCES `RestockRequest`(`RestockRequestID`),
	FOREIGN KEY(`ProductID`) REFERENCES `Product`(`ProductID`),
    -- attributes
    `ProductCount` INTEGER,
    `MaxAmount` INTEGER,
    `RestockAtThreshold` DOUBLE
);

-- PerishableItem table
CREATE TABLE IF NOT EXISTS `PerishableItem` (
	-- private/foreign key
	`PerishableItemID` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT, -- pk
    PRIMARY KEY(`PerishableItemID`),
    `MachineSlotID` VARCHAR(15) NOT NULL, -- fk1
	`RestockRequestID` INTEGER UNSIGNED, -- fk2
    FOREIGN KEY(`MachineSlotID`) REFERENCES `MachineSlot`(`SlotCode`),
	FOREIGN KEY(`RestockRequestID`) REFERENCES `RestockRequest`(`RestockRequestID`),
    -- attributes
    `DateExpire` Date,
    `RestockDaysBeforeExpire` INTEGER,
    `SlotPosition` INTEGER -- starts at 1, goes to machineSlot.maxAmount
);

