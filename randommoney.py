import mysql.connector
import random
import string

def generate_secret_token(length=16):
    """Generate a random secret token."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def add_user(username, balance):
    """Add a new user to the Bank table."""
    db = mysql.connector.connect(
        host="stock100-swopnil100-1453.h.aivencloud.com",
        port=11907,
        user="avnadmin",
        passwd="AVNS_5RG3ixLOO6L1IRdRAC9",
        database="Stock"
    )
    
    cursor = db.cursor()

    # Generate a random secret token
    secret_token = generate_secret_token()

    # Insert the new user into the database
    insert_query = "INSERT INTO Bank (username, balance, secret_token) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (username, balance, secret_token))

    # Commit the transaction
    db.commit()

    cursor.close()
    db.close()

# Add a new user with username 'user' and balance 100000
add_user('user', 100000)
