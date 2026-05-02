-- 4/12/2026
-- fills DB with sample data. expects tables to be made
-- only for one machine
-- this data is written for the date 4/12/2026

-- machine data
INSERT IGNORE INTO Machine VALUES(1, "1234 Oak Ave Springfield, IL 62704", "3756-B", "Operational", STR_TO_DATE('9-22-2025','%m-%d-%Y'), 180);

-- serviceworker data
INSERT IGNORE INTO ServiceWorker VALUES(1, 1, "John Doe", "Technician", "555-555-5555", "JohnDoe@gmail.com", "Repair Works Inc");
INSERT IGNORE INTO ServiceWorker VALUES(2, 1, "Jane Doe", "Restocker", "123-456-7890", "JaneDoe@hotmail.com", "Venders United");
INSERT IGNORE INTO ServiceWorker VALUES(3, 1, "Fred Nerks", "Technician", "000-000-0000", "FredNerks@yahoo.com", "Repair Works Inc");

-- product data
INSERT IGNORE INTO Product VALUES(1, 1, "Cheetos", "bagged puff chips. cheddar cheese flavored. orange packaging.", 
"1 Serving Per Container. Serving Size 21 pieces / 28g. 160 Calories.",
"Corn, Salt, Cheese",
3.99);
INSERT IGNORE INTO Product VALUES(2, 1, "Dr Pepper", "canned soda. cherry flavored. dark red and white packaging",
"1 Serving Per Container. Serving Size 1 can / 20oz. 240 Calories.",
"Carbonated Water, High Fructose Corn Syrup, Caramel",
2.98);
INSERT IGNORE INTO Product VALUES(3, 1, "Snickers", "wrapped candy bar. chocolate, nougat, and caramel. brown, blue, red, and white packaging",
"1 Serving Per Container. Serving Size 1 bar / 8 oz. 250 Calories.",
"Milk Chocolate, Sugar, Peanuts",
5.50);

INSERT IGNORE INTO Product VALUES(4, 1, "Sprite", "canned soda. lemon-lime flavored. green packaging.",
"1 Serving Per Container. Serving Size 1 can / 20oz. 240 Calories.",
"Carbonated Water, High Fructose Corn Syrup, Lemons",
4.99);

INSERT IGNORE INTO Product VALUES(5, 1, "Bottled Water", "Bottled water. Clear packaging",
"1 Serving Per Container. Serving Size 1 can / 20oz. 0 Calories.",
"Water, Minerals",
1.59);

INSERT IGNORE INTO Product VALUES(6, 1, "Twinkie", "Pastry. Clear packaging, yellow pastry",
"1 Serving Per Container. Serving Size 1 pastry / 5oz. 500 Calories.",
"Wheat, Sugar, Milk, Preservatives",
6.99);

-- moneyhandler data
INSERT IGNORE INTO moneyhandler VALUES(1, 1, .80, 100, .80, .20);

-- transaction data
INSERT IGNORE INTO `Transaction` VALUES(1, 1, 1, .33, STR_TO_DATE('2025-3-20T14:39:01.123','%Y-%m-%dT%H:%i:%s.%f'), 2.75, "9999", null); -- null value because this is a card transaction, not a cash transaction
INSERT IGNORE INTO `Transaction` VALUES(2, 1, 1, .33, STR_TO_DATE('3-25-2026','%m-%d-%Y'), null, null, 5.0); -- null because cash transaction, not card 
INSERT IGNORE INTO `Transaction` VALUES(3, 2, 1, .25, STR_TO_DATE('3-25-2026','%m-%d-%Y'), null, null, 10.0);
INSERT IGNORE INTO `Transaction` VALUES(4, 1, 1, .33, STR_TO_DATE('3-30-2026','%m-%d-%Y'), 1.50, "1234", null);

