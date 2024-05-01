from collections import OrderedDict
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime, timedelta
import mysql.connector
import threading
import time
import json

import requests

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime, timedelta
import mysql.connector
import threading
import time
import json
import hashlib
from flask import current_app


def inject_get_and_remove_flash_messages(app):
    @app.context_processor
    def utility_processor():
        def get_and_remove_flash_messages():
            messages = []
            for message in get_flashed_messages(with_categories=True):
                category = message[0]
                message_text = message[1]
                messages.append({'category': category, 'message': message_text})
                session.pop('_flashes', None)
            return messages
        return dict(get_and_remove_flash_messages=get_and_remove_flash_messages)


from flask import get_flashed_messages, session
app = Flask(__name__)
inject_get_and_remove_flash_messages(app)
@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "img-src 'self' * data:;"
    return response
def get_and_remove_flash_messages():
    messages = []
    for message in get_flashed_messages(with_categories=True):
        category = message[0]
        message_text = message[1]
        messages.append({'category': category, 'message': message_text})
        session.pop('_flashes', None)
    return messages
# Function to hash the password using SHA-256
def hash_password(password):

    return hashlib.sha256(password.encode()).hexdigest()
from bank import process_payment
from flask import session

from flask import request, redirect, url_for, render_template
import mysql.connector
from flask import request, redirect, url_for, render_template
@app.route('/home')
def home():
    return render_template('dash.html')
import mysql.connector
@app.route('/money')
def money():
    username = session.get('username')
    available_money=fetch_available_money(username)

    return render_template('add_money.html',available_money=available_money)

def get_user(card_holder_name):
    try:
        db = mysql.connector.connect(
            # host="stock100-swopnil100-1453.h.aivencloud.com",
            port=11907,
            user="avnadmin",
            passwd="AVNS_5RG3ixLOO6L1IRdRAC9",
            database="Stock"
        )

        cursor = db.cursor()

        query = "SELECT * FROM bankdata WHERE card_holder_name = %s"
        cursor.execute(query, (card_holder_name,))

        user_data = cursor.fetchone()

        cursor.close()
        db.close()

        if user_data:
            user = {
                'username': user_data[4],  # Assuming the username is in the second column
                'balance': user_data[5]    # Assuming the balance is in the third column
            }
            return user
        else:
            return None
    except Exception as e:
        print("Error retrieving user data:", e)
        return None
def decrease_balance(username, amount):
    try:
        db = mysql.connector.connect(
            host="stock100-swopnil100-1453.h.aivencloud.com",
            port=11907,
            user="avnadmin",
            passwd="AVNS_5RG3ixLOO6L1IRdRAC9",
            database="Stock"
        )

        cursor = db.cursor()

        update_query = "UPDATE bankdata SET balance = balance - %s WHERE card_holder_name = %s"
        cursor.execute(update_query, (amount, username))

       
    except Exception as e:
        print("Error decreasing balance:", e)
        return False

   
def increase_balance(username, amount):
    try:
        db = mysql.connector.connect(
            host="stock100-swopnil100-1453.h.aivencloud.com",
            port=11907,
            user="avnadmin",
            passwd="AVNS_5RG3ixLOO6L1IRdRAC9",
            database="Stock"
        )

        cursor = db.cursor()

        update_query = "UPDATE bankdata SET balance = balance + %s WHERE card_holder_name = %s "
        cursor.execute(update_query, (amount, username))

    except Exception as e:
        print("Error decreasing balance:", e)
        return False

# Connect to the MySQL database
db = mysql.connector.connect(
        host="stock100-swopnil100-1453.h.aivencloud.com",
        port=11907,
        user="avnadmin",
        passwd="AVNS_5RG3ixLOO6L1IRdRAC9",
        database="Stock"
    )
