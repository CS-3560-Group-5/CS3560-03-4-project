import mysql.connector

machDB = mysql.connector.connect(
    host="localhost",
    user="interface",
    password="password",
    database = "vendingmachine"
)

cursor = machDB.cursor()

cursor.execute("SELECT * FROM product")

result = cursor.fetchall()

print(result)