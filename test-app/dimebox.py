#input for every transaction:
#   - host
#   - api key
import requests
import json
import os

host = os.environ.get("VERIFONE_HOST")
api_key = os.environ.get("API_KEY")
account = os.environ.get("ACCOUNT")
organisation = os.environ.get("ORGANISATION")

ui_host = host + 'reports/transactions/'
api_host = host + 'v1/'

headers = {
    "Content-Type": "application/json",
    "x-apikey": api_key
}

def createTransaction(card, customer, client_ip_address, client_user_agent):
    # Create transaction json body
    transaction_body = {
        "account": account,
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
    trx_json = trx_req_post.json()
    print(f'POST transaction response: {trx_json}')
    return trx_json

def getTransaction(trx_id, params):
    # GET transaction, card, customer details
    trx_req_get = requests.get(api_host + 'transaction/' + trx_id, params = params, headers = headers)
    trx_json = trx_req_get.json()
    print(f'GET transaction response: {trx_json}')
    return trx_json

def createCustomer(email, first_name, last_name, address, city, postal_code, country):
    customer_body = {
        "organisation": organisation,
        "email_address": email,
        "billing":{
            "first_name": first_name,
            "last_name": last_name,
            "address_1": address,
            "city": city,
            "country_code": country,
            "postal_code": postal_code
        }
    }
    # POST the customer details and capture the response as a json object
    customer_req = requests.post(api_host + 'customer/', headers = headers, json = customer_body)
    customer_json = customer_req.json()
    print(f'POST customer response: {customer_json}')
    return customer_json

def getCustomer(customer_id):
    # GET transaction, card, customer details
    customer_req_get = requests.get(api_host + 'customer/' + customer_id, headers = headers)
    customer_json = customer_req_get.json()
    print(f'GET customer response: {customer_json}')
    return customer_json

def getCard(card_id):
    # GET transaction, card, customer details
    card_req_get = requests.get(api_host + 'card/' + card_id, headers = headers)
    card_json = card_req_get.json()
    print(f'GET card response: {card_json}')
    return card_json

#createTransaction
#getTransaction
#createCustomer
#getCustomer
#getUILink
