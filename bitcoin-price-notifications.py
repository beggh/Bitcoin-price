from requests import request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import time
from datetime import datetime

BITCOIN_PRICE_THRESHOLD = 36000
#BITCOIN_API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/test/with/key/m-R9I9YI6yw9lytybDH5M'


def get_latest_bitcoin_price():
    parameters = {
        'symbol': 'BTC'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'a4f20e04-f6c0-4d21-9e15-a69d33a9c924',
    }

    session = Session()
    session.headers.update(headers)


    response = session.get(URL, params=parameters)
    data = json.loads(response.text)
    #print(data)
    parseData = json.dumps(response.json())
    #print(parseData)
    btcObj = json.loads(parseData)
    #print(btcObj["data"]["BTC"]["name"])
    #print(btcObj["data"]["BTC"]["quote"]["USD"]["price"])

    ethString = str(btcObj["data"]["BTC"]["quote"]["USD"]["price"])
    #print(ethString)
    return(float(ethString))


def post_ifttt_webhook(event, value):
    data = {'value1': value}
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    # Sends a HTTP POST request to the webhook URL
    request.post(ifttt_event_url, json=data)


def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        # Formats the date into a string: '24.02.2018 15:09'
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
        price = bitcoin_price['price']
        row = '{}: $<b>{}</b>'.format(date, price)
        rows.append(row)
    return '<br>'.join(rows)


def main():
    bitcoin_history = []
    while True:
        price = get_latest_bitcoin_price()
        date = datetime.now()
        bitcoin_history.append({'date': date, 'price': price})

        if price < BITCOIN_PRICE_THRESHOLD:
            post_ifttt_webhook('bitcoin_price_emergency', price)

        if len(bitcoin_history) == 5:
            post_ifttt_webhook('bitcoin_price_update',
                               format_bitcoin_history(bitcoin_history))
            bitcoin_history = []

        time.sleep(1 * 60)



if __name__ == '__main__':
    main()
