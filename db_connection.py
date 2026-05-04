# db_connection.py
# 4/23/2026 — Updated 4/27/2026
# Database connection module for the Vending Machine System
# Provides functions to read from and write to the MySQL database
# This module bridges the GUI with the backend MySQL database

import math
import random
import mysql.connector
from datetime import datetime

# Establishes and returns a connection to the vendingmachine database
def get_connection():
    # Creates and returns a new MySQL database connection
    return mysql.connector.connect(
        host="localhost",
        user="interface",
        password="password",
        database="vendingmachine"
    )

# EDIT : needed for service worker logic throughout most functions
# Retrieves one service worker ID of the specified type back. Is random, picks one of the possible ones
def get_random_service_worker(typeIn, machine_id=1):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT WorkerID FROM ServiceWorker WHERE MachineID = %s AND WorkerType = %s", (machine_id, typeIn,))
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    if len(results) <= 0:
        return -1
    return random.choice(results)[0]

# ═══════════════════════════════════════════════════════════════
# MACHINE SLOT / PRODUCT FUNCTIONS
# Used by Record Sale and Update Inventory screens
# ═══════════════════════════════════════════════════════════════

# Retrieves all machine slots with their associated product info
# Returns a list of dictionaries, each representing a slot in the machine
# Empty slots (no product assigned) are included with placeholder values
def get_all_products_with_slots():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # LEFT JOIN ensures we get all slots, even empty ones without a product
    cursor.execute("""
        SELECT 
            ms.SlotCode AS code,
            ms.ProductCount AS count,
            ms.MaxAmount AS max,
            ms.RestockAtThreshold AS threshold,
            p.ProductID AS product_id,
            p.Name AS name,
            p.Price AS price,
            p.Description AS description
        FROM MachineSlot ms
        LEFT JOIN Product p ON ms.ProductID = p.ProductID
        ORDER BY ms.SlotCode
    """)

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    # Build list of slot dictionaries for the GUI
    slots = []
    for row in results:
        slots.append({
            "code":        row["code"],
            "name":        row["name"]        if row["name"]        else "Empty",
            "price":       float(row["price"]) if row["price"]       else 0.0,
            "count":       row["count"]        if row["count"]       is not None else 0,
            "max":         row["max"]          if row["max"]         is not None else 0,
            "product_id":  row["product_id"],
            "description": row["description"]  if row["description"] else "",
            "threshold":   float(row["threshold"]) if row["threshold"] is not None else 0.0
        })

    return slots


# Updates the product count for a specific machine slot
# Called after a sale (decrement) or after restocking (increment)
def update_slot_count(slot_code, new_count):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE MachineSlot
        SET ProductCount = %s
        WHERE SlotCode = %s
    """, (new_count, slot_code))

    conn.commit()
    cursor.close()
    conn.close()


# Adds a specified quantity to a machine slot's current product count
# Used by the Update Inventory screen when a restocker refills a slot
# Returns the new count after restocking, or -1 if it would exceed the maximum
def restock_slot(slot_code, add_quantity):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get current count and max to validate before applying
    cursor.execute("SELECT ProductCount, MaxAmount FROM MachineSlot WHERE SlotCode = %s", (slot_code,))
    row = cursor.fetchone()

    if row is None:
        cursor.close()
        conn.close()
        return None

    current = row["ProductCount"] if row["ProductCount"] is not None else 0
    max_amt = row["MaxAmount"]    if row["MaxAmount"]    is not None else 0
    new_count = current + add_quantity

    # Do not exceed the slot's maximum capacity
    if new_count > max_amt:
        cursor.close()
        conn.close()
        return -1  # Signal that the quantity exceeds max

    cursor.execute("UPDATE MachineSlot SET ProductCount = %s WHERE SlotCode = %s", (new_count, slot_code))
    conn.commit()
    cursor.close()
    conn.close()
    return new_count


# ═══════════════════════════════════════════════════════════════
# MACHINE INFO FUNCTIONS
# Used by the Home Screen and Update Machine Information screen
# ═══════════════════════════════════════════════════════════════

# Retrieves the main machine's profile from the database
# Returns a dictionary with machine details like address, model, and state
def get_machine_info():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Machine LIMIT 1")
    result = cursor.fetchone()

    cursor.close()
    conn.close()
    return result


# Updates the stored machine profile with new values provided by the admin
# Called by the Update Machine Information screen when the admin saves changes
def update_machine_info(machine_id, address, model_number, days_between_services, current_state):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Machine
        SET Address             = %s,
            ModelNumber         = %s,
            DaysBetweenServices = %s,
            CurrentState        = %s
        WHERE MachineID = %s
    """, (address, model_number, days_between_services, current_state, machine_id))

    conn.commit()
    cursor.close()
    conn.close()


# Updates only the CurrentState field of the machine record
# Called automatically (system-triggered) when maintenance tickets are opened or closed,
# and can also be called manually from the Update Machine Information screen
def update_machine_status(machine_id, new_status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Machine
        SET CurrentState = %s
        WHERE MachineID = %s
    """, (new_status, machine_id))

    conn.commit()
    cursor.close()
    conn.close()


# ═══════════════════════════════════════════════════════════════
# TRANSACTION FUNCTIONS
# Used by the Record Sale screen
# ═══════════════════════════════════════════════════════════════

# Records a card transaction in the database
# Inserts a new row into the Transaction table with card-specific fields
# Cash fields (CashGiven) are set to NULL for card transactions
def record_card_sale(product_id, machine_id, tax, card_fee, account_charged):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO `Transaction` (ProductID, MachineID, Tax, SaleDateTime, CardFee, AccountCharged, CashGiven)
        VALUES (%s, %s, %s, %s, %s, %s, NULL)
    """, (product_id, machine_id, tax, datetime.now(), card_fee, account_charged))

    conn.commit()
    sale_number = cursor.lastrowid  # Get the auto-generated SaleNumber
    cursor.close()
    conn.close()
    return sale_number

