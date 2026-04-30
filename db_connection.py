# db_connection.py
# 4/23/2026 — Updated 4/27/2026
# Database connection module for the Vending Machine System
# Provides functions to read from and write to the MySQL database
# This module bridges the GUI with the backend MySQL database

import mysql.connector
from datetime import datetime

# Establishes and returns a connection to the vendingmachine database
# Uses the 'interface' user as specified in the project README
def get_connection():
    # Creates and returns a new MySQL database connection
    return mysql.connector.connect(
        host="localhost",
        user="interface",
        password="password",
        database="vendingmachine"
    )


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
def update_machine_info(machine_id, address, model_number, max_slots, days_between_services, current_state):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Machine
        SET Address             = %s,
            ModelNumber         = %s,
            MaxProductSlots     = %s,
            DaysBetweenServices = %s,
            CurrentState        = %s
        WHERE MachineID = %s
    """, (address, model_number, max_slots, days_between_services, current_state, machine_id))

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


# Records a cash transaction in the database
# Inserts a new row into the Transaction table with cash-specific fields
# Card fields (CardFee, AccountCharged) are set to NULL for cash transactions
def record_cash_sale(product_id, machine_id, tax, cash_given):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO `Transaction` (ProductID, MachineID, Tax, SaleDateTime, CardFee, AccountCharged, CashGiven)
        VALUES (%s, %s, %s, %s, NULL, NULL, %s)
    """, (product_id, machine_id, tax, datetime.now(), cash_given))

    conn.commit()
    sale_number = cursor.lastrowid
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
def check_and_create_restock_request(slot_code, worker_id=1):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get the slot's current count, max, and restock threshold percentage
    cursor.execute("""
        SELECT ProductCount, MaxAmount, RestockAtThreshold 
        FROM MachineSlot 
        WHERE SlotCode = %s
    """, (slot_code,))
    row = cursor.fetchone()

    if row and row["ProductCount"] is not None and row["MaxAmount"] is not None:
        count     = row["ProductCount"]
        max_amt   = row["MaxAmount"]
        threshold = row["RestockAtThreshold"] if row["RestockAtThreshold"] else 0.2

        # Create a restock request only if fill level is at or below the threshold
        if max_amt > 0 and (count / max_amt) <= threshold:
            cursor.execute("""
                INSERT INTO RestockRequest (ServiceWorkerID, MoneyHandlerID, DateRequested, DateResolved, ReasonForRequest)
                VALUES (%s, NULL, %s, NULL, %s)
            """, (worker_id, datetime.now().date(),
                  f'Auto restock request: Slot "{slot_code}" is at or below restock threshold.'))
            conn.commit()

    cursor.close()
    conn.close()


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


# Logs a cash (bill) collection event in the database
# Resets the bill amount in the MoneyHandler to zero after collection
# The restocker empties the bill storage, so BillMaxAmount reflects the cleared state
def record_cash_collection(machine_id, worker_id, amount_collected, date):
    conn = get_connection()
    cursor = conn.cursor()

    # Insert a restock request to log the cash collection event with the worker and date
    cursor.execute("""
        INSERT INTO RestockRequest (ServiceWorkerID, MoneyHandlerID, DateRequested, DateResolved, ReasonForRequest)
        SELECT %s, mh.MoneyHandlerID, %s, %s, %s
        FROM MoneyHandler mh
        WHERE mh.MachineID = %s
        LIMIT 1
    """, (worker_id, date, date,
          f"Cash collection: ${amount_collected:.2f} collected by worker {worker_id}.",
          machine_id))

    conn.commit()
    cursor.close()
    conn.close()


# Logs a coin (change) refill event in the database
# Updates the MoneyHandler to reflect the added coins
# Called when a restocker adds change to bring coins above the minimum threshold
def record_change_refill(machine_id, worker_id, amount_added, date):
    conn = get_connection()
    cursor = conn.cursor()

    # Insert a restock request to log the change refill event
    cursor.execute("""
        INSERT INTO RestockRequest (ServiceWorkerID, MoneyHandlerID, DateRequested, DateResolved, ReasonForRequest)
        SELECT %s, mh.MoneyHandlerID, %s, %s, %s
        FROM MoneyHandler mh
        WHERE mh.MachineID = %s
        LIMIT 1
    """, (worker_id, date, date,
          f"Change refill: ${amount_added:.2f} in coins added by worker {worker_id}.",
          machine_id))

    conn.commit()
    cursor.close()
    conn.close()


# Resolves the most recent open cash collection alert for a machine
# Called automatically after a restocker logs a successful cash collection
# Marks the associated restock request as resolved with today's date
def resolve_cash_collection_alert(machine_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Find and resolve the most recent open cash-related restock request for this machine
    cursor.execute("""
        UPDATE RestockRequest rr
        JOIN MoneyHandler mh ON rr.MoneyHandlerID = mh.MoneyHandlerID
        SET rr.DateResolved = %s
        WHERE mh.MachineID = %s
          AND rr.DateResolved IS NULL
          AND rr.ReasonForRequest LIKE '%Cash collection%'
        ORDER BY rr.RestockRequestID DESC
        LIMIT 1
    """, (datetime.now().date(), machine_id))

    conn.commit()
    cursor.close()
    conn.close()


# Resolves the most recent open change refill alert for a machine
# Called automatically after a restocker logs a successful coin refill
# Marks the associated restock request as resolved with today's date
def resolve_change_refill_alert(machine_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Find and resolve the most recent open change-related restock request for this machine
    cursor.execute("""
        UPDATE RestockRequest rr
        JOIN MoneyHandler mh ON rr.MoneyHandlerID = mh.MoneyHandlerID
        SET rr.DateResolved = %s
        WHERE mh.MachineID = %s
          AND rr.DateResolved IS NULL
          AND rr.ReasonForRequest LIKE '%Change refill%'
        ORDER BY rr.RestockRequestID DESC
        LIMIT 1
    """, (datetime.now().date(), machine_id))

    conn.commit()
    cursor.close()
    conn.close()


# ═══════════════════════════════════════════════════════════════
# SERVICE WORKER FUNCTIONS
# Used by the Update Inventory screen worker bar
# ═══════════════════════════════════════════════════════════════

# Retrieves all service workers assigned to the machine
# Returns a list of dictionaries with worker ID, name, and contact info
def get_service_workers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM ServiceWorker WHERE MachineID = 1")
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    return results


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
