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
organisation = os.environ.get("ORGANISATION")
customer = os.environ.get("CUSTOMER")

ui_host = host + 'reports/transactions/'
api_host = host + 'v1/'

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
        card = request.form.get('card')
        customer = session.get('customer')
        client_ip_address = session.get('client_ip_address')
        client_user_agent = session.get('client_user_agent')
        trx_json = dimebox.createTransaction(card, customer, client_ip_address, client_user_agent)
        trx_id = trx_json['_id']
        return redirect(url_for('get_transaction_id', transaction = trx_id))
    return render_template('demo.html')

@app.route('/demo/default', methods=['GET','POST'])
def demo_default():
    (client_ip_address, client_user_agent) = websiteVisit()
    if request.method == 'POST':
        # store the card token in the card variable
        card = request.form.get('card')
        trx_json = dimebox.createTransaction(card, customer, client_ip_address, client_user_agent)
        trx_id = trx_json['_id']
        return redirect(url_for('get_transaction_id', transaction = trx_id))
    customer_json = dimebox.getCustomer(customer)
    card_list = []
    for card in customer_json['cards']:
        card_json = dimebox.getCard(card)
        card_list.append(card_json)
    print(card_list)
    return render_template('demo.html', card_list = card_list)

@app.route('/demo/newcustomer', methods=['GET','POST'])
def newcustomer():
    (client_ip_address, client_user_agent) = websiteVisit()
    if request.method == 'POST':
        print("Customer form has been filled:" + str(request.form.to_dict(flat=False)))
        (first, last) = request.form['name'].split(" ", 1) 
        email = request.form['email']
        address = request.form['address']
        city = request.form['city']
        country = request.form['country']
        customer_json = dimebox.createCustomer(email, first, last, address, city, country)
        session['customer'] = customer_json['_id']
        session['client_ip_address'] = client_ip_address
        session['client_user_agent'] = client_user_agent
        session_customer = session.get('customer')
        session_client_ip = session.get('client_ip_address')
        session_client_user = session.get('client_user_agent')
        print(f'Customer stored in session: {session_customer}')
        print(f'client ip stored in session: {session_client_ip}')
        print(f'client user agent stored in session: {session_client_user}')
        customer_table = json2html.convert(json = customer_json, table_attributes="class=\"table is-striped\"")
        return render_template('existingcustomer.html', customer = customer_table)
    return render_template('newcustomer.html')

@app.route('/thankyou/<transaction>', methods=['GET'])
def get_transaction_id(transaction):
    trx_id = transaction
    (client_ip_address, client_user_agent) = websiteVisit()
    print(f"Client User-Agent is: {client_user_agent}")
    params = {
        '_populate':'card+customer'
    }
    # GET transaction, card, customer details
    trx_json = dimebox.getTransaction(trx_id, params)
    print(trx_json)
    trx_table = json2html.convert(json = trx_json, table_attributes="class=\"table is-striped\"")
    trx_link = ui_host + str(trx_json['_id'])
    return render_template('thankyou.html', trx_table = trx_table, transaction = trx_json, trx_link = trx_link)


if __name__ == '__main__':
    app.run()