# checks to see if the db can give out x amount of money for change. false if no, true if yes
def check_cash_out(machine_id, change_out):
    if change_out <= 0:
        return True
    
    conn = get_connection()
    cursor = conn.cursor()

    net_dollars = change_out
    denominations = (5.0, 1.0, .25, .1, .05, .01)   # hardcoded bc only these bills will be in machine
    denom_count = [0, 0, 0, 0 ,0 ,0]

    # calc the number of each coin/bill
    for i, n in enumerate(denominations):
        if net_dollars <= 0:
            break
        update_amt = net_dollars / n
        if update_amt < 1:
            continue
        update_amt = math.floor(update_amt)
        net_dollars = round(net_dollars - (update_amt * n), 2)
        denom_count[i] = update_amt

    cursor.execute("""
        SELECT CurrencyWorth, CurrentAmount FROM `Currency` 
        WHERE MoneyHandlerID = (
                SELECT MoneyHandlerID FROM MoneyHandler WHERE MachineID = %s LIMIT 1
            );                        
    """, tuple(str(machine_id)))
    curr_amounts = cursor.fetchall()
    denom_count.reverse()
    
    # check if CurrentAmount - denom_count is less than 0
    for i, n in enumerate(denom_count):
        if curr_amounts[i][1] - n < 0:
            cursor.close()
            conn.close()
            return False
    
    cursor.close()
    conn.close()
    return True
    

# checks to see if the db can take x amount of money from a transaction. false if no, true if yes
def check_cash_in(machine_id, cash_given=0):
    if cash_given <= 0:
        return True
    
    conn = get_connection()
    cursor = conn.cursor()

    net_dollars = cash_given
    denominations = (5.0, 1.0, .25, .1, .05, .01)   # hardcoded bc only these bills will be in machine
    denom_count = [0, 0, 0, 0 ,0 ,0]

    # calc the number of each value in
    for i, n in enumerate(denominations):
        if net_dollars <= 0:
            break
        update_amt = net_dollars / n
        if update_amt < 1:
            continue
        update_amt = math.floor(update_amt)
        net_dollars = round(net_dollars - (update_amt * n), 2)
        denom_count[i] = update_amt
    # see if any of the current amounts would be too full
    cursor.execute("""
        SELECT CurrencyWorth, CurrentAmount, MaxAmount FROM `Currency` 
        WHERE MoneyHandlerID = (
                SELECT MoneyHandlerID FROM MoneyHandler WHERE MachineID = %s LIMIT 1
            );                        
    """, tuple(str(machine_id)))
    curr_amounts = cursor.fetchall()
    cursor.execute("""
        SELECT BillMaxAmount FROM `MoneyHandler`
        WHERE MoneyHandlerID = (
                SELECT MoneyHandlerID FROM MoneyHandler WHERE MachineID = %s LIMIT 1
            );
    """, tuple(str(machine_id)))
    billMax = cursor.fetchall()[0][0]
    billCount = 0

    # check coins
    denom_count.reverse()
    #print(denom_count)
    for i, m in enumerate(curr_amounts):
        if m[2] != None and m[1] + denom_count[i] > m[2]:
            cursor.close()
            conn.close()
            return False
            
    # count how many bills in machine
    for m in curr_amounts:
        if m[2] == None:
            billCount += m[1]
    # check if counted bills are too much
    if billCount > billMax:
        cursor.close()
        conn.close()
        return False
    
    cursor.close()
    conn.close()
    return True     # if passes all, then true

