from flask import Flask, request
from binance.um_futures import UMFutures
import os

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

client = UMFutures(key=API_KEY, secret=API_SECRET)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    symbol = data['symbol']
    action = data['action']

    if action == 'long':
        client.new_order(symbol=symbol, side='BUY', type='MARKET', quantity=0.01)
    elif action == 'short':
        client.new_order(symbol=symbol, side='SELL', type='MARKET', quantity=0.01)

    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
