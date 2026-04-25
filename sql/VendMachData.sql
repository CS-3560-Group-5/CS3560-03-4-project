-- 4/12/2026
-- fills DB with sample data. expects tables to be made
-- only for one machine
-- this data is written for the date 4/12/2026

-- machine data
INSERT IGNORE INTO Machine VALUES(1, "1234 Oak Ave Springfield, IL 62704", "3756-B", "Operational", STR_TO_DATE('9-22-2025','%m-%d-%Y'), 180, 10);

-- serviceworker data
INSERT IGNORE INTO ServiceWorker VALUES(1, 1, "John Doe", "Technician", "555-555-5555", "JohnDoe@gmail.com", "Repair Works Inc");
INSERT IGNORE INTO ServiceWorker VALUES(2, 1, "Jane Doe", "Restocker", "123-456-7890", "JaneDoe@hotmail.com", "Venders United");
INSERT IGNORE INTO ServiceWorker VALUES(3, 1, "Fred Nerks", "Technician", "000-000-0000", "FredNerks@yahoo.com", "Repair Works Inc");

-- product data
INSERT IGNORE INTO Product VALUES(1, 1, "Cheetos", "bagged puff chips. cheddar cheese flavored. orange packaging.", 
"1 Serving Per Container. Serving Size 21 pieces / 28g. Amount Per Serving : 160 Calories, Total Fat 10g, Trans Fat 0g, Cholesterol 0mg, Sodium 200mg, Total Carbohydrate 15g, Dietary Fiber 0.5g, Total Sugars 1g, Includes 0g Added Sugars, Protein 2g",
"Enriched Corn Meal (Corn Meal, Ferrous Sulfate, Niacin, Thiamin Mononitrate, Riboflavin, Folic Acid), Vegetable Oil (Corn, Canola, and/or Sunflower Oil), Whey, Cheddar Cheese (Milk, Cheese Cultures, Salt, Enzymes), Salt, Maltodextrin (made from Corn), Natural and Artificial Flavors, Whey Protein Concentrate, Monosodium Glutamate, Lactic Acid, Citric Acid, Artificial Color (Yellow 6)",
3.99);
INSERT IGNORE INTO Product VALUES(2, 1, "Dr Pepper", "canned soda. cherry flavored. dark red and white packaging",
"1 Serving Per Container. Serving Size 1 can / 20oz. Amount Per Serving : Calories 240, Total Fat 0g, Saturated Fat 0g, Trans Fat 0g, Cholesterol 0mg, Sodium 95mg, Carbohydrates 66g, Dietary Fiber 0g, Total Sugars 65g, Added Sugars 65g, Protein 0g",
"Carbonated Water, High Fructose Corn Syrup, Caramel Color, Phosphoric Acid, Natural and Artificial Flavors, Sodium Benzoate, Caffeine. Caffine content: 41 mg / 12 fl oz",
2.98);
INSERT IGNORE INTO Product VALUES(3, 1, "Share Sized Snickers", "wrapped candy bar. chocolate, nougat, and caramel. brown, blue, red, and white packaging",
"1 Serving Per Container. Serving Size 1 bar / 8 oz. Amount Per Serving : Calories 250,  Total Fat 12 g, Saturated Fat 4.5 g, Trans Fat 0 g, Cholesterol<5 mg, Sodium 130 mg, Total Carbohydrate 32 g, Dietary Fiber 1 g, Total Sugars 27 g, Includes Added Sugars 25 g, Protein 5 g",
"Milk Chocolate (Sugar, Cocoa Butter, Chocolate, Skim Milk, Lactose, Milkfat, Soy Lecithin), Peanuts, Corn Syrup, Sugar, Palm Oil, Skim Milk, Lactose, Salt, Egg Whites, Artificial Flavor",
5.50);

-- moneyhandler data
INSERT IGNORE INTO moneyhandler VALUES(1, 1, .80, 100, .80, .20);

-- transaction data
INSERT IGNORE INTO `Transaction` VALUES(1, 1, 1, .33, STR_TO_DATE('2025-3-20T14:39:01.123','%Y-%m-%dT%H:%i:%s.%f'), 2.75, "4012888888881881", null); -- null value because this is a card transaction, not a cash transaction
INSERT IGNORE INTO `Transaction` VALUES(2, 1, 1, .33, STR_TO_DATE('3-25-2026','%m-%d-%Y'), null, null, 5.0); -- null because cash transaction, not card 
INSERT IGNORE INTO `Transaction` VALUES(3, 2, 1, .25, STR_TO_DATE('3-25-2026','%m-%d-%Y'), null, null, 10.0);
INSERT IGNORE INTO `Transaction` VALUES(4, 1, 1, .33, STR_TO_DATE('3-30-2026','%m-%d-%Y'), 1.50, "378282246310005", null);

