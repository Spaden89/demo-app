from flask import Flask, jsonify, abort, request, render_template, session, redirect, url_for
import requests
import os
import json
from json2html import *
import dimebox

app = Flask(__name__, instance_relative_config=True)
# Set secret key for sessions
app.secret_key = os.environ.get("SECRET_KEY")

#Loading default configuration
app.config.from_object('config.default')
# Load the configuration from the instance folder
app.config.from_pyfile('config.py')

host = os.environ.get("VERIFONE_HOST")
api_key = os.environ.get("API_KEY")
account = os.environ.get("ACCOUNT")
organisation = os.environ.get("ORGANISATION")
customer = os.environ.get("CUSTOMER")
threeds_authenticator = os.environ.get("AUTHENTICATOR")

ui_host = host + '/reports/transactions/'
api_host = host + '/v1/'

# Set the api header
headers = {
    "Content-Type": "application/json",
    "x-apikey": api_key
}

# Print the host that is used
print(f"Connected to Verifone environment: {host}")

def websiteVisit():
    # Get and print client ip address
    client_ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    print(f"Client IP address: {client_ip_address}")
    # Get and print client User-Agent
    client_user_agent = request.headers.get('User-Agent')
    print(f"Client User-Agent is: {client_user_agent}")
    return client_ip_address, client_user_agent

@app.route('/transaction', methods=['GET','POST'])
def transaction():
    if request.method == 'POST':
        # create transaction and return json and transaction ID
        if request.form.get('card'):
            card = request.form.get('card')
        else:
            card = os.environ.get("CARD")
        if session.get('customer'):
            customer = session.get('customer')
        else:
            customer = os.environ.get("CUSTOMER")
        if session.get('client_ip_address') and session.get('client_user_agent'):
            client_ip_address = session.get('client_ip_address')
            client_user_agent = session.get('client_user_agent')
        else:
            (client_ip_address, client_user_agent) = websiteVisit()
        trx_json = dimebox.createTransaction(card, customer, client_ip_address, client_user_agent)
        trx_id = trx_json['_id']
        return redirect(url_for('thank_you',transaction=[trx_id]))
    return render_template('demo.html')

@app.route('/demo/default', methods=['GET','POST'])
def demo_default():
    (client_ip_address, client_user_agent) = websiteVisit()
    if request.method == 'POST':
        # store the card token in the card variable
        card = request.form.get('card')
        trx_json = dimebox.createTransaction(card, customer, client_ip_address, client_user_agent)
        trx_id = trx_json['_id']
        return redirect(url_for('thank_you',transaction=[trx_id]))
    return render_template('demo.html')

@app.route('/demo/newcustomer', methods=['GET'])
def newcustomer():
    (client_ip_address, client_user_agent) = websiteVisit()
    session['client_ip_address'] = client_ip_address
    session['client_user_agent'] = client_user_agent
    session_client_ip = session.get('client_ip_address')
    session_client_user = session.get('client_user_agent')
    print(f'client ip stored in session: {session_client_ip}')
    print(f'client user agent stored in session: {session_client_user}')
    return render_template('newcustomer.html')

@app.route('/customer', methods=['POST'])
def customer_endpoint():
    if request.method == 'POST':
        print("Customer form has been filled:" + str(request.form.to_dict(flat=False)))
        (first, last) = request.form['name'].split(" ", 1) 
        email = request.form['email']
        address = request.form['address']
        city = request.form['city']
        postal_code = request.form['postal']
        country = request.form['country']
        customer_json = dimebox.createCustomer(email, first, last, address, city, postal_code, country)
        session['customer'] = customer_json['_id']
        session_customer = session.get('customer')
        session_client_ip = session.get('client_ip_address')
        session_client_user = session.get('client_user_agent')
        print(f'Customer stored in session: {session_customer}')
        print(f'client ip stored in session: {session_client_ip}')
        print(f'client user agent stored in session: {session_client_user}')
        customer = customer_json
        return render_template('existingcustomer.html', customer = customer)

@app.route('/thankyou', methods=['GET'])
def thank_you():
    (client_ip_address, client_user_agent) = websiteVisit()
    if request.args.get('transaction_id'):
        transaction_id = request.args.get('transaction_id')
        params = {
        '_populate':'card+customer'
        }
        # GET transaction
        transaction_json = dimebox.getTransaction(transaction_id, params)
        transaction_link = ui_host + str(transaction_json['_id'])
    if request.args.get('authentication_id'):
        customer_json = dimebox.getCustomer(customer)
        authentication_id = request.args.get('authentication_id')
        authentication_json = dimebox.getAuthentication(authentication_id)
    if request.args.get('card_id'):
        customer_json = dimebox.getCustomer(customer)
        card_id = request.args.get('card_id')
        card_json = dimebox.getCard(card_id)
        card_link = host + '/administration/cards/' + card_id
    return render_template('thankyou.html', **locals())

@app.route('/demo/checkout', methods=['GET'])
def demo_checkout():
    (client_ip_address, client_user_agent) = websiteVisit()
    return render_template('checkout.html')

@app.route('/checkout', methods=['POST'])
def checkout_endpoint():
    if request.method == 'POST':
        # generate a checkout page
        amount = 1234 
        merchant_reference = "VF-001" 
        return_url = request.host_root + url_for('thank_you')
        # process transaction
        if request.form.get('process_transaction'):
            process_transaction = False
        else:
            process_transaction = True
        # immediate capture
        if request.form.get('capture_now'):
            capture_now = True
        else:
            capture_now = False
        # enable 3ds
        if request.form.get('threeds_enabled'):
            threeds_enabled = True
        else:
            threeds_enabled = False  
        threeds_currency = "GBP"
        threeds_transaction_mode = "S"
        template = api_host + "checkout/template/v1"
        # create checkout url
        checkout_json = dimebox.createCheckout(account, 
            amount, 
            customer, 
            merchant_reference, 
            return_url, 
            process_transaction, 
            capture_now, 
            threeds_authenticator, 
            threeds_enabled,
            threeds_currency, 
            threeds_transaction_mode,
            template)
        checkout_id = checkout_json['_id']
        checkout_url = checkout_json['url']
        return redirect(checkout_url)

@app.route('/thankyou_detailed/<transaction>', methods=['GET'])
def get_transaction_id(transaction):
    trx_id = transaction
    (client_ip_address, client_user_agent) = websiteVisit()
    print(f"Client User-Agent is: {client_user_agent}")
    params = {
        '_populate':'card+customer'
    }
    # GET transaction
    trx_json = dimebox.getTransaction(trx_id, params)
    print(trx_json)
    trx_table = json2html.convert(json = trx_json, table_attributes="class=\"table is-striped\"")
    trx_link = ui_host + str(trx_json['_id'])
    return render_template('thankyou_detailed.html', trx_table = trx_table, transaction = trx_json, trx_link = trx_link)

@app.route('/checkout_template', methods=['GET'])
def checkout_template():
    (client_ip_address, client_user_agent) = websiteVisit()
    return render_template('checkout_template.html')

if __name__ == '__main__':
    app.run()