# Records a cash transaction in the database
# Inserts a new row into the Transaction table with cash-specific fields
# Card fields (CardFee, AccountCharged) are set to NULL for cash transactions
def record_cash_sale(product_id, machine_id, tax, cash_given, price=0.0):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO `Transaction` (ProductID, MachineID, Tax, SaleDateTime, CardFee, AccountCharged, CashGiven)
        VALUES (%s, %s, %s, %s, NULL, NULL, %s)
    """, (product_id, machine_id, tax, datetime.now(), cash_given))

    sale_number = cursor.lastrowid

    # Add net cash retained (price + tax) to all currencies
    # edit - updated code to allow for all coins and bills : pennies, nickels, dimes, quarters, 1 dollar bill, 5 dollar bill, 10 dollar bill
    # first put in money given by customer into db
    net_dollars = cash_given
    denominations = [5.0, 1.0, .25, .1, .05, .01]   # hardcoded bc only these bills will be in machine

    # apply all updates in loop
    for n in denominations:
        if net_dollars <= 0:
            break
        update_amt = net_dollars / n
        if update_amt < 1:
            continue
        update_amt = math.floor(update_amt)
        net_dollars = round(net_dollars - (update_amt * n), 2)
        cursor.execute("""
            UPDATE Currency
            SET CurrentAmount = CurrentAmount + %s
            WHERE MoneyHandlerID = (
                SELECT MoneyHandlerID FROM MoneyHandler WHERE MachineID = %s LIMIT 1
            )
            AND CurrencyWorth = %s
            LIMIT 1
        """, (update_amt, machine_id, n))
        conn.commit()

    # next remove change given back to customer by machine from db
    net_dollars = cash_given - (price + tax)

    # apply all updates in loop
    for n in denominations:
        if net_dollars <= 0:
            break
        update_amt = net_dollars / n
        if update_amt < 1:
            continue
        update_amt = math.floor(update_amt)
        net_dollars = round(net_dollars - (update_amt * n), 2)
        cursor.execute("""
            UPDATE Currency
            SET CurrentAmount = CurrentAmount - %s
            WHERE MoneyHandlerID = (
                SELECT MoneyHandlerID FROM MoneyHandler WHERE MachineID = %s LIMIT 1
            )
            AND CurrencyWorth = %s
            LIMIT 1
        """, (update_amt, machine_id, n))
        conn.commit()

    # end edit
    cursor.close()
    conn.close()
    return sale_number


# ═══════════════════════════════════════════════════════════════
# RESTOCK REQUEST FUNCTIONS
# System-triggered: called automatically after sales and after restocking
# ═══════════════════════════════════════════════════════════════

# Checks if a slot's product count has fallen below its restock threshold
# If so, creates a new restock request in the database
# Called after each sale to monitor inventory levels automatically
def check_and_create_restock_request(slot_code, worker_id=get_random_service_worker("Restocker")):
    # check for an empty service worker table
    if worker_id <= -1:
        return
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get the slot's current count, max, and restock threshold percentage
    cursor.execute("""
        SELECT ProductCount, MaxAmount, RestockAtThreshold 
        FROM MachineSlot 
        WHERE SlotCode = %s
    """, (slot_code,))
    row = cursor.fetchone()

    # edit : grab all unresolved restock requests 
    cursor.execute("""
        SELECT ReasonForRequest
        FROM RestockRequest
        WHERE MoneyHandlerID IS NULL AND DateResolved IS NULL
    """)
    requests = cursor.fetchall()

    exists = False
    if row and row["ProductCount"] is not None and row["MaxAmount"] is not None:
        count     = row["ProductCount"]
        max_amt   = row["MaxAmount"]
        threshold = row["RestockAtThreshold"] if row["RestockAtThreshold"] else 0.2

        # edit : functionality to not make the same restock request multiple times
        # sample restock request : Restock request in "MachineSlot" : Slot "1E" Product "Twinkie" below restock threshold.
        for request in requests:
            if "Slot" in request.get("ReasonForRequest") and slot_code in request.get("ReasonForRequest"):
                exists = True
                break

        # Create a restock request only if fill level is at or below the threshold
        if max_amt > 0 and (count / max_amt) <= threshold and exists == False:
            cursor.execute("""
                INSERT INTO RestockRequest (ServiceWorkerID, MoneyHandlerID, DateRequested, DateResolved, ReasonForRequest)
                VALUES (%s, NULL, %s, NULL, %s)
            """, (worker_id, datetime.now().date(),
                  f'Restock request in \"MachineSlot\" : Slot "{slot_code}" is at or below restock threshold.'))
            conn.commit()

    cursor.close()
    conn.close()
    return exists

def check_and_create_restock_request_ALL(worker_id=get_random_service_worker("Restocker")):
    # check for an empty service worker table
    if worker_id <= -1:
        return
    
    conn = get_connection()
    cursor = conn.cursor()

    # get all slot codes
    cursor.execute("""
        SELECT SlotCode FROM MachineSlot;
    """)
    ids = cursor.fetchall()
    print(ids)
    # loop thru check_and_create_currency_restock_request with ids
    rnd = False
    if worker_id == None:
        rnd = True
    results = []
    for id in ids:
        if rnd:
            worker_id = get_random_service_worker("Restocker")
        results.append(check_and_create_restock_request(id[0], worker_id))

    cursor.close()
    conn.close()
    return results

# checks a slot restock requests to see if it can be closed (is above the threshold now)
def resolve_slot_restock_request(slotcode):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # get slot info
    cursor.execute("""
        SELECT MaxAmount, ProductCount FROM MachineSlot
        WHERE SlotCode = %s;
    """, (slotcode,))
    slot_info = cursor.fetchall()

    # get all unresolved restock requests 
    cursor.execute("""
        SELECT RestockRequestID, ReasonForRequest FROM MachineSlot
        WHERE DateResolved IS NULL;
    """, (slotcode,))
    requests = cursor.fetchall()

    cursor.close()
    conn.close()

# checks if a currency has fallen below or above its restock thresholds
# if so, creates a new restock request in the database
# only does so if that specific restock request has NOT been made yet
# called after each sale to monitor inventory levels automatically
# returns boolean array with : [coin_under, coin_over, bills_over]
def check_and_create_currency_restock_request(currency_id, worker_id=get_random_service_worker("Restocker")):
    # check for empty service worker table
    if worker_id <= -1:
        return
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # get currencies current amount
    cursor.execute("""
        SELECT CurrentAmount, MaxAmount, CurrencyWorth FROM `currency` WHERE CurrencyID = %s;
    """, tuple(str(currency_id)))
    vals = cursor.fetchall()
    curr_amt = vals[0].get("CurrentAmount")
    max_amt = vals[0].get("MaxAmount")
    curr_worth = vals[0].get("CurrencyWorth")

    # get moneyhandler info (bill max and all threshs)
    cursor.execute("""
        SELECT BillRestockMaxThreshold, BillMaxAmount, CoinRestockMaxThreshold, CoinRestockMinThreshold FROM `MoneyHandler` 
        WHERE MoneyHandlerID = (
                SELECT MoneyHandlerID FROM Currency WHERE CurrencyID = %s LIMIT 1
            );
    """, tuple(str(currency_id)))
    moneyhandler_info = cursor.fetchall()
    #print(moneyhandler_info)

    # get MoneyHandler restock requests
    cursor.execute("""
        SELECT ReasonForRequest FROM `RestockRequest`
        WHERE MoneyHandlerID = (
                SELECT MoneyHandlerID FROM Currency WHERE CurrencyID = %s
            ) AND DateResolved IS NULL;
    """, tuple(str(currency_id)))
    money_requests = cursor.fetchall()

    # check if bill, if so add up all bills and test for being over thresh
    bills_over = False
    if max_amt == None:
        # add up 1 dollar bills
        cursor.execute("""
            SELECT CurrentAmount FROM `currency` WHERE CurrencyID = %s;
        """, tuple(str(5)))
        total = cursor.fetchall()[0].get("CurrentAmount")
        # add up 5 dollar bills
        cursor.execute("""
            SELECT CurrentAmount FROM `currency` WHERE CurrencyID = %s;
        """, tuple(str(6)))
        total += cursor.fetchall()[0].get("CurrentAmount")
        # check if total over billrestockmaxthreshold
        max = moneyhandler_info[0].get("BillMaxAmount") * moneyhandler_info[0].get("BillRestockMaxThreshold")
        if total >= max:
            bills_over = True

    # check if coin, if so see if over/under the thresh
    coin_over = False
    coin_under = False
    if max_amt != None:
        max = max_amt * moneyhandler_info[0].get("CoinRestockMaxThreshold")
        min = max_amt * moneyhandler_info[0].get("CoinRestockMinThreshold")
        # check for over
        if curr_amt >= max:
            coin_over = True
        if curr_amt <= min:
            coin_under = True
    
    # if bills_over, check to see if a bill restock request exists. if not, make one. if does, dont make one
    # relies on the SAME reason for request format being used in every single bill request: "Restock request in "MoneyHandler" : bills above restock threshold."
    if bills_over and (currency_id == 5 or currency_id == 6):
        exists = False
        for request in money_requests:
            if "Restock request in \"MoneyHandler\" : bills above restock threshold." in request.get("ReasonForRequest"):
                exists = True
                break
        # if not exists, make one
        if exists != True:
            cursor.execute("""
                INSERT INTO RestockRequest (ServiceWorkerID, MoneyHandlerID, DateRequested, DateResolved, ReasonForRequest)
                    VALUES (%s, (SELECT MoneyHandlerID FROM Currency WHERE CurrencyID = %s), %s, NULL, %s)
            """, tuple((str(worker_id), str(currency_id), str(datetime.now().date()), "Restock request in \"MoneyHandler\" : bills above restock threshold.")))
            conn.commit()

    # if coins over, check to see if, for this specific coin, a restock request exists. if not, make one. if does, dont make one
    # relies on the SAME reason for request format being used in every single coin request: "Restock request in "MoneyHandler" : "$value" coins below restock threshold." or "Restock request in "MoneyHandler" : "$value" coins above restock threshold." 
    # in this format, the value for the coins must have a leading 0 if under 1 dollar.
    if coin_over and (currency_id != 5 or currency_id != 6):
        exists = False
        for request in money_requests:
            if "Restock request in \"MoneyHandler\" : \"$" in request.get("ReasonForRequest") and "\" coins above restock threshold." in request.get("ReasonForRequest") and str(curr_worth) in request.get("ReasonForRequest"):
                exists = True
                break
        # if not exists, make one
        if exists != True:
            reason = "Restock request in \"MoneyHandler\" : \"$" + str(curr_worth) + "\" coins above restock threshold."
            cursor.execute("""
                INSERT INTO RestockRequest (ServiceWorkerID, MoneyHandlerID, DateRequested, DateResolved, ReasonForRequest)
                    VALUES (%s, (SELECT MoneyHandlerID FROM Currency WHERE CurrencyID = %s), %s, NULL, %s)
            """, tuple((str(worker_id), str(currency_id), str(datetime.now().date()), reason)))
            conn.commit()

    # do same check for coin under
    if coin_under and (currency_id != 5 or currency_id != 6):
        exists = False
        for request in money_requests:
            if "Restock request in \"MoneyHandler\" : \"$" in request.get("ReasonForRequest") and "\" coins below restock threshold." in request.get("ReasonForRequest") and str(curr_worth) in request.get("ReasonForRequest"):
                exists = True
                break
        # if not exists, make one
        if exists != True:
            reason = "Restock request in \"MoneyHandler\" : \"$" + str(curr_worth) + "\" coins below restock threshold."
            cursor.execute("""
                INSERT INTO RestockRequest (ServiceWorkerID, MoneyHandlerID, DateRequested, DateResolved, ReasonForRequest)
                VALUES (%s, (SELECT MoneyHandlerID FROM Currency WHERE CurrencyID = %s), %s, NULL, %s)
            """, tuple((str(worker_id), str(currency_id), str(datetime.now().date()), reason)))
            conn.commit()

    cursor.close()
    conn.close()
    return([coin_under, coin_over, bills_over])

# goes over all currencies and applies function check_and_create_currency_restock_request to them
# returns boolean 2d array with [[coin_under, coin_over, bills_over], [coin_under, coin_over, bills_over], etc]
def check_and_create_currency_restock_request_ALL(worker_id=None):
    # check for empty service worker table
    if worker_id != None and get_random_service_worker("Restocker") <= -1:
        return
    
    conn = get_connection()
    cursor = conn.cursor()

    # get all currency IDs
    cursor.execute("""
        SELECT CurrencyID FROM Currency;
    """)
    ids = cursor.fetchall()
    
    # loop thru check_and_create_currency_restock_request with ids
    rnd = False
    if worker_id == None:
        rnd = True
    results = []
    for id in ids:
        if rnd:
            worker_id = get_random_service_worker("Restocker")
        results.append(check_and_create_currency_restock_request(id[0], worker_id))

    cursor.close()
    conn.close()
    return results

# Retrieves all unresolved restock requests (where DateResolved is NULL)
# Returns a list of dictionaries with request details and assigned worker name
def get_open_restock_requests():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT rr.*, sw.Name AS WorkerName
        FROM RestockRequest rr
        LEFT JOIN ServiceWorker sw ON rr.ServiceWorkerID = sw.WorkerID
        WHERE rr.DateResolved IS NULL
    """)

    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


