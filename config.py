#the apikey and secret key below are of binance testnet that allows you to use virtual money.
# to obtain yo api key and api secret go to binancetesnet.com 

API_KEY = "tJF8Y2XsZ1LGdqF4KM0D0inCO8kLVmzbvYikKjIMWGVR7MDYceo8BlLmpaVDmHql"
API_SECRET = "YzB8NEFb3bVNBlb0eMTqgHbQdBJKWKtpjXtne34enrpHYBzlbvW1wPGVgR7dHGTO"

USE_TESTNET = True   # keeps us on fake money

# Minimum profit % before fees to flag an opportunity
MIN_PROFIT_THRESHOLD = 0.003  # 0.3% (covers fees with a tiny edge)
TRADE_FEE = 0.001  # 0.1%  # Fee per trade (Binance standard)

# Maximum USDT to risk per trade cycle
MAX_TRADE_USDT = 100

#telegram bot 
#this is keys to a telegram bot i created. the telegram bot is to notify me of any activity
TELEGRAM_TOKEN = "8970879593:AAHilALYkrXsuSQ-BqIUz2RdkSze_A6PuBo"
TELEGRAM_CHAT_ID = "5552946379"
