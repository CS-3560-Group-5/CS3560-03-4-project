import db_connection

# Restock request in "MachineSlot" : Slot "2B" Product "Cheetos" below restock threshold.
# Restock request in "MachineSlot" : Slot "1B" is at or below restock threshold.
db_connection.check_and_create_restock_request_ALL()
db_connection.resolve_slot_restock_request_ALL()
