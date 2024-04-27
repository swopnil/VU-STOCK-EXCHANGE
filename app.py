from flask import Flask, render_template, request, redirect, url_for, session, flash
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
        print("HELLO USER")
        return render_template('user.html', username=session['username'], stocks=stocks)
    else:
        return redirect(url_for('login'))

@app.route('/admin')
def admin():
    if 'username' in session and session['username'] == "admin": 
        print("HELLO")
        return render_template('admin.html', username=session['username'], stocks=stocks)
    else:
        return redirect(url_for('login'))

@app.route('/buy/<symbol>', methods=['POST'])
def buy(symbol):
    if 'username' in session:
        if symbol in stocks:
            volume = int(request.form['volume'])
            if stocks[symbol]['volume'] >= volume:
                stocks[symbol]['volume'] -= volume
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
            stocks[symbol]['volume'] += volume
            flash(f'You sold {volume} shares of {symbol} successfully', 'success')
        else:
            flash('Stock not found', 'error')
    return redirect(url_for('user'))


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

if __name__ == '__main__':
    app.run(debug=True)
