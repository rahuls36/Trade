import websocket
import redis
import json

# Redis Connection and Socket,Symbols Configuration
redis_conn = redis.Redis(host='redis')
socket = "wss://api.hitbtc.com/api/2/ws"
Symbols = ["ETHBTC", "BTCUSD"]


def on_open(ws):
    """
    Callback Function invoked when a socket connection is established
    :param ws: The Websocket
    :return: None
    """
    print("Connection to Web Socket Successful")
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
    trade_data = json.loads(message).get("params")
    if trade_data:
        symbol = trade_data.pop("symbol")
        trade_data.pop('volume'), trade_data.pop('volumeQuote'), trade_data.pop('timestamp')
        redis_conn.hmset(symbol, trade_data)


# Create the websocket Connection
ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)
ws.run_forever()  # Listens Indefinitely on the web socket