@app.route('/add_money', methods=['GET', 'POST'])
def add_money():
    username = session.get('username')
    available_money=fetch_available_money(username)
    
    if request.method == 'POST':
        payment_method = request.form['payment_method']
        amount = float(request.form['amount'])
        username = session.get('username')
        


       


        if username is None:
            flash('User not logged in', 'error')
            return redirect(url_for('login'))

        try:
            if payment_method == 'credit_card':
                card_number = request.form['card_number']
                expiry_date = request.form['expiry_date']
                card_holder_name=request.form['card_holder_name']
                cvv = request.form['cvv']

                cursor = db.cursor()
                query = "SELECT * FROM bankdata WHERE card_number = %s AND expiry_date = %s AND cvv = %s"
                cursor.execute(query, (card_number, expiry_date, cvv))
                result = cursor.fetchone()
                cursor.close()
                if result:
                    decrease_balance(card_holder_name, amount)
                    update_available_money(username,amount)
                    available_money=fetch_available_money(username)
                       

                    flash(f'Payment of ${amount} successful', 'success')
                
            elif payment_method == 'bank':
                bank_name = request.form['bank_name']
                account_number = request.form['account_number']
                routing_number = request.form['routing_number']
                card_holder_name=request.form['account_holder_name']

                

                cursor = db.cursor()
                query = "SELECT * FROM bankdata WHERE bank_name = %s AND account_number = %s AND routing_number = %s"
                cursor.execute(query, (bank_name, account_number, routing_number))
                result = cursor.fetchone()
                cursor.close()

                if result:
                    decrease_balance(card_holder_name, amount)
                    update_available_money(username,amount)
                    available_money=fetch_available_money(username)


                    flash(f'Payment of ${amount} successful', 'success')
                   
                else:
                    flash('Invalid bank details', 'error')

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            # Log the error for debugging purposes


    # Render the add_money.html template with flash messages
    return render_template('add_money.html',available_money=available_money)

@app.route('/news')
def get_news():
    url = 'https://api.tickertick.com/feed?q=z:aapl&n=200'
    response = requests.get(url)
    if response.status_code == 200:
        news_data = response.json().get('stories', [])  # Extracting 'stories' field
        return render_template('news.html', stories=news_data)
    else:
        return 'Error fetching news data'
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

# Your other Flask routes and functions go here...



# Function to hash the password using SHA-256

csp = {
    'default-src': ["'self'", 'https://code.highcharts.com'],
    'script-src': ["'self'", "'unsafe-inline'", 'https://code.highcharts.com'],

    'style-src': ["'self'", "'unsafe-inline'", 'https://code.highcharts.com'],
    'img-src': ["'self'", 'https://i.ibb.co/'],
   
    


}
@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    username = session.get('username')
    available_money=fetch_available_money(username)
    
    if request.method == 'POST':
        payment_method = request.form['payment_method']
        amount = float(request.form['amount'])
        username = session.get('username')
       


        if username is None:
            flash('User not logged in', 'error')
            return redirect(url_for('login'))

        try:
            if payment_method == 'credit_card':
                card_number = request.form['card_number']
                expiry_date = request.form['expiry_date']
                card_holder_name=request.form['card_holder_name']
                cvv = request.form['cvv']

                cursor = db.cursor()
                query = "SELECT * FROM bankdata WHERE card_number = %s AND expiry_date = %s AND cvv = %s"
                cursor.execute(query, (card_number, expiry_date, cvv))
                result = cursor.fetchone()
                cursor.close()
                if result:
                    
                    update_available_money1(username,amount)
                    available_money=fetch_available_money(username)

                    flash(f'Withdraw of ${amount} successful', 'success')
                    
            elif payment_method == 'bank':
                bank_name = request.form['bank_name']
                account_number = request.form['account_number']
                routing_number = request.form['routing_number']
                card_holder_name=request.form['account_holder_name']

                

                cursor = db.cursor()
                query = "SELECT * FROM bankdata WHERE bank_name = %s AND account_number = %s AND routing_number = %s"
                cursor.execute(query, (bank_name, account_number, routing_number))
                result = cursor.fetchone()
                cursor.close()

                if result:
                    increase_balance(card_holder_name, amount)
                    update_available_money1(username, amount)
                    available_money=fetch_available_money(username)


                    flash(f'Withdraw of ${amount} successful', 'success')
                   
                else:
                    flash('Invalid bank details', 'error')
                

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            # Log the error for debugging purposes
    print(available_money)
    available_money=fetch_available_money(username)

    # Render the add_money.html template with flash messages
    return render_template('withdraw.html',available_money=available_money)
app.secret_key = 'your_secret_key'
import mysql.connector

db = mysql.connector.connect(
        host="stock100-swopnil100-1453.h.aivencloud.com",
        port=11907,
        user="avnadmin",
        passwd="AVNS_5RG3ixLOO6L1IRdRAC9",
        database="Stock",
        )

cursor = db.cursor()

cursor.execute("SELECT * FROM stocks_list")
results = cursor.fetchall()

stocks = {}

