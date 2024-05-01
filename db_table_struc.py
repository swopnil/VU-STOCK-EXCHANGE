import json
import mysql.connector

# Configure MySQL connection
db = mysql.connector.connect(
    host="stock100-swopnil100-1453.h.aivencloud.com",
    port=11907,
    user="avnadmin",
    passwd="AVNS_5RG3ixLOO6L1IRdRAC9",
    database="Stock"
)

def update_db():
    cursor = db.cursor()
    alter_table_query = """
    ALTER TABLE UserData
    ADD COLUMN Cash FLOAT DEFAULT 0;
    """
    cursor.execute(alter_table_query)
    db.commit()
    cursor.close()
    db.close()
def create_db():
    cursor = db.cursor()

    # SQL statement to create the UserData table
    create_table_query = """
    CREATE TABLE UserData (
        Username VARCHAR(255) PRIMARY KEY,
        Money DECIMAL(10, 2),
        Stocks JSON
    )
    """

    # Execute the SQL statement
    cursor.execute(create_table_query)

    # Commit the transaction
    db.commit()

    # Close the cursor and database connection
    cursor.close()
    db.close()

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
        cursor = db.cursor(dictionary=True)
        # Query to fetch user data, their current money, and merged stocks
        query = """
        SELECT ID.Username, ID.Money, new_table.Symbol, SUM(new_table.Volume) AS TotalVolume
        FROM ID 
        LEFT JOIN new_table ON ID.Username = new_table.Username 
        GROUP BY ID.Username, ID.Money, new_table.Symbol
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        user_data = {}

        for row in rows:
            username = row['Username']
            money = row['Money']
            symbol = row['Symbol']
            total_volume = row['TotalVolume']
            quant = float(total_volume) if total_volume is not None else 0
            if username not in user_data:
                user_data[username] = {'Username': username, 'Money': money, 'Stocks': {}}
            if symbol is not None:
                if symbol not in user_data[username]['Stocks']:
                    user_data[username]['Stocks'][symbol] = quant
                    
                else:
                    user_data[username]['Stocks'][symbol] += quant
        # Print the processed data
        print("New Table Data:")
        for username, data in user_data.items():
            print(f"Username: {username}, Money: {data['Money']}, Stocks: {data['Stocks']}")
       
        for username, data in user_data.items():
            money = data['Money']
            stocks_json = json.dumps(data['Stocks'])
            
            insert_query = "INSERT INTO UserData (Username, Money, Stocks) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE Money = VALUES(Money), Stocks = VALUES(Stocks)"
            cursor.execute(insert_query, (username, money, stocks_json))

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

def update_cash_column():
    update_db()
    try:
        cursor = db.cursor(dictionary=True)
        # Fetch user data including money and stocks
        query = """
            SELECT Username, Money, Stocks
            FROM UserData
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            username = row['Username']
            money = row['Money']
            stocks = json.loads(row['Stocks'])

            # Calculate cash for each user
            stocks_value = sum(price * quantity for price, quantity in stocks.items())
            cash =round((money - stocks_value), 2)

            # Update UserData table with cash value
            update_query = """
                UPDATE UserData
                SET Cash = %s
                WHERE Username = %s
            """
            cursor.execute(update_query, (cash, username))

        db.commit()
        cursor.close()
        print("Cash column updated successfully!")

    except Exception as e:
        db.rollback()
        print("Error updating cash column:", e)

def print_user_data():
    try:
        cursor = db.cursor(dictionary=True)
        query = """
            SELECT Username, Money, Stocks, Cash
            FROM UserData
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        if not rows:
            print("No data found in the UserData table.")
        else:
            print("Data from the UserData table:")
            for row in rows:
                username = row['Username']
                money = row['Money']
                stocks = json.loads(row['Stocks'])
                cash = row['Cash']

                print(f"\nUsername: {username}")
                print(f"Money: {money}")
                print("Stocks:")
                for stock, quantity in stocks.items():
                    print(f"  {stock}: {quantity}")
                print(f"Cash: {cash}")

        cursor.close()

    except Exception as e:
        print("Error fetching user data:", e)

if __name__ == "__main__":
    # print_new_table_structure()
    # update_cash_column()
    print_table_structure()
    # print_user_data()

