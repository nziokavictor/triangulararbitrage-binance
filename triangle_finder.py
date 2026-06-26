from binance.client import Client
from config import API_KEY, API_SECRET

client = Client(API_KEY, API_SECRET)

# Stablecoins cause fake opportunities - exclude them
STABLECOINS = {
     "TUSD", "USDC", "BUSD", "FDUSD",
    "USDP", "DAI", "USDD", "AEUR",
    "EURI", "BIDR", "IDRT", "USD1",
    "EUR", "U", "RLUSD"
}

def get_all_triangles():
    print("Fetching all pairs from Binance...")
    info = client.get_exchange_info()

    all_pairs = set()
    for s in info["symbols"]:
        if s["status"] == "TRADING":
            all_pairs.add(s["symbol"])

    print(f"Found {len(all_pairs)} active pairs. Building triangles...")

    usdt_coins = set()
    for pair in all_pairs:
        if pair.endswith("USDT"):
            coin = pair.replace("USDT", "")
            if coin not in STABLECOINS:
                usdt_coins.add(coin)

    triangles = []
    usdt_coins = list(usdt_coins)

    for i, coinA in enumerate(usdt_coins):
        for coinB in usdt_coins[i+1:]:
            pair1 = f"{coinA}USDT"
            pair2 = f"{coinB}{coinA}"
            pair3 = f"{coinB}USDT"

            if pair1 in all_pairs and pair2 in all_pairs and pair3 in all_pairs:
                triangles.append((pair1, pair2, pair3))

            pair2_rev = f"{coinA}{coinB}"
            if pair3 in all_pairs and pair2_rev in all_pairs and pair1 in all_pairs:
                triangles.append((pair3, pair2_rev, pair1))

    print(f"Found {len(triangles)} valid triangles to scan!\n")
    return triangles

if __name__ == "__main__":
    triangles = get_all_triangles()
    print("Sample triangles found:")
    for t in triangles[:10]:
        print(f"  {t[0]} → {t[1]} → {t[2]}")
    print(f"  ... and {len(triangles)-10} more")