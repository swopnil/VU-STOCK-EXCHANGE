from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load stocks data from JSON file
def load_stocks():
    with open("stocks.json", "r") as f:
        return json.load(f)

# Save stocks data to JSON file
def save_stocks(stocks):
    with open("stocks.json", "w") as f:
        json.dump(stocks, f)

# Check if user is logged in
def is_logged_in():
    return 'username' in session

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Simple hardcoded authentication
        if username == "admin" and password == "admin":
            session['username'] = username
            return redirect(url_for('admin'))
        elif username == "user" and password == "user":
            session['username'] = username
            return redirect(url_for('user'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

# Admin route
@app.route('/admin')
def admin():
    if not is_logged_in() or session['username'] != "admin":
        return redirect(url_for('login'))
    
    stocks = load_stocks()
    return render_template('admin.html', stocks=stocks)

# User route
@app.route('/user')
def user():
    if not is_logged_in() or session['username'] != "user":
        return redirect(url_for('login'))
    
    stocks = load_stocks()
    return render_template('user.html', stocks=stocks)

# Buy route
@app.route('/buy', methods=['POST'])
def buy():
    if not is_logged_in() or session['username'] != "user":
        return redirect(url_for('login'))
    
    symbol = request.form['symbol']
    volume = int(request.form['volume'])
    
    stocks = load_stocks()
    
    if symbol not in stocks:
        flash(f"Stock {symbol} not found", 'error')
        return redirect(url_for('user'))
    
    available_volume = stocks[symbol]["volume"]
    if available_volume < volume:
        flash("Not enough stocks available", 'error')
        return redirect(url_for('user'))
    
    # Calculate the price change ratio
    price_change_ratio = volume / available_volume * 0.1
    
    # Update the price
    stocks[symbol]["price"] *= (1 + price_change_ratio)
    
    # Deduct the purchased volume from available volume
    stocks[symbol]["volume"] -= volume
    
    # Save updated stocks data
    save_stocks(stocks)
    
    flash(f"Successfully bought {volume} shares of {symbol}", 'success')
    return redirect(url_for('user'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
