-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: vendingmachine
-- ------------------------------------------------------
-- Server version	8.0.45
CREATE DATABASE IF NOT EXISTS `VendingMachine`;

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `currency`
--

DROP TABLE IF EXISTS `currency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `currency` (
  `CurrencyID` int unsigned NOT NULL AUTO_INCREMENT,
  `MoneyHandlerID` int unsigned NOT NULL,
  `CurrentAmount` int DEFAULT NULL,
  `MaxAmount` int DEFAULT NULL,
  `CurrencyWorth` double DEFAULT NULL,
  PRIMARY KEY (`CurrencyID`),
  KEY `MoneyHandlerID` (`MoneyHandlerID`),
  CONSTRAINT `currency_ibfk_1` FOREIGN KEY (`MoneyHandlerID`) REFERENCES `moneyhandler` (`MoneyHandlerID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `currency`
--

LOCK TABLES `currency` WRITE;
/*!40000 ALTER TABLE `currency` DISABLE KEYS */;
INSERT INTO `currency` VALUES (1,1,35,50,0.01),(2,1,80,NULL,1),(3,1,35,60,1);
/*!40000 ALTER TABLE `currency` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `machine`
--

DROP TABLE IF EXISTS `machine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `machine` (
  `MachineID` int unsigned NOT NULL AUTO_INCREMENT,
  `Address` varchar(255) DEFAULT NULL,
  `ModelNumber` varchar(127) DEFAULT NULL,
  `CurrentState` varchar(63) DEFAULT NULL,
  `DateLastServiced` date DEFAULT NULL,
  `DaysBetweenServices` int DEFAULT NULL,
  `MaxProductSlots` int DEFAULT NULL,
  PRIMARY KEY (`MachineID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `machine`
--

LOCK TABLES `machine` WRITE;
/*!40000 ALTER TABLE `machine` DISABLE KEYS */;
INSERT INTO `machine` VALUES (1,'1234 Oak Ave Springfield, IL 62704','3756-B','Operational','2025-09-22',180,10);
/*!40000 ALTER TABLE `machine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `machineslot`
--

DROP TABLE IF EXISTS `machineslot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `machineslot` (
  `SlotCode` varchar(15) NOT NULL,
  `ProductID` int unsigned DEFAULT NULL,
  `RestockRequestID` int unsigned DEFAULT NULL,
  `ProductCount` int DEFAULT NULL,
  `MaxAmount` int DEFAULT NULL,
  `RestockAtThreshold` double DEFAULT NULL,
  PRIMARY KEY (`SlotCode`),
  KEY `RestockRequestID` (`RestockRequestID`),
  KEY `ProductID` (`ProductID`),
  CONSTRAINT `machineslot_ibfk_1` FOREIGN KEY (`RestockRequestID`) REFERENCES `restockrequest` (`RestockRequestID`),
  CONSTRAINT `machineslot_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `product` (`ProductID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `machineslot`
--

LOCK TABLES `machineslot` WRITE;
/*!40000 ALTER TABLE `machineslot` DISABLE KEYS */;
INSERT INTO `machineslot` VALUES ('1A',NULL,NULL,NULL,NULL,NULL),('1B',1,3,1,10,0.2),('1C',NULL,NULL,NULL,NULL,NULL),('1D',2,NULL,3,10,0.1),('1E',NULL,NULL,NULL,NULL,NULL),('2A',NULL,NULL,NULL,NULL,NULL),('2B',1,NULL,3,10,0.2),('2C',NULL,NULL,NULL,NULL,NULL),('2D',NULL,NULL,NULL,NULL,NULL),('2E',NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `machineslot` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maintenancerequest`
--

DROP TABLE IF EXISTS `maintenancerequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maintenancerequest` (
  `MaintencanceRequestID` int unsigned NOT NULL AUTO_INCREMENT,
  `MachineID` int unsigned NOT NULL,
  `ServiceWorkerID` int unsigned NOT NULL,
  `DateRequested` date DEFAULT NULL,
  `DateResolved` date DEFAULT NULL,
  `ReasonForRequest` mediumtext,
  PRIMARY KEY (`MaintencanceRequestID`),
  KEY `MachineID` (`MachineID`),
  KEY `ServiceWorkerID` (`ServiceWorkerID`),
  CONSTRAINT `maintenancerequest_ibfk_1` FOREIGN KEY (`MachineID`) REFERENCES `machine` (`MachineID`),
  CONSTRAINT `maintenancerequest_ibfk_2` FOREIGN KEY (`ServiceWorkerID`) REFERENCES `serviceworker` (`WorkerID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maintenancerequest`
--

LOCK TABLES `maintenancerequest` WRITE;
/*!40000 ALTER TABLE `maintenancerequest` DISABLE KEYS */;
INSERT INTO `maintenancerequest` VALUES (1,1,3,'2025-03-20','2025-03-21','Error in Button Module'),(2,1,1,'2026-03-25','2026-03-26','Error in Lighting Module'),(3,1,2,'2026-03-21',NULL,'Auto-Scheduled Servicing');
/*!40000 ALTER TABLE `maintenancerequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `moneyhandler`
--

DROP TABLE IF EXISTS `moneyhandler`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `moneyhandler` (
  `MoneyHandlerID` int unsigned NOT NULL AUTO_INCREMENT,
  `MachineID` int unsigned NOT NULL,
  `BillRestockMaxThreshold` double DEFAULT NULL,
  `BillMaxAmount` int DEFAULT NULL,
  `CoinRestockMaxThreshold` double DEFAULT NULL,
  `CoinRestockMinThreshold` double DEFAULT NULL,
  PRIMARY KEY (`MoneyHandlerID`),
  KEY `MachineID` (`MachineID`),
  CONSTRAINT `moneyhandler_ibfk_1` FOREIGN KEY (`MachineID`) REFERENCES `machine` (`MachineID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `moneyhandler`
--

LOCK TABLES `moneyhandler` WRITE;
/*!40000 ALTER TABLE `moneyhandler` DISABLE KEYS */;
INSERT INTO `moneyhandler` VALUES (1,1,0.8,100,0.8,0.2);
/*!40000 ALTER TABLE `moneyhandler` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `perishableitem`
--

DROP TABLE IF EXISTS `perishableitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `perishableitem` (
  `PerishableItemID` int unsigned NOT NULL AUTO_INCREMENT,
  `MachineSlotID` varchar(15) NOT NULL,
  `RestockRequestID` int unsigned DEFAULT NULL,
  `DateExpire` date DEFAULT NULL,
  `RestockDaysBeforeExpire` int DEFAULT NULL,
  `SlotPosition` int DEFAULT NULL,
  PRIMARY KEY (`PerishableItemID`),
  KEY `MachineSlotID` (`MachineSlotID`),
  KEY `RestockRequestID` (`RestockRequestID`),
  CONSTRAINT `perishableitem_ibfk_1` FOREIGN KEY (`MachineSlotID`) REFERENCES `machineslot` (`SlotCode`),
  CONSTRAINT `perishableitem_ibfk_2` FOREIGN KEY (`RestockRequestID`) REFERENCES `restockrequest` (`RestockRequestID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `perishableitem`
--

LOCK TABLES `perishableitem` WRITE;
/*!40000 ALTER TABLE `perishableitem` DISABLE KEYS */;
INSERT INTO `perishableitem` VALUES (1,'1B',NULL,'2027-03-12',10,1),(2,'2B',NULL,'2027-03-12',10,1),(3,'2B',4,'2026-04-09',10,2),(4,'2B',NULL,'2027-03-10',10,3),(5,'1D',NULL,'2027-04-11',10,1),(6,'1D',NULL,'2027-04-10',10,2),(7,'1D',NULL,'2027-04-10',10,3);
/*!40000 ALTER TABLE `perishableitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `ProductID` int unsigned NOT NULL AUTO_INCREMENT,
  `MachineID` int unsigned NOT NULL,
  `Name` varchar(127) DEFAULT NULL,
  `Description` mediumtext,
  `NutritionFacts` mediumtext,
  `Ingredients` mediumtext,
  `Price` double DEFAULT NULL,
  PRIMARY KEY (`ProductID`),
  KEY `MachineID` (`MachineID`),
  CONSTRAINT `product_ibfk_1` FOREIGN KEY (`MachineID`) REFERENCES `machine` (`MachineID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,1,'Cheetos','bagged puff chips. cheddar cheese flavored. orange packaging.','1 Serving Per Container. Serving Size 21 pieces / 28g. Amount Per Serving : 160 Calories, Total Fat 10g, Trans Fat 0g, Cholesterol 0mg, Sodium 200mg, Total Carbohydrate 15g, Dietary Fiber 0.5g, Total Sugars 1g, Includes 0g Added Sugars, Protein 2g','Enriched Corn Meal (Corn Meal, Ferrous Sulfate, Niacin, Thiamin Mononitrate, Riboflavin, Folic Acid), Vegetable Oil (Corn, Canola, and/or Sunflower Oil), Whey, Cheddar Cheese (Milk, Cheese Cultures, Salt, Enzymes), Salt, Maltodextrin (made from Corn), Natural and Artificial Flavors, Whey Protein Concentrate, Monosodium Glutamate, Lactic Acid, Citric Acid, Artificial Color (Yellow 6)',3.99),(2,1,'Dr Pepper','canned soda. cherry flavored. dark red and white packaging','1 Serving Per Container. Serving Size 1 can / 20oz. Amount Per Serving : Calories 240, Total Fat 0g, Saturated Fat 0g, Trans Fat 0g, Cholesterol 0mg, Sodium 95mg, Carbohydrates 66g, Dietary Fiber 0g, Total Sugars 65g, Added Sugars 65g, Protein 0g','Carbonated Water, High Fructose Corn Syrup, Caramel Color, Phosphoric Acid, Natural and Artificial Flavors, Sodium Benzoate, Caffeine. Caffine content: 41 mg / 12 fl oz',2.98),(3,1,'Share Sized Snickers','wrapped candy bar. chocolate, nougat, and caramel. brown, blue, red, and white packaging','1 Serving Per Container. Serving Size 1 bar / 8 oz. Amount Per Serving : Calories 250,  Total Fat 12 g, Saturated Fat 4.5 g, Trans Fat 0 g, Cholesterol<5 mg, Sodium 130 mg, Total Carbohydrate 32 g, Dietary Fiber 1 g, Total Sugars 27 g, Includes Added Sugars 25 g, Protein 5 g','Milk Chocolate (Sugar, Cocoa Butter, Chocolate, Skim Milk, Lactose, Milkfat, Soy Lecithin), Peanuts, Corn Syrup, Sugar, Palm Oil, Skim Milk, Lactose, Salt, Egg Whites, Artificial Flavor',5.5);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `restockrequest`
--

DROP TABLE IF EXISTS `restockrequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `restockrequest` (
  `RestockRequestID` int unsigned NOT NULL AUTO_INCREMENT,
  `ServiceWorkerID` int unsigned NOT NULL,
  `MoneyHandlerID` int unsigned DEFAULT NULL,
  `DateRequested` date DEFAULT NULL,
  `DateResolved` date DEFAULT NULL,
  `ReasonForRequest` mediumtext,
  PRIMARY KEY (`RestockRequestID`),
  KEY `MoneyHandlerID` (`MoneyHandlerID`),
  KEY `ServiceWorkerID` (`ServiceWorkerID`),
  CONSTRAINT `restockrequest_ibfk_1` FOREIGN KEY (`MoneyHandlerID`) REFERENCES `moneyhandler` (`MoneyHandlerID`),
  CONSTRAINT `restockrequest_ibfk_2` FOREIGN KEY (`ServiceWorkerID`) REFERENCES `serviceworker` (`WorkerID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `restockrequest`
--

LOCK TABLES `restockrequest` WRITE;
/*!40000 ALTER TABLE `restockrequest` DISABLE KEYS */;
INSERT INTO `restockrequest` VALUES (1,3,1,'2025-03-20','2025-03-21','Restock request in \"MoneyHandler\" : \"$.01\" coins below restock threshold.'),(2,2,1,'2026-03-25',NULL,'Restock request in \"MoneyHandler\" : \"$1\" dollar bills above restock threshold.'),(3,1,NULL,'2026-03-30',NULL,'Restock request in \"MachineSlot\" : Slot \"2B\" Product \"Cheetos\" below restock threshold.'),(4,2,NULL,'2026-03-30',NULL,'Restock request in \"MachineSlot\" : Slot \"2B\" Product \"Cheetos\" at position 2 expired.');
/*!40000 ALTER TABLE `restockrequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `serviceworker`
--

DROP TABLE IF EXISTS `serviceworker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `serviceworker` (
  `WorkerID` int unsigned NOT NULL AUTO_INCREMENT,
  `MachineID` int unsigned NOT NULL,
  `Name` varchar(63) DEFAULT NULL,
  `PhoneNumber` varchar(31) DEFAULT NULL,
  `Email` varchar(63) DEFAULT NULL,
  `Company` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`WorkerID`),
  KEY `MachineID` (`MachineID`),
  CONSTRAINT `serviceworker_ibfk_1` FOREIGN KEY (`MachineID`) REFERENCES `machine` (`MachineID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `serviceworker`
--

LOCK TABLES `serviceworker` WRITE;
/*!40000 ALTER TABLE `serviceworker` DISABLE KEYS */;
INSERT INTO `serviceworker` VALUES (1,1,'John Doe','555-555-5555','JohnDoe@gmail.com','Repair Works Inc'),(2,1,'Jane Doe','123-456-7890','JaneDoe@hotmail.com','Venders United'),(3,1,'Fred Nerks','000-000-0000','FredNerks@yahoo.com','Repair Works Inc');
/*!40000 ALTER TABLE `serviceworker` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction`
--

DROP TABLE IF EXISTS `transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaction` (
  `SaleNumber` int unsigned NOT NULL AUTO_INCREMENT,
  `ProductID` int unsigned NOT NULL,
  `MachineID` int unsigned NOT NULL,
  `Tax` double DEFAULT NULL,
  `SaleDateTime` datetime DEFAULT NULL,
  `CardFee` double DEFAULT NULL,
  `AccountCharged` varchar(127) DEFAULT NULL,
  `CashGiven` double DEFAULT NULL,
  PRIMARY KEY (`SaleNumber`),
  KEY `ProductID` (`ProductID`),
  KEY `MachineID` (`MachineID`),
  CONSTRAINT `transaction_ibfk_1` FOREIGN KEY (`ProductID`) REFERENCES `product` (`ProductID`),
  CONSTRAINT `transaction_ibfk_2` FOREIGN KEY (`MachineID`) REFERENCES `machine` (`MachineID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction`
--

LOCK TABLES `transaction` WRITE;
/*!40000 ALTER TABLE `transaction` DISABLE KEYS */;
INSERT INTO `transaction` VALUES (1,1,1,0.33,'2025-03-20 14:39:01',2.75,'4012888888881881',NULL),(2,1,1,0.33,'2026-03-25 00:00:00',NULL,NULL,5),(3,2,1,0.25,'2026-03-25 00:00:00',NULL,NULL,10),(4,1,1,0.33,'2026-03-30 00:00:00',1.5,'378282246310005',NULL);
/*!40000 ALTER TABLE `transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'vendingmachine'
--

--
-- Dumping routines for database 'vendingmachine'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-18  8:23:45
