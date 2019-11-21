from flask import Flask, jsonify, abort, request, render_template, session
import requests
import os
import json
from json2html import *

app = Flask(__name__, instance_relative_config=True)
# Set secret key for sessions
app.secret_key = os.environ.get("SECRET_KEY")

#Loading default configuration
app.config.from_object('config.default')
# Load the configuration from the instance folder
app.config.from_pyfile('config.py')

host = os.environ.get("VERIFONE_HOST")
api_key = os.environ.get("API_KEY")

ui_host = host + 'reports/transactions/'
api_host = host + 'v1/'

# Set the api header
headers = {
    "Content-Type": "application/json",
    "x-apikey": api_key
}

# Print the host that is used
print(f"Connected to Verifone environment: {host}")

@app.route('/demo', methods=['GET','POST'])
def demo():
    # Get and print client ip address
    client_ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    print(f"Client IP address: {client_ip_address}")
    # Get and print client User-Agent
    client_user_agent = request.headers.get('User-Agent')
    print(f"Client User-Agent is: {client_user_agent}")
    return render_template('demo.html')

@app.route('/newcustomer', methods=['GET','POST'])
def newcustomer():
    # Get and print client ip address
    client_ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    print(f"Client IP address: {client_ip_address}")
    # Get and print client User-Agent
    client_user_agent = request.headers.get('User-Agent')
    print(f"Client User-Agent is: {client_user_agent}")
    if request.method == 'POST':
        print("Customer form has been filled:" + str(request.form.to_dict(flat=False)))
        customer_name = request.form['name'].split(" ", 1)
        customer_email = request.form['email']
        customer_address = request.form['address']
        customer_city = request.form['city']
        customer_country = request.form['country']
        customer_body = {
            "organisation":"5d2eeef0628e0432e2826bff",
            "email_address": customer_email,
            "billing":{
                "first_name": customer_name[0],
                "last_name": customer_name[1],
                "address_1": customer_address,
                "city": customer_city,
                "country_code": customer_country,
                "postal_code": "WA4 5GX"
            }
        }
        # POST the customer details and capture the response as a json object
        customer_req = requests.post(api_host + 'customer/', headers = headers, json = customer_body)
        customer_json = customer_req.json()
        print(customer_json)
        customer_id = customer_json['_id']
        customer_table = json2html.convert(json = customer_json, table_attributes="class=\"table is-striped\"")
        return render_template('existingcustomer.html', customer = customer_table)
    return render_template('newcustomer.html')


@app.route('/thankyou', methods=['POST', 'GET'])
def get_transaction():
    # Get and print client ip address
    client_ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    print(f"Client IP address: {client_ip_address}")
    # Get and print client User-Agent
    client_user_agent = request.headers.get('User-Agent')
    print(f"Client User-Agent is: {client_user_agent}")
    # store the card token in the card variable
    card = request.form.get('card')
    # set up the params variable for getting the trx 
    params = {
        '_populate':'card+customer'
    }
    print(f"The session carried over this token: {card}")
    # The form posts to this end point
    if card and request.method == 'POST':
        # Create customer json body
        customer_body = {
            "organisation":"5d2eeef0628e0432e2826bff",
            "email_address": "john.gilmore@email.com",
            "billing":{
                "first_name": "John",
                "last_name": "Gilmore",
                "address_1": "46 Shore Street",
                "city": "Heath Stockton",
                "country_code": "GB",
                "postal_code": "WA4 5GX"
            }
        }
        # POST the customer details and capture the response as a json object
        customer_req = requests.post(api_host + 'customer/', headers = headers, json = customer_body)
        customer_json = customer_req.json()
        print(customer_json)
        # Create transaction json body
        transaction_body = {
            "account": "5d2efcf2628e0432e2826c6a",
            "amount": 1234,
            "card": card,
            "capture_now": True,
            "customer_ip": client_ip_address,
            "customer": customer_json['_id'],
            "dynamic_descriptor": "Demonstration Test",
            "merchant_reference": "Test Demo",
            "user_agent": client_user_agent,
        }
        # POST transaction request and capture the response as a json object
        trx_req_post = requests.post(api_host + 'transaction', headers = headers, json = transaction_body)
        trx_json_post = trx_req_post.json()
        trx_id = trx_json_post['_id']
        # GET transaction, card, customer details
        trx_req_get = requests.get(api_host + 'transaction/' + trx_id, params = params, headers = headers)
        trx_json = trx_req_get.json()
        print(trx_json)
        trx_table = json2html.convert(json = trx_json, table_attributes="class=\"table is-striped\"")
        trx_link = ui_host + str(trx_json['_id'])
        return render_template('thankyou.html', trx_table = trx_table, transaction = trx_json, trx_link = trx_link)

@app.route('/thankyou/<transaction>', methods=['GET'])
def get_transaction_id(transaction):
    trx_id = transaction
    # Get and print client ip address
    client_ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    print(f"Client IP address: {client_ip_address}")
    # Get and print client User-Agent
    client_user_agent = request.headers.get('User-Agent')
    print(f"Client User-Agent is: {client_user_agent}")
    params = {
        '_populate':'card+customer'
    }
    # GET transaction, card, customer details
    trx_req_get = requests.get(api_host + 'transaction/' + trx_id, params = params, headers = headers)
    trx_json = trx_req_get.json()
    print(trx_json)
    trx_table = json2html.convert(json = trx_json, table_attributes="class=\"table is-striped\"")
    trx_link = ui_host + str(trx_json['_id'])
    return render_template('thankyou.html', trx_table = trx_table, transaction = trx_json, trx_link = trx_link)


if __name__ == '__main__':
    app.run()
