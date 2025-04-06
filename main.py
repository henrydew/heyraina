
import logging
import requests
import time
from telegram import Bot

# Konfigurasi
TELEGRAM_TOKEN = '7541364901:AAEJTwUsf3ke1O9ZfXinDfRcFgBZFLULfAw'
CHAT_ID = '232604495'
SYMBOL = 'XAUUSD=X'  # Yahoo Finance symbol untuk Gold
RSI_PERIOD = 14
MA_SHORT = 50
MA_LONG = 200
API_URL = f'https://query1.finance.yahoo.com/v8/finance/chart/{SYMBOL}?interval=15m&range=1d'

bot = Bot(token=TELEGRAM_TOKEN)

def get_data():
    try:
        response = requests.get(API_URL)
        data = response.json()
        close_prices = data['chart']['result'][0]['indicators']['quote'][0]['close']
        return [price for price in close_prices if price is not None]
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return []

def calculate_rsi(prices, period=RSI_PERIOD):
    gains = []
    losses = []
    for i in range(1, len(prices)):
        delta = prices[i] - prices[i - 1]
        if delta >= 0:
            gains.append(delta)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(-delta)
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_ma(prices, period):
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period

def check_signal():
    prices = get_data()
    if len(prices) < MA_LONG:
        return "Not enough data."
    rsi = calculate_rsi(prices)
    ma_short = calculate_ma(prices, MA_SHORT)
    ma_long = calculate_ma(prices, MA_LONG)
    current_price = prices[-1]

    if rsi < 30 and ma_short > ma_long:
        return f"RSI: {rsi:.2f} | MA50: {ma_short:.2f} | MA200: {ma_long:.2f}\n**Signal: BUY**"
    elif rsi > 70 and ma_short < ma_long:
        return f"RSI: {rsi:.2f} | MA50: {ma_short:.2f} | MA200: {ma_long:.2f}\n**Signal: SELL**"
    else:
        return f"RSI: {rsi:.2f} | MA50: {ma_short:.2f} | MA200: {ma_long:.2f}\n**Signal: WAIT**"

def main():
    while True:
        signal = check_signal()
        bot.send_message(chat_id=CHAT_ID, text=signal)
        time.sleep(900)  # setiap 15 menit

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
