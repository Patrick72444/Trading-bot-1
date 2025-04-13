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
    quantity = 0.01

    # Obtener el precio actual del mercado
    mark_price = float(client.mark_price(symbol=symbol)['markPrice'])

    if action == 'long':
        client.new_order(symbol=symbol, side='BUY', type='MARKET', quantity=quantity)

        # Orden SL (-0.8%)
        stop_price = round(mark_price * 0.992, 2)
        client.new_order(
            symbol=symbol,
            side='SELL',
            type='STOP_MARKET',
            stopPrice=stop_price,
            closePosition=True
        )

        # Orden TP (+2%)
        take_profit = round(mark_price * 1.02, 2)
        client.new_order(
            symbol=symbol,
            side='SELL',
            type='TAKE_PROFIT_MARKET',
            stopPrice=take_profit,
            closePosition=True
        )

    elif action == 'short':
        client.new_order(symbol=symbol, side='SELL', type='MARKET', quantity=quantity)

        # Orden SL (-0.8%) para short
        stop_price = round(mark_price * 1.008, 2)
        client.new_order(
            symbol=symbol,
            side='BUY',
            type='STOP_MARKET',
            stopPrice=stop_price,
            closePosition=True
        )

        # Orden TP (+2%) para short
        take_profit = round(mark_price * 0.98, 2)
        client.new_order(
            symbol=symbol,
            side='BUY',
            type='TAKE_PROFIT_MARKET',
            stopPrice=take_profit,
            closePosition=True
        )

    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
