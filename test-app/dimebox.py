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
customer = os.environ.get("CUSTOMER")
threeds_authenticator = os.environ.get("AUTHENTICATOR")

ui_host = host + '/reports/transactions/'
api_host = host + '/v1/'

headers = {
    "Content-Type": "application/json",
    "x-apikey": api_key
}

def createTransaction(
    card, 
    capture_now,
    customer, 
    client_ip_address, 
    client_user_agent,
    merchant_reference):
    # Create transaction json body
    transaction_body = {
        "account": account,
        "amount": 1234,
        "card": card,
        "capture_now": capture_now,
        "customer_ip": client_ip_address,
        "customer": customer,
        "dynamic_descriptor": "Demonstration Test",
        "merchant_reference": merchant_reference,
        "user_agent": client_user_agent,
    }
    # POST transaction request and capture the response as a json object
    print(f'POST transaction request: {transaction_body}')
    transaction_req_post = requests.post(api_host + 'transaction', headers = headers, json = transaction_body)
    transaction_json = transaction_req_post.json()
    print(f'POST transaction response: {transaction_json}')
    return transaction_json

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
    print(f'POST request customer: {customer_body}')
    customer_req = requests.post(api_host + '/customer/', headers = headers, json = customer_body)
    customer_json = customer_req.json()
    print(f'POST response customer: {customer_json}')
    return customer_json

def createCheckout(
    account, 
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
    template):
    checkout_body = {
    "account": account,
    "amount": amount,
    "customer": customer,
    "merchant_reference": merchant_reference,
    "return_url": return_url,
    "configurations": {
        "card": {
            "process_transaction": process_transaction,
            "dynamic_descriptor": "VF-001",
            "capture_now": capture_now,
            "threed_secure": {
                "authenticator": threeds_authenticator,
                "enabled": threeds_enabled,
                "currency_code": threeds_currency,
                "transaction_mode": threeds_transaction_mode
            }
        }
    },
    "template": template
    }
    print(f'POST Checkout request: {checkout_body}')
    # POST the customer details and capture the response as a json object
    checkout_req = requests.post(api_host + '/checkout/', headers = headers, json = checkout_body)
    checkout_json = checkout_req.json()
    print(f'POST checkout response: {checkout_json}')
    return checkout_json

def getCustomer(customer_id):
    # GET transaction, card, customer details
    customer_req_get = requests.get(api_host + '/customer/' + customer_id, headers = headers)
    customer_json = customer_req_get.json()
    print(f'GET customer response: {customer_json}')
    return customer_json

def getCard(card_id):
    # GET card details
    card_req_get = requests.get(api_host + '/card/' + card_id, headers = headers)
    card_json = card_req_get.json()
    print(f'GET card response: {card_json}')
    return card_json

def getAuthentication(authentication_id):
    # GET authentication details
    authentication_req_get = requests.get(api_host + '/3d/' + authentication_id, headers = headers)
    authentication_json = authentication_req_get.json()
    print(f'GET authentication response: {authentication_json}')
    return authentication_json

def getTransaction(trx_id, params):
    # GET transaction, card, customer details
    trx_req_get = requests.get(api_host + '/transaction/' + trx_id, params = params, headers = headers)
    trx_json = trx_req_get.json()
    print(f'GET transaction response: {trx_json}')
    return trx_json



#createTransaction
#getTransaction
#createCustomer
#getCustomer
#getUILink
