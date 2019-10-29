from flask import Flask, jsonify, abort, request, render_template
import requests

app = Flask(__name__, instance_relative_config=True)

#Loading default configuration
app.config.from_object('config.default')

# Load the configuration from the instance folder
app.config.from_pyfile('config.py')

# Load the file specified by the APP_CONFIG_FILE environment variable
# Variables defined here will override those in the default configuration
app.config.from_envvar('APP_CONFIG_FILE')

host = app.config["VERIFONE_HOST"]
ui_host = host + 'reports/transactions/'
api_host = host + 'v1/'
api_key = app.config["API_KEY"]

@app.route('/demo', methods=['GET','POST'])
def demo():
    if request.method == 'POST':
        card_id = request.form.get('card')
        print(card_id)
        headers = {
            "Content-Type": "application/json",
            "x-apikey": api_key
        }
        print(host)
        card_req = requests.get(api_host + 'card/' + card_id, headers=headers)
        card_json = card_req.json()
        print(card_json)
        body = {
            "account": "5d2efcf2628e0432e2826c6a",
            "amount": 1234,
            "card": card_id,
            "capture_now": True,
            "customer_ip": "81.205.51.143",
            "dynamic_descriptor": "Demonstration Test",
            "merchant_reference": "Test Demo",
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15",
        }
        trx_req = requests.post(api_host + 'transaction', headers = headers, json = body)
        trx_json=trx_req.json()
        print(trx_json)
        trx_link=ui_host + str(trx_json['_id'])
        return render_template('thankyou.html', api_host = api_host, card = card_json, transaction = trx_json, trx_link = trx_link)
    return render_template('home.html')


@app.route('/get_card', methods=['POST', 'GET'])
def receive_card():
    req_data = request.args.get('card')
    return '''<h1>The language value is: {}</h1>'''.format(req_data)

if __name__ == '__main__':
    app.run(debug=True)
