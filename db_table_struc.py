import mysql.connector

# Configure MySQL connection
db = mysql.connector.connect(
    host="stock100-swopnil100-1453.h.aivencloud.com",
    port=11907,
    user="avnadmin",
    passwd="AVNS_5RG3ixLOO6L1IRdRAC9",
    database="Stock"
)

# Function to print out all tables and their headings
def print_table_structure():
    cursor = db.cursor()

    # Get list of tables
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    # Iterate through each table
    for table in tables:
        table_name = table[0]
        print(f"Table: {table_name}")

        # Get table structure
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()

        # Print column names
        for column in columns:
            print(f"- {column[0]} ({column[1]})")

        print()  # Add empty line between tables

    cursor.close()
    

def print_new_table_structure():
    try:
        cursor = db.cursor()

        # Query to fetch the structure of the new table
        query = """
            SELECT ID.Username, ID.Money, new_table.Symbol, SUM(new_table.Volume) AS TotalVolume
            FROM ID 
            LEFT JOIN new_table ON ID.Username = new_table.Username 
            GROUP BY ID.Username, ID.Money, new_table.Symbol
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        merged_stocks = {}
        # Process the data and merge stocks with the same symbol
        for row in rows:
            username = row[0]
            money = row[1]
            symbol = row[2]
            volume = row[3]
            if username not in merged_stocks:
                merged_stocks[username] = {'Money': money, 'Stocks': {}}
            if symbol not in merged_stocks[username]['Stocks']:
                merged_stocks[username]['Stocks'][symbol] = volume
            else:
                merged_stocks[username]['Stocks'][symbol] += volume
        # Print the processed data
        print("New Table Data:")
        for username, data in merged_stocks.items():
            print(f"Username: {username}, Money: {data['Money']}, Stocks: {data['Stocks']}")

        cursor.close()
    except Exception as e:
        print("Error fetching new table structure:", e)

# Function to print out all data from the new_table
def print_new_table_data():
    cursor = db.cursor()

    # Execute query to select all data from new_table
    cursor.execute("SELECT * FROM new_table")

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Print column names
    column_names = [i[0] for i in cursor.description]
    print(", ".join(column_names))

    # Print data rows
    for row in rows:
        print(", ".join(str(col) for col in row))

    cursor.close()

def print_bank_data():
    try:

        # Create a cursor object to execute SQL queries
        cursor = db.cursor()

        # Execute a SELECT query to fetch data from the bankdata table
        cursor.execute("SELECT * FROM bankdata")

        # Fetch all rows of the result set
        bank_data = cursor.fetchall()

        # Print the fetched data
        for row in bank_data:
            print("ID:", row[0])
            print("Card Number:", row[1])
            print("Expiry Date:", row[2])
            print("CVV:", row[3])
            print("Card Holder Name:", row[4])
            print("Balance:", row[5])
            print("Bank Name:", row[6])
            print("Account Number:", row[7])
            print("Routing Number:", row[8])
            print()  # Add an empty line for readability

    except mysql.connector.Error as err:
        print("Error:", err)
    cursor.close()

def print_NTT():
    try:
        # Create a cursor object to execute SQL queries
        cursor = db.cursor()

        # Execute a SELECT query to fetch data from the NTT table, ordered by timestamp
        cursor.execute("SELECT * FROM NTT ORDER BY Time")

        # Fetch all rows of the result set
        ID_data = cursor.fetchall()

        # Print the fetched data
        for row in ID_data:
            if row[1] == "AMD":
                print("ID:", row[0])
                print("Name:", row[1])
                print("Price:", row[2])
                print("Volume:", row[3])
                print("Time:", row[4])
                print()  # Add an empty line for readability

    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()

if __name__ == "__main__":
    # print_new_table_structure()
    print_table_structure()
    print_bank_data()
    print_NTT()