-- maintenancerequest data
INSERT IGNORE INTO MaintenanceRequest VALUES(1, 1, 3, STR_TO_DATE('3-20-2025','%m-%d-%Y'), STR_TO_DATE('3 21 2025','%m %d %Y'), "Error in Button Module");
INSERT IGNORE INTO MaintenanceRequest VALUES(2, 1, 1, STR_TO_DATE('3-25-2026','%m-%d-%Y'), STR_TO_DATE('3-26-2026','%m-%d-%Y'), "Error in Lighting Module");
INSERT IGNORE INTO MaintenanceRequest VALUES(3, 1, 1, STR_TO_DATE('3-21-2026','%m-%d-%Y'), null, "Auto-Scheduled Servicing"); -- null dateresolved because not resolved yet

-- currency data
INSERT IGNORE INTO Currency VALUES(1, 1, 35, 50, .01); -- penny
INSERT IGNORE INTO Currency VALUES(2, 1, 80, null, 1.0); -- null currentamount because not a coin (1 dollar bill)
INSERT IGNORE INTO Currency VALUES(3, 1, 35, 60, 1.0);	-- 1 dollar coin

-- restockrequest data
INSERT IGNORE INTO RestockRequest VALUES(1, 2, 1, STR_TO_DATE('3-20-2025','%m-%d-%Y'), STR_TO_DATE('3 21 2025','%m %d %Y'), "Restock request in \"MoneyHandler\" : \"$.01\" coins below restock threshold.");
INSERT IGNORE INTO RestockRequest VALUES(2, 2, 1, STR_TO_DATE('3-25-2026','%m-%d-%Y'), null, "Restock request in \"MoneyHandler\" : \"$1\" dollar bills above restock threshold."); -- null dateresolved because not resolved yet
INSERT IGNORE INTO RestockRequest VALUES(3, 2, null, STR_TO_DATE('3-30-2026','%m-%d-%Y'), null, "Restock request in \"MachineSlot\" : Slot \"2B\" Product \"Cheetos\" below restock threshold."); -- null moneyhandlerID because not a money restock
INSERT IGNORE INTO RestockRequest VALUES(4, 2, null, STR_TO_DATE('3-30-2026','%m-%d-%Y'), null, "Restock request in \"MachineSlot\" : Slot \"2B\" Product \"Cheetos\" at position 2 expired.");

-- machineslot data
INSERT IGNORE INTO MachineSlot VALUES("1A", null, null, null, null, null); -- all null because empty slot
INSERT IGNORE INTO MachineSlot VALUES("2A", null, null, null, null, null);
INSERT IGNORE INTO MachineSlot VALUES("1B", 1, 3, 1, 10, .2);
INSERT IGNORE INTO MachineSlot VALUES("2B", 1, null, 3, 10, .2);
INSERT IGNORE INTO MachineSlot VALUES("1C", null, null, null, null, null);
INSERT IGNORE INTO MachineSlot VALUES("2C", null, null, null, null, null);
INSERT IGNORE INTO MachineSlot VALUES("1D", 2, null, 3, 10, .1);
INSERT IGNORE INTO MachineSlot VALUES("2D", null, null, null, null, null);
INSERT IGNORE INTO MachineSlot VALUES("1E", null, null, null, null, null);
INSERT IGNORE INTO MachineSlot VALUES("2E", null, null, null, null, null);

-- perishableitem data
INSERT IGNORE INTO PerishableItem VALUES(1, "1B", null, STR_TO_DATE('3-12-2027','%m-%d-%Y'), 10, 1);
INSERT IGNORE INTO PerishableItem VALUES(2, "2B", null, STR_TO_DATE('3-12-2027','%m-%d-%Y'), 10, 1);
INSERT IGNORE INTO PerishableItem VALUES(3, "2B", 4, STR_TO_DATE('4-9-2026','%m-%d-%Y'), 10, 2); -- this one is past the expiration date and is no good
INSERT IGNORE INTO PerishableItem VALUES(4, "2B", null, STR_TO_DATE('3-10-2027','%m-%d-%Y'), 10, 3);
INSERT IGNORE INTO PerishableItem VALUES(5, "1D", null, STR_TO_DATE('4-11-2027','%m-%d-%Y'), 10, 1);
INSERT IGNORE INTO PerishableItem VALUES(6, "1D", null, STR_TO_DATE('4-10-2027','%m-%d-%Y'), 10, 2);
INSERT IGNORE INTO PerishableItem VALUES(7, "1D", null, STR_TO_DATE('4-10-2027','%m-%d-%Y'), 10, 3);




