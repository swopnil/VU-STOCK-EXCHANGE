import requests
import json

def process_bank_transfer(bank_name, account_number, routing_number, amount):
    # Implement secure bank transfer logic here
    # You can use a third-party payment gateway or bank API for this
    # For example, you can make an API call to your bank's server with the provided information
    # and receive a response indicating whether the transfer was successful or not

    # For now, let's assume the transfer is always successful
    return True

def process_payment(payment_method, card_number, expiry_date, cvv, bank_name, account_number, routing_number, amount):
    if payment_method == 'credit_card':
        # Implement secure credit card payment processing logic here
        # You can use a third-party payment gateway or credit card processing API for this
        # For example, you can make an API call to a payment gateway with the provided card information
        # and receive a response indicating whether the payment was successful or not

        # For now, let's assume the payment is always successful
        return True
    elif payment_method == 'bank':
        return process_bank_transfer(bank_name, account_number, routing_number, amount)
    else:
        return False