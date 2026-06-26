from binance.client import Client
from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_MARKET
from config import API_KEY, API_SECRET, USE_TESTNET, MAX_TRADE_USDT

client = Client(API_KEY, API_SECRET, testnet=USE_TESTNET)

def get_balance(asset="USDT"):
    try:
        balance = client.get_asset_balance(asset=asset)
        return float(balance["free"])
    except Exception as e:
        print(f"Balance check error: {e}")
        return 0.0

def get_step_size(symbol):
    try:
        info = client.get_symbol_info(symbol)
        for f in info["filters"]:
            if f["filterType"] == "LOT_SIZE":
                return float(f["stepSize"])
    except:
        return 0.001

def round_quantity(quantity, step_size):
    precision = len(str(step_size).rstrip("0").split(".")[-1])
    return round(quantity, precision)

def all_prices_ready(pair1, pair2, pair3, prices):
    """Check all 3 prices are loaded before attempting trade"""
    ready = (
        pair1 in prices and
        pair2 in prices and
        pair3 in prices and
        prices[pair1]["ask"] > 0 and
        prices[pair2]["ask"] > 0 and
        prices[pair3]["bid"] > 0
    )
    if not ready:
        print(f"⏳ Prices not ready:")
        print(f"   {pair1}: {pair1 in prices}")
        print(f"   {pair2}: {pair2 in prices}")
        print(f"   {pair3}: {pair3 in prices}")
    return ready

def execute_triangle(pair1, pair2, pair3, prices):
    print(f"\n🚀 Executing: {pair1} → {pair2} → {pair3}")

    # Safety check 1 — prices must all be loaded
    if not all_prices_ready(pair1, pair2, pair3, prices):
        print("❌ Aborted — prices not ready")
        return False

    try:
        usdt_balance = get_balance("USDT")
        trade_amount = min(MAX_TRADE_USDT, usdt_balance)

        if trade_amount < 10:
            print("❌ Aborted — not enough USDT balance")
            return False

        print(f"💰 Trading with: {trade_amount} USDT")

        # --- Step 1: USDT → coinA ---
        ask1 = prices[pair1]["ask"]
        step_size1 = get_step_size(pair1)
        qty1 = round_quantity(trade_amount / ask1, step_size1)

        print(f"Step 1: Buying {qty1} of {pair1} at {ask1}")
        order1 = client.order_market_buy(symbol=pair1, quantity=qty1)

        if order1["status"] != "FILLED":
            print(f"❌ Step 1 failed: {order1['status']}")
            return False

        coinA_received = float(order1["executedQty"])
        print(f"  ✅ Received: {coinA_received}")

        # --- Step 2: coinA → coinB ---
        ask2 = prices[pair2]["ask"]
        step_size2 = get_step_size(pair2)
        qty2 = round_quantity(coinA_received / ask2, step_size2)

        print(f"Step 2: Buying {qty2} of {pair2} at {ask2}")
        order2 = client.order_market_buy(symbol=pair2, quantity=qty2)

        if order2["status"] != "FILLED":
            print(f"❌ Step 2 failed — selling back {coinA_received} of {pair1}")
            # Safety: sell coinA back to USDT
            client.order_market_sell(symbol=pair1, quantity=coinA_received)
            return False

        coinB_received = float(order2["executedQty"])
        print(f"  ✅ Received: {coinB_received}")

        # --- Step 3: coinB → USDT ---
        step_size3 = get_step_size(pair3)
        qty3 = round_quantity(coinB_received, step_size3)

        print(f"Step 3: Selling {qty3} of {pair3}")
        order3 = client.order_market_sell(symbol=pair3, quantity=qty3)

        if order3["status"] != "FILLED":
            print(f"❌ Step 3 failed — selling back {coinB_received} of {pair2}")
            # Safety: sell coinB back to coinA, then coinA back to USDT
            client.order_market_sell(symbol=pair2, quantity=coinB_received)
            client.order_market_sell(symbol=pair1, quantity=coinA_received)
            return False

        print(f"  ✅ All 3 steps complete!")
        return True

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False