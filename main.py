import time
from websocket_feed import start_feed_thread, prices
from triangle_finder import get_all_triangles
from calculator import scan_all
from executor import execute_triangle, get_balance
from telegram_alert import send_startup_alert, send_opportunity_alert, send_trade_result

# Build triangles first
triangles = get_all_triangles()

# Start WebSocket
start_feed_thread(triangles)

print("Waiting for prices to load...")
time.sleep(5)

balance = get_balance('USDT')
print(f"💰 Starting USDT balance: {balance}")
print(f"Scanning {len(triangles)} triangles at WebSocket speed!")
print("=" * 60)

# Send startup alert to Telegram
send_startup_alert(len(triangles))

scan_count = 0
is_executing = False

while True:
    try:
        scan_count += 1
        results = scan_all(triangles, prices)
        results.sort(key=lambda x: x["profit"], reverse=True)

        print(f"\n--- Scan #{scan_count} | {len(results)} triangles checked ---")
        print("Top 5:")
        for r in results[:5]:
            flag = "✅" if r["profitable"] else "  "
            print(f"  {flag} {r['profit']*100:.4f}% | {r['triangle']}")

        # Execute if opportunity found and not already trading
        opportunities = [r for r in results if r["profitable"]]
        if opportunities and not is_executing:
            best = opportunities[0]
            print(f"\n🚨 OPPORTUNITY: {best['profit']*100:.4f}% | {best['triangle']}")

            # Alert Telegram immediately
            send_opportunity_alert(best["triangle"], best["profit"], scan_count)

            is_executing = True
            p1, p2, p3 = best["triangle"].split(" → ")

            # Execute the trade
            usdt_before = get_balance("USDT")
            success = execute_triangle(p1, p2, p3, prices)
            usdt_after = get_balance("USDT")

            actual_profit = usdt_after - usdt_before

            # Send result to Telegram
            send_trade_result(best["triangle"], actual_profit, success)

            is_executing = False

        time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")
        is_executing = False
        time.sleep(5)
        