# Marks a restock request as resolved by setting its DateResolved to today
# Called after a restocker confirms they have restocked a slot
# Note: the GUI passes a slot_code; this resolves the oldest open request
# for that slot based on the reason text. If your schema links slots to
# requests directly, update this query to match your foreign key structure.
def resolve_restock_request(slot_code):
    conn = get_connection()
    cursor = conn.cursor()

    # Resolve the most recent open restock request that mentions this slot code
    cursor.execute("""
        UPDATE RestockRequest
        SET DateResolved = %s
        WHERE DateResolved IS NULL
          AND ReasonForRequest LIKE %s
        ORDER BY RestockRequestID DESC
        LIMIT 1
    """, (datetime.now().date(), f'%"{slot_code}"%'))

    conn.commit()
    cursor.close()
    conn.close()

# Marks a currency restock request as resolved by setting its DateResolved to today IF it no longer needs it (is in the correct ranges)
# called after a restocker restocks/empties any coins/bills
def resolve_restock_request_currency(currency_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # get currencies current amount
    cursor.execute("""
        SELECT CurrentAmount, MaxAmount, CurrencyWorth FROM `currency` WHERE CurrencyID = %s;
    """, tuple(str(currency_id)))
    vals = cursor.fetchall()
    curr_amt = vals[0].get("CurrentAmount")
    max_amt = vals[0].get("MaxAmount")
    curr_worth = vals[0].get("CurrencyWorth")

    # get moneyhandler info (bill max and all threshs)
    cursor.execute("""
        SELECT BillRestockMaxThreshold, BillMaxAmount, CoinRestockMaxThreshold, CoinRestockMinThreshold FROM `MoneyHandler` 
        WHERE MoneyHandlerID = (
                SELECT MoneyHandlerID FROM Currency WHERE CurrencyID = %s LIMIT 1
            );
    """, tuple(str(currency_id)))
    moneyhandler_info = cursor.fetchall()
    #print(moneyhandler_info)

    # get MoneyHandler restock requests
    cursor.execute("""
        SELECT ReasonForRequest, RestockRequestID FROM `RestockRequest`
        WHERE MoneyHandlerID = (
                SELECT MoneyHandlerID FROM Currency WHERE CurrencyID = %s
            ) AND DateResolved IS NULL;
    """, tuple(str(currency_id)))
    money_requests = cursor.fetchall()

    # check if bill, if so add up all bills and test for being over thresh
    bills_over = False
    if max_amt == None:
        # add up 1 dollar bills
        cursor.execute("""
            SELECT CurrentAmount FROM `currency` WHERE CurrencyID = %s;
        """, tuple(str(5)))
        total = cursor.fetchall()[0].get("CurrentAmount")
        # add up 5 dollar bills
        cursor.execute("""
            SELECT CurrentAmount FROM `currency` WHERE CurrencyID = %s;
        """, tuple(str(6)))
        total += cursor.fetchall()[0].get("CurrentAmount")
        # check if total over billrestockmaxthreshold
        max = moneyhandler_info[0].get("BillMaxAmount") * moneyhandler_info[0].get("BillRestockMaxThreshold")
        if total >= max:
            bills_over = True

    # check if coin, if so see if over/under the thresh
    coin_over = False
    coin_under = False
    if max_amt != None:
        max = max_amt * moneyhandler_info[0].get("CoinRestockMaxThreshold")
        min = max_amt * moneyhandler_info[0].get("CoinRestockMinThreshold")
        # check for over
        if curr_amt >= max:
            coin_over = True
        if curr_amt <= min:
            coin_under = True

    # check if bills aren't over and there is an open request. if so, close request
    if bills_over != True and (currency_id == 5 or currency_id == 6):
        target = None
        for request in money_requests:
            if "Restock request in \"MoneyHandler\" : bills above restock threshold." in request.get("ReasonForRequest"):
                target = request
                break
        if target != None:
            cursor.execute("""
                UPDATE RestockRequest
                    SET DateResolved = %s
                    WHERE DateResolved IS NULL AND RestockRequestID = %s
                    LIMIT 1;
                """, (datetime.now().date(), target.get("RestockRequestID")))
            conn.commit()

    # check if coins aren't over, if so close request if exists
    if coin_over != True and (currency_id != 5 or currency_id != 6):
        target = None
        for request in money_requests:
            if "Restock request in \"MoneyHandler\" : \"$" in request.get("ReasonForRequest") and "\" coins above restock threshold." in request.get("ReasonForRequest") and str(curr_worth) in request.get("ReasonForRequest"):
                target = request
                break
        if target != None:
            cursor.execute("""
                UPDATE RestockRequest
                    SET DateResolved = %s
                    WHERE DateResolved IS NULL AND RestockRequestID = %s
                    LIMIT 1;
                """, (datetime.now().date(), target.get("RestockRequestID")))
            conn.commit()

    # check if coins aren't under, if so close request if exists
    if coin_under != True and (currency_id != 5 or currency_id != 6):
        target = None
        for request in money_requests:
            if "Restock request in \"MoneyHandler\" : \"$" in request.get("ReasonForRequest") and "\" coins below restock threshold." in request.get("ReasonForRequest") and str(curr_worth) in request.get("ReasonForRequest"):
                target = request
                break
        if target != None:
            cursor.execute("""
                UPDATE RestockRequest
                    SET DateResolved = %s
                    WHERE DateResolved IS NULL AND RestockRequestID = %s
                    LIMIT 1;
                """, (datetime.now().date(), target.get("RestockRequestID")))
            conn.commit()

    cursor.close()
    conn.close()
    return [coin_over, coin_under, bills_over]

# goes through alll currencies and applies resolve_restock_request_currency() to them
def resolve_restock_request_currency_ALL():
    conn = get_connection()
    cursor = conn.cursor()

    # get all currency IDs
    cursor.execute("""
        SELECT CurrencyID FROM Currency;
    """)
    ids = cursor.fetchall()
    
    # loop thru check_and_create_currency_restock_request with ids
    results = []
    for id in ids:
        results.append(resolve_restock_request_currency(id[0]))

    cursor.close()
    conn.close()
    return results

# Marks a single restock request resolved by its primary key.
# Used by the "Resolved" button in the View Restocker Requests screen
# for manual dismissal when the auto-resolve path didn't trigger.
def resolve_restock_request_by_id(request_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE RestockRequest
        SET DateResolved = %s
        WHERE RestockRequestID = %s AND DateResolved IS NULL
    """, (datetime.now().date(), int(request_id)))
    conn.commit()
    cursor.close()
    conn.close()


# ═══════════════════════════════════════════════════════════════
# MAINTENANCE REQUEST FUNCTIONS
# Used by the Maintenance Request and Close Maintenance Ticket screens
# ═══════════════════════════════════════════════════════════════

# Creates a new maintenance request record in the database
# Returns the auto-generated MaintenanceRequestID for display in the UI
# Called when a technician or admin reports a malfunction or schedules service
def create_maintenance_request(machine_id, worker_id, reason, date_requested):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO MaintenanceRequest (MachineID, ServiceWorkerID, DateRequested, DateResolved, ReasonForRequest)
        VALUES (%s, %s, %s, NULL, %s)
    """, (machine_id, worker_id, date_requested, reason))

    conn.commit()
    request_id = cursor.lastrowid  # Get the auto-generated MaintenanceRequestID
    cursor.close()
    conn.close()
    return request_id


# Retrieves all unresolved maintenance requests for a specific machine
# Returns a list of dictionaries with request details and assigned technician name
# Used by the Close Maintenance Ticket screen to display open tickets
def get_open_maintenance_requests(machine_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT mr.*, sw.Name AS TechName
        FROM MaintenanceRequest mr
        LEFT JOIN ServiceWorker sw ON mr.ServiceWorkerID = sw.WorkerID
        WHERE mr.MachineID = %s
          AND mr.DateResolved IS NULL
        ORDER BY mr.DateRequested DESC
    """, (machine_id,))

    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


# Marks a maintenance request as resolved by setting its DateResolved timestamp
# The technician's service notes are appended to the ReasonForRequest field
# System side effect: the caller (GUI) also updates machine status to ONLINE
def close_maintenance_request(request_id, date_resolved, notes):
    conn = get_connection()
    cursor = conn.cursor()

    # Append the technician's service notes to the existing reason for a full record
    cursor.execute("""
        UPDATE MaintenanceRequest
        SET DateResolved    = %s,
            ReasonForRequest = CONCAT(ReasonForRequest, ' | Service notes: ', %s)
        WHERE MaintenanceRequestID = %s
    """, (date_resolved, notes, request_id))

    conn.commit()
    cursor.close()
    conn.close()


# ═══════════════════════════════════════════════════════════════
# CASH / MONEY HANDLER FUNCTIONS
# Used by the Update Cash Level screen
# System-triggered alerts are resolved here after the restocker acts
# ═══════════════════════════════════════════════════════════════

# Retrieves the MoneyHandler record for a given machine
# Returns a dictionary with bill/coin thresholds and amount values
# Used to display current cash status on the Update Cash Level screen
def get_money_handler(machine_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM MoneyHandler
        WHERE MachineID = %s
        LIMIT 1
    """, (machine_id,))

    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


# Applies a per-denomination cash adjustment from the Update Cash Level screen
# action: "refill" adds coin/bill counts; "collect" subtracts (clamped to 0)
# deltas: list of {"currency_id": int, "count": int, "worth": float}
# Logs a single RestockRequest summarizing what was applied (already resolved,
# since this records completed work, not a pending request).
def apply_cash_adjustments(machine_id, worker_id, action, deltas, date):
    if action not in ("refill", "collect"):
        raise ValueError(f"Unknown cash action: {action!r}")
    nonzero = [d for d in deltas if int(d.get("count", 0)) > 0]
    if not nonzero:
        return

    conn = get_connection()
    cursor = conn.cursor()

    parts = []
    for d in sorted(nonzero, key=lambda x: float(x["worth"])):
        worth = float(d["worth"])
        label = f"${worth:.2f}" if worth >= 1.0 else f"${worth:.2f}"
        parts.append(f"{int(d['count'])}× {label}")
    verb = "added" if action == "refill" else "collected"
    prefix = "Cash refill" if action == "refill" else "Cash collection"
    reason = f"{prefix}: {', '.join(parts)} {verb} by worker {worker_id}."

    cursor.execute("""
        INSERT INTO RestockRequest (ServiceWorkerID, MoneyHandlerID, DateRequested, DateResolved, ReasonForRequest)
        SELECT %s, mh.MoneyHandlerID, %s, %s, %s
        FROM MoneyHandler mh
        WHERE mh.MachineID = %s
        LIMIT 1
    """, (worker_id, date, datetime.now().date(), reason, machine_id))

    if action == "refill":
        for d in nonzero:
            # Coins have a MaxAmount cap; bills have NULL (no per-row cap).
            cursor.execute("""
                UPDATE Currency
                SET CurrentAmount = LEAST(
                    COALESCE(MaxAmount, CurrentAmount + %s),
                    CurrentAmount + %s
                )
                WHERE CurrencyID = %s
            """, (int(d["count"]), int(d["count"]), int(d["currency_id"])))
    else:
        for d in nonzero:
            cursor.execute("""
                UPDATE Currency
                SET CurrentAmount = GREATEST(0, CurrentAmount - %s)
                WHERE CurrencyID = %s
            """, (int(d["count"]), int(d["currency_id"])))

    conn.commit()
    cursor.close()
    conn.close()


# Resolves all open auto-generated bill-collection alerts for a machine.
# Called after the operator collects bills via Update Cash Level — the next
# sale will recreate the alert if bills are still above the threshold.
def resolve_cash_collection_alert(machine_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE RestockRequest rr
        JOIN MoneyHandler mh ON rr.MoneyHandlerID = mh.MoneyHandlerID
        SET rr.DateResolved = %s
        WHERE mh.MachineID = %s
          AND rr.DateResolved IS NULL
          AND rr.ReasonForRequest LIKE '%%bills above restock%%'
    """, (datetime.now().date(), machine_id))
    conn.commit()
    cursor.close()
    conn.close()


# Resolves all open auto-generated coin-refill alerts for a machine.
# Called after the operator refills coins via Update Cash Level.
def resolve_change_refill_alert(machine_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE RestockRequest rr
        JOIN MoneyHandler mh ON rr.MoneyHandlerID = mh.MoneyHandlerID
        SET rr.DateResolved = %s
        WHERE mh.MachineID = %s
          AND rr.DateResolved IS NULL
          AND rr.ReasonForRequest LIKE '%%coins below restock%%'
    """, (datetime.now().date(), machine_id))
    conn.commit()
    cursor.close()
    conn.close()


# Inspects current cash state vs MoneyHandler thresholds and inserts an
# auto restock request for any breach that doesn't already have an open one.
# Called from RecordSaleScreen after a successful sale.
def check_and_create_money_handler_requests(machine_id, worker_id=get_random_service_worker("Restocker")):
    # check for empty service worker table
    if worker_id <= -1:
        return
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT mh.MoneyHandlerID, mh.BillMaxAmount, mh.BillRestockMaxThreshold,
               mh.CoinRestockMinThreshold
        FROM MoneyHandler mh
        WHERE mh.MachineID = %s
        LIMIT 1
    """, (machine_id,))
    mh = cursor.fetchone()
    if not mh:
        cursor.close()
        conn.close()
        return

    money_handler_id = mh["MoneyHandlerID"]
    bill_max = float(mh["BillMaxAmount"] or 0)
    bill_pct = float(mh["BillRestockMaxThreshold"] or 0)
    coin_min_pct = float(mh["CoinRestockMinThreshold"] or 0)

    cursor.execute("""
        SELECT CurrencyID, CurrencyWorth, CurrentAmount, MaxAmount
        FROM Currency
        WHERE MoneyHandlerID = %s
    """, (money_handler_id,))
    rows = cursor.fetchall()

    today = datetime.now().date()

    def already_open(reason_like):
        cursor.execute("""
            SELECT 1 FROM RestockRequest
            WHERE MoneyHandlerID = %s AND DateResolved IS NULL
              AND ReasonForRequest LIKE %s
            LIMIT 1
        """, (money_handler_id, reason_like))
        return cursor.fetchone() is not None

    # Bills above max-threshold (combined dollar value across all bills)
    bill_total = sum(float(r["CurrencyWorth"]) * int(r["CurrentAmount"] or 0)
                     for r in rows if float(r["CurrencyWorth"]) >= 1.0)
    if bill_max > 0 and bill_pct > 0 and bill_total >= bill_max * (bill_pct / 100.0):
        reason = 'Auto restock request: bills above restock threshold.'
        if not already_open('%bills above restock%'):
            cursor.execute("""
                INSERT INTO RestockRequest
                  (ServiceWorkerID, MoneyHandlerID, DateRequested, DateResolved, ReasonForRequest)
                VALUES (%s, %s, %s, NULL, %s)
            """, (worker_id, money_handler_id, today, reason))

    # Coins below their per-row min-threshold (percentage of MaxAmount)
    for r in rows:
        worth = float(r["CurrencyWorth"])
        if worth >= 1.0:
            continue
        max_amt = r["MaxAmount"]
        cur = int(r["CurrentAmount"] or 0)
        if not max_amt or coin_min_pct <= 0:
            continue
        if cur <= int(max_amt) * (coin_min_pct / 100.0):
            denom_label = f"${worth:.2f}"
            reason = f'Auto restock request: "{denom_label}" coins below restock threshold.'
            if not already_open(f'%"{denom_label}" coins below restock%'):
                cursor.execute("""
                    INSERT INTO RestockRequest
                      (ServiceWorkerID, MoneyHandlerID, DateRequested, DateResolved, ReasonForRequest)
                    VALUES (%s, %s, %s, NULL, %s)
                """, (worker_id, money_handler_id, today, reason))

    conn.commit()
    cursor.close()
    conn.close()


# ═══════════════════════════════════════════════════════════════
# TRANSACTION HISTORY FUNCTIONS
# Used by the View Transactions screen
# ═══════════════════════════════════════════════════════════════

# Retrieves all transactions for the machine joined with product info
# Returns rows sorted newest-first and aggregate summary totals
def get_all_transactions(machine_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            t.SaleNumber,
            t.SaleDateTime,
            p.Name       AS ProductName,
            p.Price,
            t.Tax,
            t.CashGiven,
            t.CardFee,
            t.AccountCharged
        FROM `Transaction` t
        LEFT JOIN Product p ON t.ProductID = p.ProductID
        WHERE t.MachineID = %s
        ORDER BY t.SaleDateTime DESC
    """, (machine_id,))

    rows = cursor.fetchall()

    # Aggregate totals
    cursor.execute("""
        SELECT
            SUM(p.Price + t.Tax)                     AS total_revenue,
            SUM(t.Tax)                               AS total_tax,
            SUM(CASE WHEN t.CashGiven IS NOT NULL
                     THEN t.CashGiven ELSE 0 END)    AS total_cash
        FROM `Transaction` t
        LEFT JOIN Product p ON t.ProductID = p.ProductID
        WHERE t.MachineID = %s
    """, (machine_id,))

    totals = cursor.fetchone()
    cursor.close()
    conn.close()
    return rows, totals


