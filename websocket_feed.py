import json
import threading
from websocket import WebSocketApp
from triangle_finder import get_all_triangles

# This dictionary holds the latest prices in memory
# Updated instantly whenever Binance sends a price change
prices = {}
triangles = []

def on_message(ws, message):
    data = json.loads(message)
    if "data" in data:
        ticker = data["data"]
        symbol = ticker["s"]          # e.g. "BTCUSDT"
        prices[symbol] = {
            "ask": float(ticker["a"]),  # best sell price
            "bid": float(ticker["b"])   # best buy price
        }

def on_error(ws, error):
    print(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed. Reconnecting...")
    start_feed()

def on_open(ws):
    print("✅ WebSocket connected! Receiving live prices...")

def build_stream_url(triangles):
    # Collect all unique pairs across all triangles
    unique_pairs = set()
    for (p1, p2, p3) in triangles:
        unique_pairs.add(p1.lower())
        unique_pairs.add(p2.lower())
        unique_pairs.add(p3.lower())

    # Build Binance stream URL for all pairs at once
    streams = "/".join([f"{p}@bookTicker" for p in unique_pairs])
    url = f"wss://stream.binance.com:9443/stream?streams={streams}"
    print(f"Subscribing to {len(unique_pairs)} price streams...")
    return url

def start_feed(triangles):
    url = build_stream_url(triangles)
    ws = WebSocketApp(
        url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )
    ws.run_forever()

def start_feed_thread(triangles):
    thread = threading.Thread(target=start_feed, args=(triangles,), daemon=True)
    thread.start()
    return thread

