CREATE DATABASE  IF NOT EXISTS `vendingmachine` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `vendingmachine`;
-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: vendingmachine
-- ------------------------------------------------------
-- Server version	8.0.45

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
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `currency`
--

LOCK TABLES `currency` WRITE;
/*!40000 ALTER TABLE `currency` DISABLE KEYS */;
INSERT INTO `currency` VALUES (1,1,9,50,0.01),(2,1,35,60,0.05),(3,1,55,60,0.1),(4,1,30,60,0.25),(5,1,30,NULL,1),(6,1,60,NULL,5);
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
  PRIMARY KEY (`MachineID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `machine`
--

LOCK TABLES `machine` WRITE;
/*!40000 ALTER TABLE `machine` DISABLE KEYS */;
INSERT INTO `machine` VALUES (1,'1234 Oak Ave Springfield, IL 62704','3756-B','Operational','2025-09-22',180);
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
INSERT INTO `machineslot` VALUES ('1A',NULL,NULL,NULL,NULL,NULL),('1B',1,3,1,10,0.2),('1C',5,NULL,5,15,0.2),('1D',2,NULL,8,10,0.1),('1E',6,5,0,10,0.3),('2A',3,NULL,5,10,0.2),('2B',1,NULL,7,10,0.2),('2C',NULL,NULL,NULL,NULL,NULL),('2D',5,NULL,15,20,0.2),('2E',4,NULL,20,20,0.1);
/*!40000 ALTER TABLE `machineslot` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maintenancerequest`
--

DROP TABLE IF EXISTS `maintenancerequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maintenancerequest` (
  `MaintenanceRequestID` int unsigned NOT NULL AUTO_INCREMENT,
  `MachineID` int unsigned NOT NULL,
  `ServiceWorkerID` int unsigned NOT NULL,
  `DateRequested` date DEFAULT NULL,
  `DateResolved` date DEFAULT NULL,
  `ReasonForRequest` mediumtext,
  PRIMARY KEY (`MaintenanceRequestID`),
  KEY `MachineID` (`MachineID`),
  KEY `ServiceWorkerID` (`ServiceWorkerID`),
  CONSTRAINT `maintenancerequest_ibfk_1` FOREIGN KEY (`MachineID`) REFERENCES `machine` (`MachineID`),
  CONSTRAINT `maintenancerequest_ibfk_2` FOREIGN KEY (`ServiceWorkerID`) REFERENCES `serviceworker` (`WorkerID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maintenancerequest`
--

LOCK TABLES `maintenancerequest` WRITE;
/*!40000 ALTER TABLE `maintenancerequest` DISABLE KEYS */;
INSERT INTO `maintenancerequest` VALUES (1,1,3,'2025-03-20','2025-03-21','Error in Button Module | Service Notes: Fixed'),(2,1,1,'2026-03-25','2026-03-26','Error in Lighting Module | Service Notes: Fixed'),(3,1,1,'2026-03-25',NULL,'Error in Lighting Module'),(4,1,3,'2025-03-20',NULL,'Error in Button Module'),(5,1,1,'2026-03-21',NULL,'Auto-Scheduled Servicing');
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,1,'Cheetos','bagged puff chips. cheddar cheese flavored. orange packaging.','1 Serving Per Container. Serving Size 21 pieces / 28g. 160 Calories.','Corn, Salt, Cheese',3.99),(2,1,'Dr Pepper','canned soda. cherry flavored. dark red and white packaging','1 Serving Per Container. Serving Size 1 can / 20oz. 240 Calories.','Carbonated Water, High Fructose Corn Syrup, Caramel',2.98),(3,1,'Snickers','wrapped candy bar. chocolate, nougat, and caramel. brown, blue, red, and white packaging','1 Serving Per Container. Serving Size 1 bar / 8 oz. 250 Calories.','Milk Chocolate, Sugar, Peanuts',5.5),(4,1,'Sprite','canned soda. lemon-lime flavored. green packaging.','1 Serving Per Container. Serving Size 1 can / 20oz. 240 Calories.','Carbonated Water, High Fructose Corn Syrup, Lemons',4.99),(5,1,'Bottled Water','Bottled water. Clear packaging','1 Serving Per Container. Serving Size 1 can / 20oz. 0 Calories.','Water, Minerals',1.59),(6,1,'Twinkie','Pastry. Clear packaging, yellow pastry','1 Serving Per Container. Serving Size 1 pastry / 5oz. 500 Calories.','Wheat, Sugar, Milk, Preservatives',6.99);
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `restockrequest`
--

LOCK TABLES `restockrequest` WRITE;
/*!40000 ALTER TABLE `restockrequest` DISABLE KEYS */;
INSERT INTO `restockrequest` VALUES (1,2,1,'2025-03-20',NULL,'Restock request in \"MoneyHandler\" : \"$0.01\" coins below restock threshold.'),(2,2,1,'2026-03-25',NULL,'Restock request in \"MoneyHandler\" : bills above restock threshold.'),(3,2,NULL,'2026-03-30',NULL,'Restock request in \"MachineSlot\" : Slot \"2B\" Product \"Cheetos\" below restock threshold.'),(4,2,1,'2025-03-20',NULL,'Restock request in \"MoneyHandler\" : \"$0.1\" coins above restock threshold.'),(5,2,NULL,'2025-03-20','2025-03-21','Restock request in \"MachineSlot\" : Slot \"1E\" Product \"Twinkie\" below restock threshold.');
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
  `WorkerType` varchar(63) DEFAULT NULL,
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
INSERT INTO `serviceworker` VALUES (1,1,'John Doe','Technician','555-555-5555','JohnDoe@gmail.com','Repair Works Inc'),(2,1,'Jane Doe','Restocker','123-456-7890','JaneDoe@hotmail.com','Venders United'),(3,1,'Fred Nerks','Technician','000-000-0000','FredNerks@yahoo.com','Repair Works Inc'), (4,1,'Joe Bloggs','Restocker','111-222-333','JoeBloggs@gmail.com','Stockers Inc');
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
INSERT INTO `transaction` VALUES (1,1,1,0.33,'2025-03-20 14:39:01',2.75,'9999',NULL),(2,1,1,0.33,'2026-03-25 00:00:00',NULL,NULL,5),(3,2,1,0.25,'2026-03-25 00:00:00',NULL,NULL,10),(4,1,1,0.33,'2026-03-30 00:00:00',1.5,'1234',NULL);
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

-- Dump completed on 2026-05-02 11:41:06