-- maintenancerequest data
INSERT IGNORE INTO MaintenanceRequest VALUES(1, 1, 3, STR_TO_DATE('3-20-2025','%m-%d-%Y'), STR_TO_DATE('3 21 2025','%m %d %Y'), "Error in Button Module");
INSERT IGNORE INTO MaintenanceRequest VALUES(2, 1, 1, STR_TO_DATE('3-25-2026','%m-%d-%Y'), STR_TO_DATE('3-26-2026','%m-%d-%Y'), "Error in Lighting Module");
INSERT IGNORE INTO MaintenanceRequest VALUES(3, 1, 1, STR_TO_DATE('3-25-2026','%m-%d-%Y'), null, "Error in Lighting Module");
INSERT IGNORE INTO MaintenanceRequest VALUES(4, 1, 3, STR_TO_DATE('3-20-2025','%m-%d-%Y'), null, "Error in Button Module");
INSERT IGNORE INTO MaintenanceRequest VALUES(5, 1, 1, STR_TO_DATE('3-21-2026','%m-%d-%Y'), null, "Auto-Scheduled Servicing"); -- null dateresolved because not resolved yet

-- currency data
INSERT IGNORE INTO Currency VALUES(1, 1, 9, 50, .01); -- penny
INSERT IGNORE INTO Currency VALUES(2, 1, 35, 60, .05);	-- nickel
INSERT IGNORE INTO Currency VALUES(3, 1, 55, 60, 1.0);	-- dime
INSERT IGNORE INTO Currency VALUES(4, 1, 30, 60, 1.0);	-- quarter
INSERT IGNORE INTO Currency VALUES(5, 1, 30, null, 1.0); -- null currentamount because not a coin (1 dollar bill)
INSERT IGNORE INTO Currency VALUES(6, 5, 32, null, 5.0); -- null currentamount because not a coin (5 dollar bill)
INSERT IGNORE INTO Currency VALUES(7, 10, 20, null, 10.0); -- null currentamount because not a coin (10 dollar bill)

-- restockrequest data
INSERT IGNORE INTO RestockRequest VALUES(1, 2, 1, STR_TO_DATE('3-20-2025','%m-%d-%Y'), STR_TO_DATE('3 21 2025','%m %d %Y'), "Restock request in \"MoneyHandler\" : \"$.01\" coins below restock threshold.");
INSERT IGNORE INTO RestockRequest VALUES(2, 2, 1, STR_TO_DATE('3-25-2026','%m-%d-%Y'), null, "Restock request in \"MoneyHandler\" : bills above restock threshold."); -- null dateresolved because not resolved yet
INSERT IGNORE INTO RestockRequest VALUES(3, 2, null, STR_TO_DATE('3-30-2026','%m-%d-%Y'), null, "Restock request in \"MachineSlot\" : Slot \"2B\" Product \"Cheetos\" below restock threshold."); -- null moneyhandlerID because not a money restock
INSERT IGNORE INTO RestockRequest VALUES(4, 2, 1, STR_TO_DATE('3-20-2025','%m-%d-%Y'), STR_TO_DATE('3 21 2025','%m %d %Y'), "Restock request in \"MoneyHandler\" : \"$.1\" coins above restock threshold.");
INSERT IGNORE INTO RestockRequest VALUES(5, 2, null, STR_TO_DATE('3-20-2025','%m-%d-%Y'), STR_TO_DATE('3 21 2025','%m %d %Y'), "Restock request in \"MachineSlot\" : Slot \"1E\" Product \"Twinkie\" below restock threshold."); 


-- machineslot data
INSERT IGNORE INTO MachineSlot VALUES("1A", null, null, null, null, null); -- all null because empty slot
INSERT IGNORE INTO MachineSlot VALUES("2A", 3, null, 5, 10, .2);
INSERT IGNORE INTO MachineSlot VALUES("1B", 1, 3, 1, 10, .2);
INSERT IGNORE INTO MachineSlot VALUES("2B", 1, null, 7, 10, .2);
INSERT IGNORE INTO MachineSlot VALUES("1C", 5, null, 5, 15, .2);
INSERT IGNORE INTO MachineSlot VALUES("2C", null, null, null, null, null);
INSERT IGNORE INTO MachineSlot VALUES("1D", 2, null, 8, 10, .1);
INSERT IGNORE INTO MachineSlot VALUES("2D", 5, null, 15, 20, .2);
INSERT IGNORE INTO MachineSlot VALUES("1E", 6, 5, 0, 10, .3);
INSERT IGNORE INTO MachineSlot VALUES("2E", 4, null, 20, 20, .1);




