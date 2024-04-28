from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime, timedelta
import mysql.connector
import threading
import time
import json
from talisman import Talisman



from stock import App
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime, timedelta
import mysql.connector
import threading
import time
import json
import hashlib

app = Flask(__name__)

# Function to hash the password using SHA-256
def hash_password(password):

    return hashlib.sha256(password.encode()).hexdigest()

# Add a new route to handle user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not is_username_available(username):
            flash('Username is already taken', 'error')
        else:
            hashed_password = hash_password(password)
            add_user_to_database(username, password)
            flash('Registration successful. You can now login.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

# Function to check if a username is available
def is_username_available(username):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ver WHERE Username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    return result is None

# Function to add a new user to the database
def add_user_to_database(username, password):
    cursor = db.cursor()
    cursor.execute("INSERT INTO ver (Username, Password) VALUES (%s, %s)", (username, password))
    db.commit()
    cursor.execute("INSERT INTO ID (Username, Money) VALUES (%s, %s)", (username, 10000))
    db.commit()
    
    cursor.close()

# Configure MySQL connection
db = mysql.connector.connect(
host="stock100-swopnil100-1453.h.aivencloud.com",
port=11907,
user="avnadmin",
passwd="AVNS_5RG3ixLOO6L1IRdRAC9",
database="Stock",
)

# Function to hash the password using SHA-256

csp = {
    'default-src': ["'self'", 'https://code.highcharts.com'],
    'style-src': ["'self'", "'unsafe-inline'", 'https://code.highcharts.com']
}
talisman = Talisman(app, content_security_policy=csp)
app.secret_key = 'your_secret_key'
stocks = {
    'AAPL': {'company_name': 'Apple Inc.', 'price': 135.00, 'volume': 1000},
    'GOOGL': {'company_name': 'Alphabet Inc.', 'price': 2350.00, 'volume': 500},
    'MSFT': {'company_name': 'Microsoft Corporation', 'price': 250.00, 'volume': 800},
}
# Configure MySQL connection
db = mysql.connector.connect(
host="stock100-swopnil100-1453.h.aivencloud.com",
port=11907,
user="avnadmin",
passwd="AVNS_5RG3ixLOO6L1IRdRAC9",
database="Stock",
)

# Sample user data (for demonstration)
users = {'admin': 'admin', 'user': 'user'}

# Function to update stock data every second
import time
from datetime import datetime
import time
from datetime import datetime
@app.route('/money')
def get_money():
    if 'username' in session:
        username = session['username']
        # Connect to the database and fetch the user's money
        db = mysql.connector.connect(
        host="stock100-swopnil100-1453.h.aivencloud.com",
        port=11907,
        user="avnadmin",
        passwd="AVNS_5RG3ixLOO6L1IRdRAC9",
        database="Stock",
        )
        cursor = db.cursor()
        query = "SELECT money FROM ID WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()
        db.close()
        if result:
            money = result[0]
            return jsonify({'money': money})
    return jsonify({'money': None})
def update_stock_data(stocks):
    while True:
        current_time = datetime.now()
        for symbol, data in stocks.items():
            # Connect to the database
            db = mysql.connector.connect(
            host="stock100-swopnil100-1453.h.aivencloud.com",
            port=11907,
            user="avnadmin",
            passwd="AVNS_5RG3ixLOO6L1IRdRAC9",
            database="Stock",
            )
        
            # Create a cursor
            cursor = db.cursor()
            
            # Insert the current price into the database
            query = "INSERT INTO NTT (Name, Price, Volume, Time) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (symbol, data['price'], data['volume'], current_time))
            
            # Commit the transaction and close the cursor and database connection
            db.commit()
            cursor.close()
            db.close()
        
        # Wait for 1 second before updating again
        time.sleep(60)

# Start the thread to update stock data
update_thread = threading.Thread(target=update_stock_data, args=(stocks,))
update_thread.daemon = True  # Set as daemon thread to stop when main thread stops
update_thread.start()


# Define the initial stocks



# Your Flask routes and other code go here...

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'admin':  # Check if username and password are both 'admin'
            session['username'] = username
            flash('You were successfully logged in as admin', 'success')
            return redirect(url_for('admin'))  # Redirect to admin page
            
        cursor = db.cursor()
        cursor.execute("SELECT * FROM ver WHERE Username = %s AND Password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            session['username'] = username
            flash('You were successfully logged in', 'success')
            return redirect(url_for('user'))  # Redirect to user.html after successful login
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/user')
def user():
    if 'username' in session:  
        username = session['username']
        available_money = fetch_available_money(username)
        if available_money is not None:
            return render_template('user.html', username=username, stocks=stocks, available_money=available_money)
        else:
            flash('Error fetching available money', 'error')
            return render_template('user.html', username=username, stocks=stocks)
    else:
        flash('Please log in as a user', 'error')
        return redirect(url_for('login'))

def fetch_available_money(username):
    try:
        db = mysql.connector.connect(
        host="stock100-swopnil100-1453.h.aivencloud.com",
        port=11907,
        user="avnadmin",
        passwd="AVNS_5RG3ixLOO6L1IRdRAC9",
        database="Stock",
        )
        cursor = db.cursor()
        query = "SELECT Money FROM ID WHERE Username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()
        db.close()
        
        if result:
            return result[0]
        else:
            return None
    except Exception as e:
        print("Error fetching available money:", e)
        return None

@app.route('/admin')
def admin():
    if 'username' in session and session['username'] == "admin": 
        return render_template('admin.html', username=session['username'], stocks=stocks)
    else:
        flash('Please log in as an admin', 'error')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You were successfully logged out', 'success')
    return redirect(url_for('index'))

from flask import request

from datetime import datetime


# Function to fetch available money for a user
def fetch_available_money(username):
    try:
        cursor = db.cursor()
        query = "SELECT Money FROM ID WHERE Username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return result[0]
        else:
            return None
    except Exception as e:
        print("Error fetching available money:", e)
        return None

# Function to update available money for a user
def update_available_money(username, amount):
    try:
        cursor = db.cursor()
        query = "UPDATE ID SET Money = Money + %s WHERE Username = %s"
        cursor.execute(query, (amount, username))
        db.commit()
        cursor.close()
        return True
    except Exception as e:
        print("Error updating available money:", e)
        return False

# Function to update the "My Stocks" table for a user
def update_my_stocks(username, symbol, volume):
    try:
        cursor = db.cursor()
        query = "INSERT INTO new_table (Username, Symbol, Volume) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE Volume = Volume + %s"
        cursor.execute(query, (username, symbol, volume, volume))
        db.commit()
        cursor.close()
        return True
    except Exception as e:
        print("Error updating My Stocks:", e)
        return False

# Function to handle buying stocks
@app.route('/buy/<symbol>', methods=['POST'])
def buy(symbol):
    if 'username' in session:
        username = session['username']
        if symbol in stocks:
            volume = int(request.form['volume'])
            if stocks[symbol]['volume'] >= volume:
                total_cost = volume * stocks[symbol]['price']
                available_money = fetch_available_money(username)
                if available_money is not None and available_money >= total_cost:
                    # Deduct the cost of purchased stocks from available money
                    if update_available_money(username, -total_cost):
                        # Deduct the volume from available stocks
                        stocks[symbol]['volume'] -= volume
                        # Update the user's "My Stocks" table
                        if update_my_stocks(username, symbol, volume):
                            flash(f'You bought {volume} shares of {symbol} successfully', 'success')
                            return redirect(url_for('user'))
                        else:
                            flash('Error updating My Stocks', 'error')
                    else:
                        flash('Error updating available money', 'error')
                else:
                    flash('Insufficient funds', 'error')
            else:
                flash('Not enough stocks available', 'error')
        else:
            flash('Stock not found', 'error')
    else:
        flash('Please log in', 'error')
    return redirect(url_for('login'))

# Function to handle selling stocks
@app.route('/sell/<symbol>', methods=['POST'])
def sell(symbol):
    if 'username' in session:
        username = session['username']
        if symbol in stocks:
            volume = int(request.form['volume'])
            # Check if the user owns the specified volume of the stock
            cursor = db.cursor()
            query = "SELECT Volume FROM new_table WHERE Username = %s AND Symbol = %s"
            cursor.execute(query, (username, symbol))
            result = cursor.fetchone()
            cursor.close()
            if result and result[0] >= volume:
                # Calculate the sale amount
                sale_amount = volume * stocks[symbol]['price']
                # Update available money
                if update_available_money(username, sale_amount):
                    # Update the user's "My Stocks" table
                    if update_my_stocks(username, symbol, -volume):
                        flash(f'You sold {volume} shares of {symbol} successfully', 'success')
                        return redirect(url_for('user'))
                    else:
                        flash('Error updating My Stocks', 'error')
                else:
                    flash('Error updating available money', 'error')
            else:
                flash('You don\'t own enough of this stock to sell or you don\'t own it at all!', 'error')
        else:
            flash('Stock not found', 'error')
    else:
        flash('Please log in', 'error')
    return redirect(url_for('login'))


@app.route('/prices/<symbol>')
def get_prices(symbol):
    if symbol in stocks:
        real_time_price = get_real_time_price(symbol)
        if real_time_price:
            timestamp = int(datetime.now().timestamp() * 1000)  # Convert to milliseconds
            return jsonify({'time': [timestamp], 'price': [real_time_price], 'stocks': stocks})  # Include time, price, and stocks data in the response
    return jsonify({'time': [], 'price': [], 'stocks': stocks})  # Include empty arrays for time, price, and stocks data in the response if stock symbol not found


@app.route('/add_stock', methods=['POST'])
def add_stock():
    if 'username' in session and session['username'] == "admin":
        symbol = request.form['symbol']
        company_name = request.form['company_name']
        price = float(request.form['price'])
        volume = int(request.form['volume'])
        if symbol not in stocks:
            stocks[symbol] = {'company_name': company_name, 'price': price, 'volume': volume}
            flash(f'Stock {symbol} added successfully', 'success')
        else:
            flash('Stock already exists', 'error')
    else:
        flash('Unauthorized access', 'error')
    return redirect(url_for('admin'))

def get_real_time_price(symbol):
    # Connect to the database
    db = mysql.connector.connect(
    host="stock100-swopnil100-1453.h.aivencloud.com",
    port=11907,
    user="avnadmin",
    passwd="AVNS_5RG3ixLOO6L1IRdRAC9",
    database="Stock",
    )
    # Create a cursor
    cursor = db.cursor(dictionary=True)
    
    # Query the database for the latest price of the given symbol
    query = "SELECT Price FROM NTT WHERE Name = %s ORDER BY Time DESC LIMIT 1"
    cursor.execute(query, (symbol,))
    result = cursor.fetchone()
    
    # Close the cursor and database connection
    cursor.close()
    db.close()
    
    # Return the latest price if available, otherwise return None
    if result:
        return result['Price']
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)
