from flask import Flask, jsonify, abort, request, render_template
import requests
import os
import json
from json2html import *

app = Flask(__name__, instance_relative_config=True)

#Loading default configuration
app.config.from_object('config.default')
# Load the configuration from the instance folder
app.config.from_pyfile('config.py')

host = os.environ.get("VERIFONE_HOST")
api_key = os.environ.get("API_KEY")

ui_host = host + 'reports/transactions/'
api_host = host + 'v1/'

@app.route('/demo', methods=['GET','POST'])
def demo():
    client_ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    if request.method == 'POST':
        # Get card
        card_id = request.form.get('card')
        print(card_id)
        headers = {
            "Content-Type": "application/json",
            "x-apikey": api_key
        }
        print(host)
        card_req = requests.get(api_host + 'card/' + card_id, headers=headers)
        card_json = card_req.json()
        card_table = json2html.convert(json = card_json, table_attributes="class=\"table is-striped\"")
        print(card_json)
        # Create customer
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
        customer_req = requests.post(api_host + 'customer/', headers = headers, json = customer_body)
        customer_json = customer_req.json()
        customer_table = json2html.convert(json = customer_json, table_attributes="class=\"table is-striped\"")
        print(customer_json)
        # Create transaction
        transaction_body = {
            "account": "5d2efcf2628e0432e2826c6a",
            "amount": 1234,
            "card": card_id,
            "capture_now": True,
            "customer_ip": client_ip_address,
            "customer": customer_json['_id'],
            "dynamic_descriptor": "Demonstration Test",
            "merchant_reference": "Test Demo",
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15",
        }
        trx_req = requests.post(api_host + 'transaction', headers = headers, json = transaction_body)
        trx_json = trx_req.json()
        trx_table = json2html.convert(json = trx_json, table_attributes="class=\"table is-striped\"")
        print(trx_json)
        trx_link = ui_host + str(trx_json['_id'])
        return render_template('thankyou.html', api_host = api_host, card_table = card_table, card = card_json, transaction_table = trx_table, transaction = trx_json, customer_table = customer_table, customer = customer_json, trx_link = trx_link)
    return render_template('demo.html')


@app.route('/get_card', methods=['POST', 'GET'])
def receive_card():
    req_data = request.args.get('card')
    return '''<h1>The language value is: {}</h1>'''.format(req_data)

if __name__ == '__main__':
    app.run(debug=True)