# Returns slot codes that have an open restock request assigned to a specific worker
def get_slot_codes_with_open_restock_for_worker(worker_id=get_random_service_worker("Restocker")):
    # check for empty service worker table
    if worker_id <= -1:
        return
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT ReasonForRequest
        FROM RestockRequest
        WHERE ServiceWorkerID = %s
          AND DateResolved IS NULL
          AND MoneyHandlerID IS NULL
    """, (worker_id,))

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Extract slot codes from the reason text (format: '...Slot "XY"...')
    import re
    codes = set()
    for (reason,) in rows:
        match = re.search(r'Slot "([^"]+)"', reason or "")
        if match:
            codes.add(match.group(1))
    return codes


# ═══════════════════════════════════════════════════════════════
# SERVICE WORKER FUNCTIONS
# Used by the Update Inventory screen worker bar
# ═══════════════════════════════════════════════════════════════

# Retrieves all service workers assigned to the machine
# Returns a list of dictionaries with worker ID, name, and contact info
def get_service_workers(machine_id=1):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM ServiceWorker WHERE MachineID = %s", (machine_id,))
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    return results

# Adds a new service worker to the database for this machine
def add_service_worker(machine_id, name, worker_type, phone, email, company):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ServiceWorker (MachineID, Name, WorkerType, PhoneNumber, Email, Company)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (machine_id, name, worker_type, phone or None, email or None, company or None))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id


# Updates an existing service worker's details
def update_service_worker(worker_id, name, worker_type, phone, email, company):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE ServiceWorker
        SET Name = %s, WorkerType = %s, PhoneNumber = %s, Email = %s, Company = %s
        WHERE WorkerID = %s
    """, (name, worker_type, phone or None, email or None, company or None, worker_id))
    conn.commit()
    cursor.close()
    conn.close()


