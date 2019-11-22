#input for every transaction:
#   - host
#   - api key
import requests
import json
import os

host = os.environ.get("VERIFONE_HOST")
api_key = os.environ.get("API_KEY")

ui_host = host + 'reports/transactions/'
api_host = host + 'v1/'

headers = {
    "Content-Type": "application/json",
    "x-apikey": api_key
}

def createTransaction(card, customer, client_ip_address, client_user_agent):
    # Create transaction json body
    transaction_body = {
        "account": "5d2efcf2628e0432e2826c6a",
        "amount": 1234,
        "card": card,
        "capture_now": True,
        "customer_ip": client_ip_address,
        "customer": customer,
        "dynamic_descriptor": "Demonstration Test",
        "merchant_reference": "Test Demo",
        "user_agent": client_user_agent,
    }
    # POST transaction request and capture the response as a json object
    trx_req_post = requests.post(api_host + 'transaction', headers = headers, json = transaction_body)
    trx_json_post = trx_req_post.json()
    trx_id = trx_json_post['_id']
    return trx_id

def getTransaction(trx_id, params):
    # GET transaction, card, customer details
    trx_req_get = requests.get(api_host + 'transaction/' + trx_id, params = params, headers = headers)
    trx_json = trx_req_get.json()
    return trx_json

def createCustomer(email, first_name, last_name, address, city, country):
    customer_body = {
        "organisation":"5d2eeef0628e0432e2826bff",
        "email_address": email,
        "billing":{
            "first_name": first_name,
            "last_name": last_name,
            "address_1": address,
            "city": city,
            "country_code": country,
            "postal_code": "WA4 5GX"
        }
    }
    # POST the customer details and capture the response as a json object
    customer_req = requests.post(api_host + 'customer/', headers = headers, json = customer_body)
    customer_json = customer_req.json()
    customer_id = customer_json['_id']
    return customer_id, customer_json

#createTransaction
#getTransaction
#createCustomer
#getCustomer
#getUILink