for row in results:
    stocks[row[1]] = {
        'company_name': row[2],
        'price': row[3],
        'volume': row[4]
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
    db = mysql.connector.connect(
            host="stock100-swopnil100-1453.h.aivencloud.com",
            port=11907,
            user="avnadmin",
            passwd="AVNS_5RG3ixLOO6L1IRdRAC9",
            database="Stock",
        )
    cursor = db.cursor(dictionary=True)
    # Fetch required data from the database or other sources
    # For example, let's assume you want to fetch the available stocks and their prices
   

    username = session.get('username')
    transfers = "SELECT timestamp, transaction_type, symbol, company_name, amount, number FROM transaction WHERE username = %s ORDER BY timestamp DESC LIMIT 5"
    cursor.execute(transfers, (username,))
    transfers = cursor.fetchall()
   
    if 'username' in session:
        username = session['username']
        available_money = fetch_available_money(username)
        cursor = db.cursor()
        query = "SELECT Symbol, Volume FROM new_table WHERE Username = %s"
        cursor.execute(query, (username,))
        user_stocks = cursor.fetchall()
        cursor.close()
        if available_money is not None:
            return render_template('dash.html', username=username, stocks=OrderedDict(sorted(stocks.items())), available_money=available_money, user_stocks=user_stocks,transfers=transfers)
        else:
            flash('Error fetching available money', 'error')
            return render_template('dash.html', username=username, stocks=OrderedDict(sorted(stocks.items())), user_stocks=user_stocks, transfers=transfers)
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
        cursor10 = db.cursor()
        query = "SELECT Money FROM ID WHERE Username = %s"
        cursor10.execute(query, (username,))
        result = cursor10.fetchone()
        cursor10.close()
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
       user_data = fetch_user_data()
       return render_template('admin.html', username=session['username'], stocks=OrderedDict(sorted(stocks.items())), user_data=user_data)
   else:
       flash('Please log in as an admin', 'error')
       return redirect(url_for('login'))
def fetch_user_data():
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

       # Create a dictionary to store user data with merged stocks
       user_data = {}

       # Process the data and merge stocks for each user
       for row in rows:
           username = row['Username']
           money = row['Money']
           symbol = row['Symbol']
           volume = row['TotalVolume']
           if username not in user_data:
               user_data[username] = {'Username': username, 'Money': money, 'Stocks': {}}
           if symbol not in user_data[username]['Stocks']:
               user_data[username]['Stocks'][symbol] = volume
           else:
               user_data[username]['Stocks'][symbol] += volume

       cursor.close()
       return user_data.values()
   except Exception as e:
       print("Error fetching user data:", e)
       return None

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You were successfully logged out', 'success')
    return redirect(url_for('index'))

from flask import request

from datetime import datetime


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
def update_available_money1(username, amount):
    try:
        cursor = db.cursor()
        query = "UPDATE ID SET Money = Money - %s WHERE Username = %s"
        cursor.execute(query, (amount, username))
        db.commit()
        cursor.close()
        return True
    except Exception as e:
        print("Error updating available money:", e)
        return False
# Function to update the "My Stocks" table for a user
# Function to update the user's stock portfolio in the database
# Function to update the user's stock portfolio in the database
# Function to update the user's stock portfolio in the database
def update_my_stocks(username, symbol, volume_change):
    try:
        cursor = db.cursor()
        # Check if the user already owns the specified stock
        cursor.execute("SELECT * FROM new_table WHERE Username = %s AND Symbol = %s", (username, symbol))
        existing_record = cursor.fetchone()
        if existing_record:
             # Debugging: Print volume change
            # If the user already owns the stock, update the volume
            existing_volume = int(existing_record[3])  # Convert existing volume to integer
            new_volume = existing_volume + volume_change
            
            if new_volume <= 0:
                # If the updated volume is zero or negative, remove the record from the table
                cursor.execute("DELETE FROM new_table WHERE Username = %s AND Symbol = %s", (username, symbol))
            else:
                # Otherwise, update the volume in the existing record
                cursor.execute("UPDATE new_table SET Volume = %s WHERE Username = %s AND Symbol = %s", (new_volume, username, symbol))
        elif volume_change > 0:
            # If the user doesn't own the stock and is buying (volume_change > 0), insert a new record
            cursor.execute("INSERT INTO new_table (Username, Symbol, Volume) VALUES (%s, %s, %s)", (username, symbol, int(volume_change)))
        db.commit()
        cursor.close()
        return True
    except Exception as e:
        print("Error updating My Stocks:", e)
        return False

@app.route('/buy/<symbol>', methods=['POST'])
def buy(symbol):
    username=session['username']
    available_money = fetch_available_money(username)

    db = mysql.connector.connect(
            host="stock100-swopnil100-1453.h.aivencloud.com",
            port=11907,
            user="avnadmin",
            passwd="AVNS_5RG3ixLOO6L1IRdRAC9",
            database="Stock",)
    error_message = None
    if 'username' in session:
        username = session['username']
        if symbol in stocks:
            volume = int(request.form['volume'])
            sale_amount = volume * stocks[symbol]['price']

            if stocks[symbol]['volume'] >= volume:
                total_cost = volume * stocks[symbol]['price']
                available_money = fetch_available_money(username)
                if available_money is not None and available_money >= total_cost:
                    # Deduct the cost of purchased stocks from available money
                    if update_available_money(username, -total_cost):
                        # Increase the price by 10% when buying
                        buy_ratio = 1
                        new_price = stocks[symbol]['price'] * (1 + buy_ratio)
                        # Decrease the volume of available stocks
                        stocks[symbol]['volume'] -= volume
                        # Update the price in the stocks dictionary
                        stocks[symbol]['price'] = round(new_price, 2)
                        # Ensure volume_change is an integer before calling update_my_stocks
                        volume_change = int(volume)
                        update_my_stocks(username, symbol, volume_change)
                        cursor = db.cursor()
                        query = "UPDATE stocks_list SET Price = %s, Volume = Volume - %s WHERE Symbol = %s"
                        cursor.execute(query, (new_price, volume, symbol))
                        transaction_time = datetime.now()
                        transaction_type = "buy"
                        company_name = stocks[symbol]['company_name']
                        amount = sale_amount
                        number = volume
                        query = "INSERT INTO transaction (username, timestamp, transaction_type, symbol, company_name, amount, number) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        cursor.execute(query, (username, transaction_time, transaction_type, symbol, company_name, amount, number))
                        cursor.execute("INSERT INTO new_table (Username, Symbol, Volume) VALUES (%s, %s, %s)", (username, symbol, number))
                        cursor.close()
                        db.commit()
                        flash(f'You bought {volume} shares of {symbol} successfully', 'success')
                        flash(f'The price increased by {buy_ratio * 100}% due to buying', 'info')
                    else:
                        error_message = 'Error updating available money'
                else:
                    error_message = 'Insufficient funds'
            else:
                error_message = 'Not enough stocks available'
        else:
            error_message = 'Stock not found'
    else:
        error_message = 'Please log in'

    username = session.get('username')
    cursor = db.cursor()
    query = "SELECT Symbol, Volume FROM new_table WHERE Username = %s"
    cursor.execute(query, (username,))
    user_stocks = cursor.fetchall()
    cursor.close()
    return render_template('buy.html', username=username, stocks=OrderedDict(sorted(stocks.items())), available_money=available_money, user_stocks=user_stocks, error_message=error_message)
@app.route('/sell/<symbol>', methods=['POST'])
def sell(symbol):
    username=session['username']
    available_money = fetch_available_money(username)

    db = mysql.connector.connect(
            host="stock100-swopnil100-1453.h.aivencloud.com",
            port=11907,
            user="avnadmin",
            passwd="AVNS_5RG3ixLOO6L1IRdRAC9",
            database="Stock",)
    error_message = None
    if 'username' in session:
        username = session['username']
        if symbol in stocks:
            volume = int(request.form['volume'])
            sale_amount = volume * stocks[symbol]['price']

            if stocks[symbol]['volume'] >= volume:
                total_cost = volume * stocks[symbol]['price']
                available_money = fetch_available_money(username)
                if available_money is not None and available_money >= total_cost:
                    # Deduct the cost of purchased stocks from available money
                    if update_available_money(username, +total_cost):
                        # Increase the price by 10% when buying
                        buy_ratio = 1
                        new_price = stocks[symbol]['price'] * (1 + buy_ratio)
                        # Decrease the volume of available stocks
                        stocks[symbol]['volume'] += volume
                        # Update the price in the stocks dictionary
                        stocks[symbol]['price'] = round(new_price, 2)
                        # Ensure volume_change is an integer before calling update_my_stocks
                        volume_change = int(volume)
                        update_my_stocks(username, symbol, volume_change)
                        cursor = db.cursor()
                        query = "UPDATE stocks_list SET Price = %s, Volume = Volume + %s WHERE Symbol = %s"
                        cursor.execute(query, (new_price, volume, symbol))
                        transaction_time = datetime.now()
                        transaction_type = "sell"
                        company_name = stocks[symbol]['company_name']
                        amount = sale_amount
                        number = volume
                        query = "INSERT INTO transaction (username, timestamp, transaction_type, symbol, company_name, amount, number) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        cursor.execute(query, (username, transaction_time, transaction_type, symbol, company_name, amount, number))
                        cursor.execute("INSERT INTO new_table (Username, Symbol, Volume) VALUES (%s, %s, %s)", (username, symbol, number))
                        cursor.close()
                        db.commit()
                        flash(f'You sold {volume} shares of {symbol} successfully', 'success')
                    else:
                        error_message = 'Error updating available money'
                else:
                    error_message = 'Insufficient funds'
            else:
                error_message = 'Not enough stocks available'
        else:
            error_message = 'Stock not found'
    else:
        error_message = 'Please log in'

    username = session.get('username')
    cursor = db.cursor()
    query = "SELECT Symbol, Volume FROM new_table WHERE Username = %s"
    cursor.execute(query, (username,))
    user_stocks = cursor.fetchall()
    cursor.close()
    return render_template('buy.html', username=username, stocks=OrderedDict(sorted(stocks.items())), available_money=available_money, user_stocks=user_stocks, error_message=error_message)
@app.route('/mystocks')
def mystocks():
    # Update the user_stocks list here
    if 'username' in session:
        username = session['username']
        available_money = fetch_available_money(username)
        cursor = db.cursor()
        query = "SELECT Symbol, Volume FROM new_table WHERE Username = %s"
        cursor.execute(query, (username,))
        user_stocks = cursor.fetchall()
        cursor.close()
    return render_template('my_stocks.html', user_stocks=user_stocks)

@app.route('/latest_transfers')
def latest_transfers():
    db = mysql.connector.connect(
            host="stock100-swopnil100-1453.h.aivencloud.com",
            port=11907,
            user="avnadmin",
            passwd="AVNS_5RG3ixLOO6L1IRdRAC9",
            database="Stock",
        )
    cursor = db.cursor(dictionary=True)
    # Fetch required data from the database or other sources
    # For example, let's assume you want to fetch the available stocks and their prices
    available_stocks = fetch_available_stocks() 

    username = session.get('username')
    transfers = "SELECT timestamp, transaction_type, symbol, company_name, amount, number FROM transaction WHERE username = %s ORDER BY timestamp DESC LIMIT 5"
    cursor.execute(transfers, (username,))
    transfers = cursor.fetchall()
    
    cursor.close()
    
     # Implement this function to fetch available stocks from your database
    available_money=fetch_available_money(username)
    # Pass the fetched data to the dash.html template
    return render_template('dash.html', available_stocks=available_stocks, stocks=OrderedDict(sorted(stocks.items())),available_money=available_money,transfers=transfers)


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
        try:
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
            # Create the table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stocks_list (
                    ID INT AUTO_INCREMENT PRIMARY KEY,
                    Symbol VARCHAR(10),
                    CompanyName VARCHAR(255),
                    Price FLOAT,
                    Volume INT
                )
            """)
            # Insert the new stock data into the table
            cursor.execute("INSERT INTO stocks_list (Symbol, CompanyName, Price, Volume) VALUES (%s, %s, %s, %s)", (symbol, company_name, price, volume))
            # Commit the transaction
            db.commit()

            # Close the cursor and database connection
            cursor.close()
            db.close()

            flash(f'Stock {symbol} added successfully', 'success')

        except Exception as e:
            print("Error adding stock:", e)
            flash('Error adding stock', 'error')
        
    else:
        flash('Unauthorized access', 'error')
    return redirect(url_for('admin'))
from flask import request

@app.route('/delete_stock/<symbol>', methods=['POST', 'DELETE'])
def delete_stock(symbol):
    if 'username' in session and session['username'] == "admin":
        # Check if the stock exists
        if symbol in stocks:
            # Remove the stock from the stocks dictionary
            del stocks[symbol]
            # Update the database to remove the stock
            cursor = db.cursor()
            cursor.execute("DELETE FROM stocks_list WHERE Symbol = %s", (symbol,))
            db.commit()
            cursor.close()
            flash(f'Stock {symbol} deleted successfully', 'success')
        else:
            flash('Stock not found', 'error')
    else:
        flash('Unauthorized access', 'error')
    return redirect(url_for('admin'))


@app.route('/prices/<symbol>')
def get_prices(symbol):

    
    if symbol in stocks:
        limit = request.args.get('limit', default=10, type=int)  # Get the 'limit' query parameter (default to 10)
        real_time_prices = get_real_time_prices(symbol, limit)
       
        if real_time_prices:
            timestamps = [data['Time'] for data in real_time_prices]
            prices = [data['Price'] for data in real_time_prices]
            return jsonify({'time': timestamps, 'price': prices, 'stocks': stocks})
    return jsonify({'time': [], 'price': [], 'stocks': stocks})

def get_real_time_prices(symbol, limit):
    try:
        db = mysql.connector.connect(
            host="stock100-swopnil100-1453.h.aivencloud.com",
            port=11907,
            user="avnadmin",
            passwd="AVNS_5RG3ixLOO6L1IRdRAC9",
            database="Stock",
        )
        cursor = db.cursor(dictionary=True)

        # Query the database for the latest 'limit' prices of the given symbol
        query = "SELECT Time, Price FROM NTT WHERE Name = %s ORDER BY Time DESC LIMIT %s"
        cursor.execute(query, (symbol, limit))
        results = cursor.fetchall()

        cursor.close()
        db.close()

        return results
    except Exception as e:
        print("Error fetching real-time prices:", e)
        return None
    
def fetch_available_stocks():
    try:
        db = mysql.connector.connect(
            host="stock100-swopnil100-1453.h.aivencloud.com",
            port=11907,
            user="avnadmin",
            passwd="AVNS_5RG3ixLOO6L1IRdRAC9",
            database="Stock",
        )
        cursor = db.cursor(dictionary=True)

        # Query the database to fetch available stocks
        query = "SELECT Symbol, CompanyName, Price FROM stocks_list"
        cursor.execute(query)
        results = cursor.fetchall()

        cursor.close()
        db.close()

        return results
    except Exception as e:
        print("Error fetching available stocks:", e)
        return None

@app.route('/get_d')
def get_d():
    db = mysql.connector.connect(
            host="stock100-swopnil100-1453.h.aivencloud.com",
            port=11907,
            user="avnadmin",
            passwd="AVNS_5RG3ixLOO6L1IRdRAC9",
            database="Stock",
        )
    cursor = db.cursor(dictionary=True)
    # Fetch required data from the database or other sources
    # For example, let's assume you want to fetch the available stocks and their prices
    available_stocks = fetch_available_stocks() 

    username = session.get('username')
    transfers = "SELECT timestamp, transaction_type, symbol, company_name, amount, number FROM transaction WHERE username = %s ORDER BY timestamp DESC LIMIT 5"
    cursor.execute(transfers, (username,))
    transfers = cursor.fetchall()
    
    cursor.close()
    
     # Implement this function to fetch available stocks from your database
    available_money=fetch_available_money(username)
    # Pass the fetched data to the dash.html template
    return render_template('dash.html',username=username, available_stocks=available_stocks, stocks=OrderedDict(sorted(stocks.items())),available_money=available_money,transfers=transfers)
@app.route('/trade')
def trade():
    db = mysql.connector.connect(
            host="stock100-swopnil100-1453.h.aivencloud.com",
            port=11907,
            user="avnadmin",
            passwd="AVNS_5RG3ixLOO6L1IRdRAC9",
            database="Stock",
        )
    cursor = db.cursor(dictionary=True)
    # Fetch required data from the database or other sources
    # For example, let's assume you want to fetch the available stocks and their prices
    available_stocks = fetch_available_stocks() 

    username = session.get('username')
    query_transactions = "SELECT timestamp, transaction_type, symbol, company_name, amount, number FROM transaction WHERE username = %s ORDER BY timestamp DESC LIMIT 5"
    cursor.execute(query_transactions, (username,))
    transfers = cursor.fetchall()
    cursor.close()
    
     # Implement this function to fetch available stocks from your database
    available_money=fetch_available_money(username)
    return render_template('buy.html', available_stocks=available_stocks, stocks=OrderedDict(sorted(stocks.items())),available_money=available_money,transfers=transfers)


if __name__ == '__main__':
    app.run(debug=True)