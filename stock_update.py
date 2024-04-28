import json
import threading
import time
from datetime import datetime, timedelta

def update_stock_data(stocks):
    while True:
        current_time = datetime.now()
        for symbol, data in stocks.items():
            # Adjust price based on user transactions
            if 'transactions' in data:
                for transaction in data['transactions']:
                    if transaction['type'] == 'buy':
                        data['price'] *= 1.1  # Increase price by 10% for buying
                        data['volume'] -= transaction['volume']
                    elif transaction['type'] == 'sell':
                        data['price'] *= 0.9  # Decrease price by 10% for selling
                        data['volume'] += transaction['volume']
                # Clear transactions after updating stock data
                data['transactions'] = []

            # Update time for each stock with different second
            data['time'] = (current_time - timedelta(seconds=len(stocks) - 1 - list(stocks.keys()).index(symbol))).strftime('%Y-%m-%d %H:%M:%S')

        # Wait for 1 second before updating again
        time.sleep(1)
