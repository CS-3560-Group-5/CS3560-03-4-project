# db_connection.py
# 4/23/2026
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


# Retrieves all machine slots with their associated product info
# Returns a list of dictionaries, each representing a slot in the machine
# Empty slots (no product assigned) are included with None values
# Used by the Record Sale and Update Inventory screens
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
            "code": row["code"],
            "name": row["name"] if row["name"] else "Empty",
            "price": float(row["price"]) if row["price"] else 0.0,
            "count": row["count"] if row["count"] is not None else 0,
            "max": row["max"] if row["max"] is not None else 0,
            "product_id": row["product_id"],
            "description": row["description"] if row["description"] else "",
            "threshold": float(row["threshold"]) if row["threshold"] is not None else 0.0
        })
    
    return slots


# Retrieves the main machine's information from the database
# Returns a dictionary with machine details like address, model, and state
def get_machine_info():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM Machine LIMIT 1")
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return result


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
# Returns the new count after restocking
def restock_slot(slot_code, add_quantity):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # First get current count and max to validate
    cursor.execute("SELECT ProductCount, MaxAmount FROM MachineSlot WHERE SlotCode = %s", (slot_code,))
    row = cursor.fetchone()
    
    if row is None:
        cursor.close()
        conn.close()
        return None
    
    current = row["ProductCount"] if row["ProductCount"] is not None else 0
    max_amt = row["MaxAmount"] if row["MaxAmount"] is not None else 0
    new_count = current + add_quantity
    
    # Don't exceed the slot's maximum capacity
    if new_count > max_amt:
        cursor.close()
        conn.close()
        return -1  # Signal that it exceeds max
    
    # Apply the restock update
    cursor.execute("UPDATE MachineSlot SET ProductCount = %s WHERE SlotCode = %s", (new_count, slot_code))
    conn.commit()
    cursor.close()
    conn.close()
    return new_count


# Checks if a slot's product count has fallen below its restock threshold
# If so, creates a new restock request in the database
# Called after each sale to monitor inventory levels
def check_and_create_restock_request(slot_code, worker_id=1):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get the slot's current count, max, and threshold
    cursor.execute("""
        SELECT ProductCount, MaxAmount, RestockAtThreshold 
        FROM MachineSlot 
        WHERE SlotCode = %s
    """, (slot_code,))
    row = cursor.fetchone()
    
    if row and row["ProductCount"] is not None and row["MaxAmount"] is not None:
        count = row["ProductCount"]
        max_amt = row["MaxAmount"]
        threshold = row["RestockAtThreshold"] if row["RestockAtThreshold"] else 0.2
        
        # Check if current fill percentage is at or below the threshold
        if max_amt > 0 and (count / max_amt) <= threshold:
            # Create a restock request for this slot
            cursor.execute("""
                INSERT INTO RestockRequest (ServiceWorkerID, MoneyHandlerID, DateRequested, DateResolved, ReasonForRequest)
                VALUES (%s, NULL, %s, NULL, %s)
            """, (worker_id, datetime.now().date(), 
                  f'Restock request: Slot "{slot_code}" below restock threshold.'))
            conn.commit()
    
    cursor.close()
    conn.close()


# Retrieves all unresolved restock requests (where DateResolved is NULL)
# Used to display pending restock tasks
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
# Called after a restocker confirms they have restocked the slot
def resolve_restock_request(request_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE RestockRequest 
        SET DateResolved = %s 
        WHERE RestockRequestID = %s
    """, (datetime.now().date(), request_id))
    
    conn.commit()
    cursor.close()
    conn.close()


# Retrieves all unresolved maintenance requests
# Returns a list of dictionaries with request details and assigned technician
def get_open_maintenance_requests():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT mr.*, sw.Name AS TechName
        FROM MaintenanceRequest mr
        LEFT JOIN ServiceWorker sw ON mr.ServiceWorkerID = sw.WorkerID
        WHERE mr.DateResolved IS NULL
    """)
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


# Retrieves all service workers assigned to the machine
# Returns a list of dictionaries with worker details
def get_service_workers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM ServiceWorker WHERE MachineID = 1")
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return results


# Quick test to verify database connection works
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
        
        print("\nDatabase connection successful!")
    except Exception as e:
        print(f"Connection failed: {e}")
