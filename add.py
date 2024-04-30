import mysql.connector

# Define the database connection
db = mysql.connector.connect(
    host="stock100-swopnil100-1453.h.aivencloud.com",
    port=11907,
    user="avnadmin",
    passwd="AVNS_5RG3ixLOO6L1IRdRAC9",
    database="Stock",
)

# Create a cursor object
cursor = db.cursor()

# Define the SQL query
sql_query = "SELECT * FROM `transaction`"

# Execute the SQL query
cursor.execute(sql_query)

# Fetch all the rows from the result set
rows = cursor.fetchall()

# Display the column names
column_names = [desc[0] for desc in cursor.description]
print("\t".join(column_names))

# Display the contents of the table
for row in rows:
    print("\t".join(map(str, row)))

# Close the cursor and database connection
cursor.close()
db.close()
