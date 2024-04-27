from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Sample user data (for demonstration)
users = {'admin': 'admin', 'user': 'user'}

# Sample stock data (for demonstration)
stocks = {
    'AAPL': {'company_name': 'Apple Inc.', 'price': 135.00, 'volume': 1000},
    'GOOGL': {'company_name': 'Alphabet Inc.', 'price': 2350.00, 'volume': 500},
    'MSFT': {'company_name': 'Microsoft Corporation', 'price': 250.00, 'volume': 800},
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            flash('You were successfully logged in', 'success')
            if username == "user":
                return redirect(url_for('user'))
            elif username == "admin":
                return redirect(url_for('admin'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You were successfully logged out', 'success')
    return redirect(url_for('index'))

@app.route('/user')
def user():
    if 'username' in session and session['username'] == "user":  
        return render_template('user.html', username=session['username'], stocks=stocks)
    else:
        return redirect(url_for('login'))

@app.route('/admin')
def admin():
    if 'username' in session and session['username'] == "admin": 
        return render_template('admin.html', username=session['username'], stocks=stocks)
    else:
        return redirect(url_for('login'))

@app.route('/buy/<symbol>', methods=['POST'])
def buy(symbol):
    if 'username' in session:
        if symbol in stocks:
            volume = int(request.form['volume'])
            if stocks[symbol]['volume'] >= volume:
                # Calculate the new price after buying
                buy_ratio = 0.1  # 10% increase when buying
                new_price = stocks[symbol]['price'] * (1 + buy_ratio)
                stocks[symbol]['volume'] -= volume
                stocks[symbol]['price'] = round(new_price, 2)  # Round to 2 decimal places
                flash(f'You bought {volume} shares of {symbol} successfully', 'success')
            else:
                flash('Not enough stocks available', 'error')
        else:
            flash('Stock not found', 'error')
    return redirect(url_for('user'))

@app.route('/sell/<symbol>', methods=['POST'])
def sell(symbol):
    if 'username' in session:
        if symbol in stocks:
            volume = int(request.form['volume'])
            # Calculate the new price after selling
            sell_ratio = 0.1  # 10% decrease when selling
            new_price = stocks[symbol]['price'] * (1 - sell_ratio)
            stocks[symbol]['volume'] += volume
            stocks[symbol]['price'] = round(new_price, 2)  # Round to 2 decimal places
            flash(f'You sold {volume} shares of {symbol} successfully', 'success')
        else:
            flash('Stock not found', 'error')
    return redirect(url_for('user'))


@app.route('/prices')
def get_prices():
    # Fetch real-time prices for all stocks
    real_time_prices = {}
    for symbol, data in stocks.items():
        # Logic to fetch real-time prices for each stock
        # For demonstration purposes, let's assume you have a function `get_real_time_price(symbol)`
        # that fetches the real-time price for a given stock symbol
        real_time_prices[symbol] = get_real_time_price(symbol)
    return jsonify(real_time_prices)

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
    # Your code to fetch real-time price for the given symbol goes here
    # This could involve querying an API or database
    
    # For demonstration, let's assume you have a dictionary of real-time prices
    real_time_prices = {
        'AAPL': 135.50,
        'GOOGL': 2345.67,
        'MSFT': 251.34,
        # Add more symbols and corresponding prices as needed
    }
    
    # Return the real-time price for the given symbol
    return real_time_prices.get(symbol)
if __name__ == '__main__':
    app.run(debug=True)