# Removes a service worker and all their linked records, handling the full FK chain.
def delete_service_worker(worker_id):
    conn = get_connection()
    cursor = conn.cursor()
    # Find all RestockRequest IDs belonging to this worker
    cursor.execute("SELECT RestockRequestID FROM RestockRequest WHERE ServiceWorkerID = %s", (worker_id,))
    rr_ids = [row[0] for row in cursor.fetchall()]
    if rr_ids:
        fmt = ','.join(['%s'] * len(rr_ids))
        # MachineSlot and PerishableItem reference RestockRequest — NULL those FKs first
        cursor.execute(f"UPDATE MachineSlot SET RestockRequestID = NULL WHERE RestockRequestID IN ({fmt})", rr_ids)
        #cursor.execute(f"UPDATE PerishableItem SET RestockRequestID = NULL WHERE RestockRequestID IN ({fmt})", rr_ids)
    cursor.execute("DELETE FROM MaintenanceRequest WHERE ServiceWorkerID = %s", (worker_id,))
    cursor.execute("DELETE FROM RestockRequest WHERE ServiceWorkerID = %s", (worker_id,))
    cursor.execute("DELETE FROM ServiceWorker WHERE WorkerID = %s", (worker_id,))
    conn.commit()
    cursor.close()
    conn.close()


