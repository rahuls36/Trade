import websocket
import redis
import json
import sqlite3
import os

# Redis Connection and Socket,Symbols Configuration
redis_conn = redis.Redis(host='redis')
socket = "wss://api.hitbtc.com/api/2/ws"
Symbols = []
updated = False

def get_symbols_from_db():
    print("This is called")
    db_location = os.getcwd() + "/db.sqlite3"
    conn = sqlite3.connect(db_location)
    cursor = conn.cursor()
    cursor.execute("Select name from Trade_symbol")
    for symb in cursor.fetchall():
        if symb[0] not in Symbols:
            Symbols.append(symb[0])
            global updated
            updated = True


def on_open(ws):
    """
    Callback Function invoked when a socket connection is established
    :param ws: The Websocket
    :return: None
    """
    print("Connection to Web Socket Successful")
    get_symbols_from_db()
    global updated
    updated = False
    for symbol in Symbols:
        request = {"method": "subscribeTicker", "params": {"symbol": symbol}, "id": 123}
        ws.send(json.dumps(request))


def on_message(ws, message):
    """
    Callback Function Invoked when data is received and Stores the latest Ticker for Configured Symbol data in redis
    :param ws: The websocket
    :param message: The data received on the websocket
    :return: None
    """
    get_symbols_from_db()
    print(Symbols)
    if updated:
        on_open(ws)
    trade_data = json.loads(message).get("params")
    if trade_data:
        symbol = trade_data.pop("symbol")
        trade_data.pop('volume'), trade_data.pop('volumeQuote'), trade_data.pop('timestamp')
        redis_conn.hmset(symbol, trade_data)


# Create the websocket Connection
ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)
ws.run_forever()  # Listens Indefinitely on the web socket
