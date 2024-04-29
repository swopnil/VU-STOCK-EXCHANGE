import random
import datetime
import mysql.connector

# Define the database connection
db = mysql.connector.connect(
    host="stock100-swopnil100-1453.h.aivencloud.com",
    port=11907,
    user="avnadmin",
    passwd="AVNS_5RG3ixLOO6L1IRdRAC9",
    database="Stock",
)

# Define the list of stock names
stock_names = ['AMD']

# Insert random data for all 12 months
for month in range(1, 13):
    for day in range(1, 32):
        try:
            # Get the current date and time
            date = datetime.datetime(2023, month, day).strftime('%Y-%m-%d %H:%M:%S')
            
            # Generate a random stock name
            stock_name = 'AMD'
            
            # Generate a random price between 100 and 200
            price = round(random.uniform(100, 200), 2)
            
            # Generate a random volume between 1000 and 10000
            volume = random.randint(1000, 10000)
            
            # Insert the data into the NTT table
            cursor = db.cursor()
            cursor.execute("INSERT INTO NTT (Name, Price, Volume, Time) VALUES (%s, %s, %s, %s)",
                           (stock_name, price, volume, date))
            db.commit()
        except ValueError:
            # Ignore dates that don't exist (e.g. February 30)
            pass

# Close the database connection
db.close()