def has_open_auto_maintenance(machine_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM MaintenanceRequest
        WHERE MachineID = %s AND DateResolved IS NULL
          AND ReasonForRequest = 'Auto-Scheduled Servicing'
    """, (machine_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0


def get_currency_breakdown(machine_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    # GROUP BY CurrencyWorth so multiple rows with the same denomination show as one line
    cursor.execute("""
        SELECT c.CurrencyWorth, SUM(c.CurrentAmount) AS CurrentAmount
        FROM Currency c
        JOIN MoneyHandler mh ON c.MoneyHandlerID = mh.MoneyHandlerID
        WHERE mh.MachineID = %s
        GROUP BY c.CurrencyWorth
        ORDER BY c.CurrencyWorth DESC
    """, (machine_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

# Returns one row per Currency with everything the cash UI needs
# (id, denomination value, current count, max-per-row cap or None for bills).
def get_currency_details(machine_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.CurrencyID, c.CurrencyWorth, c.CurrentAmount, c.MaxAmount
        FROM Currency c
        JOIN MoneyHandler mh ON c.MoneyHandlerID = mh.MoneyHandlerID
        WHERE mh.MachineID = %s
        ORDER BY c.CurrencyWorth DESC
    """, (machine_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


# added to get currency max amounts
def get_total_currency_amounts(machine_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.CurrencyID, c.MaxAmount
        FROM Currency c
        JOIN MoneyHandler mh ON c.MoneyHandlerID = mh.MoneyHandlerID
        WHERE mh.MachineID = %s
        GROUP BY c.CurrencyID
        ORDER BY c.CurrencyID DESC
    """, (machine_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def get_total_cash_in_machine(machine_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT SUM(c.CurrencyWorth * c.CurrentAmount) AS current_cash
        FROM Currency c
        JOIN MoneyHandler mh ON c.MoneyHandlerID = mh.MoneyHandlerID
        WHERE mh.MachineID = %s
    """, (machine_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return float(row["current_cash"] or 0) if row else 0.0


def get_all_service_workers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ServiceWorker ORDER BY WorkerID")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def add_product_to_slot(slot_code, name, price, description, max_qty, threshold):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    # Product requires MachineID (NOT NULL FK) — pull it from the single Machine row
    cursor.execute("""
        INSERT INTO Product (MachineID, Name, Price, Description)
        SELECT MachineID, %s, %s, %s FROM Machine LIMIT 1
    """, (name, float(price), description or None))
    product_id = cursor.lastrowid
    # Slot may already exist as an empty row — update it rather than inserting a duplicate
    cursor.execute("SELECT SlotCode FROM MachineSlot WHERE SlotCode = %s", (slot_code,))
    if cursor.fetchone():
        cursor.execute("""
            UPDATE MachineSlot
            SET ProductID = %s, MaxAmount = %s, ProductCount = 0, RestockAtThreshold = %s
            WHERE SlotCode = %s
        """, (product_id, int(max_qty), float(threshold), slot_code))
    else:
        cursor.execute("""
            INSERT INTO MachineSlot (SlotCode, ProductID, MaxAmount, ProductCount, RestockAtThreshold)
            VALUES (%s, %s, %s, 0, %s)
        """, (slot_code, product_id, int(max_qty), float(threshold)))
    conn.commit()
    cursor.close()
    conn.close()


# ═══════════════════════════════════════════════════════════════
# CONNECTION TEST
# Run this file directly to verify the database is reachable
# ═══════════════════════════════════════════════════════════════

# Quick test to verify database connection and core queries work
if __name__ == "__main__":
    print("Testing database connection...")
    try:
        info = get_machine_info()
        print(f"Machine: {info['ModelNumber']} at {info['Address']}")
        print(f"State: {info['CurrentState']}")

        slots = get_all_products_with_slots()
        print(f"\nLoaded {len(slots)} machine slots:")
        for s in slots:
            print(f"  [{s['code']}] {s['name']} - ${s['price']:.2f} ({s['count']}/{s['max']})")

        money = get_money_handler(info["MachineID"])
        print(f"\nMoney Handler: {money}")

        tickets = get_open_maintenance_requests(info["MachineID"])
        print(f"\nOpen Maintenance Tickets: {len(tickets)}")

        print("\nDatabase connection successful!")
    except Exception as e:
        print(f"Connection failed: {e}")
