from config import TRADE_FEE, MIN_PROFIT_THRESHOLD

def check_triangle(pair1, pair2, pair3, prices):
    try:
        ask1 = prices[pair1]["ask"]
        ask2 = prices[pair2]["ask"]
        bid3 = prices[pair3]["bid"]

        if ask1 == 0 or ask2 == 0 or bid3 == 0:
            return None

        fee = 1 - TRADE_FEE
        step1 = (1 / ask1) * fee
        step2 = (step1 / ask2) * fee
        step3 = (step2 * bid3) * fee

        return round(step3 - 1, 6)

    except KeyError:
        return None  # price not yet received for this pair

def scan_all(triangles, prices):
    results = []
    for (p1, p2, p3) in triangles:
        profit = check_triangle(p1, p2, p3, prices)
        if profit is not None:
            results.append({
                "triangle": f"{p1} → {p2} → {p3}",
                "profit": profit,
                "profitable": profit > MIN_PROFIT_THRESHOLD
            })
    return results