import requests
import pandas as pd
import numpy as np
import time
from pathlib import Path

CONFIG = {
    'MAX_GAINERS': 200,
    'MIN_VOLUME_USD': 500_000,  # Higher for memecoins
    'MIN_PRICE_USD': 0.0001,
    'MAX_PRICE_CHANGE_24H': 1000.0,  # Allow huge pumps
    'MIN_PRICE_CHANGE_24H': 10.0,    # Only strong movers
    'REQUIRE_BTC_HEALTHY': True,
    'MIN_BTC_7D_CHANGE': -8.0,
}

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"
CACHE_DIR = Path("cache_momentum")
CACHE_DIR.mkdir(exist_ok=True)

def get_btc_7d_change():
    try:
        r = requests.get(f"{COINGECKO_API_URL}/coins/bitcoin", timeout=10)
        if r.status_code == 200:
            return r.json()['market_data']['price_change_percentage_7d_in_currency']['usd']
    except:
        pass
    return None

def fetch_top_gainers():
    url = f"{COINGECKO_API_URL}/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'price_change_percentage_24h_desc',
        'per_page': CONFIG['MAX_GAINERS'],
        'page': 1,
        'price_change_percentage': '24h'
    }
    try:
        r = requests.get(url, params=params, timeout=20)
        if r.status_code == 200:
            return [c for c in r.json() if c.get('market_cap_rank', 9999) >= 21]
    except:
        pass
    return []

def apply_momentum_filter(coins_data, btc_7d):
    if CONFIG['REQUIRE_BTC_HEALTHY'] and (btc_7d is None or btc_7d < CONFIG['MIN_BTC_7D_CHANGE']):
        print("🛑 BTC unhealthy. Skipping Momentum Ignition.")
        return pd.DataFrame()

    pool = []
    for coin in coins_data:
        symbol = coin['symbol'].upper()
        price_change_24h = coin.get('price_change_percentage_24h')
        volume = coin.get('total_volume')
        price = coin.get('current_price')
        rank = coin.get('market_cap_rank', 9999)

        # Use short-circuit checks to avoid comparing None values
        if not (
            isinstance(price_change_24h, (int, float))
            and CONFIG['MIN_PRICE_CHANGE_24H'] <= price_change_24h <= CONFIG['MAX_PRICE_CHANGE_24H']
            and isinstance(volume, (int, float)) and volume >= CONFIG['MIN_VOLUME_USD']
            and isinstance(price, (int, float)) and price >= CONFIG['MIN_PRICE_USD']
            and rank >= 21
        ):
            continue

        pool.append({
            'TOKEN': symbol,
            'PRICE_CHANGE_24H': price_change_24h,
            'VOLUME_24H': volume,
            'MARKET_CAP_RANK': rank,
            'POOL': 'momentum_ignition'
        })

    if pool:
        df = pd.DataFrame(pool).sort_values('PRICE_CHANGE_24H', ascending=False).head(50)
        print(f"🔥 Momentum Ignition: {len(df)} tokens")
        return df
    return pd.DataFrame()

def save_csv(df, filename):
    df.to_csv(filename, index=False)
    if not df.empty:
        print(f"📁 Saved to {filename}")

if __name__ == "__main__":
    print("🚀 RSPS Momentum Ignition: Raw Momentum Plays")
    btc_7d = get_btc_7d_change()
    print(f"📈 BTC 7d: {btc_7d:.1f}%" if btc_7d else "⚠️ BTC data unavailable")
    gainers = fetch_top_gainers()
    df = apply_momentum_filter(gainers, btc_7d)
    save_csv(df, "rspS_momentum_ignition_pool.csv")