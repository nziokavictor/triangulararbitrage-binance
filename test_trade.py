from executor import execute_triangle, get_balance
from telegram_alert import send_trade_result
from websocket_feed import start_feed_thread, prices
from triangle_finder import get_all_triangles
import time

print("Loading live prices...")
triangles = get_all_triangles()
start_feed_thread(triangles)

# Wait until all prices are loaded
print("Waiting for all prices to load", end="")
for i in range(15):
    time.sleep(1)
    print(".", end="", flush=True)
print(" ready!\n")

# Check starting balance
balance_before = get_balance("USDT")
print(f"💰 Balance before: {balance_before} USDT")

# Use a simple well known triangle
TEST_TRIANGLE = ("BTCUSDT", "ETHBTC", "ETHUSDT")
p1, p2, p3 = TEST_TRIANGLE

print(f"\n🧪 Testing: {p1} → {p2} → {p3}")
print(f"Prices ready: {p1 in prices}, {p2 in prices}, {p3 in prices}")

# Execute
success = execute_triangle(p1, p2, p3, prices)

# Final result
balance_after = get_balance("USDT")
actual_profit = balance_after - balance_before

print(f"\n📊 Results:")
print(f"  Before : {balance_before:.4f} USDT")
print(f"  After  : {balance_after:.4f} USDT")
print(f"  Profit : {actual_profit:.4f} USDT")

send_trade_result(f"{p1} → {p2} → {p3}", actual_profit, success)