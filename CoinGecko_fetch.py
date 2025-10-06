from pycoingecko import CoinGeckoAPI
import numpy as np
import pandas as pd
from datetime import datetime

# Initialize CoinGecko API client
cg = CoinGeckoAPI()

# List of token IDs (update IDs as needed for missing/ambiguous tokens)
tokens = {
    'AAVE': 'aave',
    'ADA': 'cardano',
    'ALGO': 'algorand',
    'ANKR': 'ankr',
    'APE': 'apecoin',
    'APT': 'aptos',
    'ARB': 'arbitrum',
    'ASR': 'as-roma-fan-token',
    'AVAX': 'avalanche-2',
    'AXS': 'axie-infinity',
    'BCH': 'bitcoin-cash',
    'BGB': 'bitget-token',
    'BNT': 'bancor',
    'BONK': 'bonk',
    'C98': 'coin98',
    'CHZ': 'chiliz',
    'CRO': 'crypto-com-chain',
    'CRV': 'curve-dao-token',
    'CVX': 'convex-finance',
    'DOGE': 'dogecoin',
    'DOT': 'polkadot',
    'DYDX': 'dydx-chain',
    'ENS': 'ethereum-name-service',
    'ETC': 'ethereum-classic',
    'FET': 'fetch-ai',
    'FIL': 'filecoin',
    'FLOKI': 'floki',
    'GALA': 'gala',
    'HBAR': 'hedera-hashgraph',
    'INJ': 'injective-protocol',
    'JASMY': 'jasmycoin',
    'KAS': 'kaspa',
    'KAVA': 'kava',
    'LDO': 'lido-dao',
    'LEO': 'leo-token',
    'LINK': 'chainlink',
    'MANA': 'decentraland',
    'NEAR': 'near',
    'ONDO': 'ondo-finance',
    'PAXG': 'pax-gold',
    'PENDLE': 'pendle',
    'PEPE': 'pepe',
    'REEF': 'reef',
    'SAND': 'the-sandbox',
    'SEI': 'sei-network',
    'SHIB': 'shiba-inu',
    'SUI': 'sui',
    'SXP': 'swipe',
    'UNI': 'uniswap',
    'XLM': 'stellar',
    'XMR': 'monero',
    'XRP': 'ripple',
    'ZRX': '0x'

}

# Function to fetch market cap and circulating supply
def fetch_token_data(token_ids, date=None):
    data = []
    if date:
        # Historical data: fetch one by one (CoinGecko API limitation)
        for name, id in token_ids.items():
            if not id:
                print(f"Warning: No CoinGecko ID for {name}. Skipping.")
                data.append({'name': name, 'id': id, 'market_cap': 0, 'circulating_supply': 0})
                continue
            try:
                response = cg.get_coin_history_by_id(id=id, date=date, localization=False)
                market_cap = response.get('market_data', {}).get('market_cap', {}).get('usd', 0)
                circulating_supply = response.get('market_data', {}).get('circulating_supply', 0)
                data.append({'name': name, 'id': id, 'market_cap': market_cap, 'circulating_supply': circulating_supply})
            except Exception as e:
                print(f"Error fetching {name}: {e}")
                data.append({'name': name, 'id': id, 'market_cap': 0, 'circulating_supply': 0})
    else:
        # Current data: fetch all at once
        ids = ','.join([id for id in token_ids.values() if id])
        try:
            response = cg.get_coins_markets(vs_currency='usd', ids=ids)
            # Map id to data for quick lookup
            id_to_data = {item['id']: item for item in response}
            for name, id in token_ids.items():
                if not id:
                    print(f"Warning: No CoinGecko ID for {name}. Skipping.")
                    data.append({'name': name, 'id': id, 'market_cap': 0, 'circulating_supply': 0})
                    continue
                item = id_to_data.get(id, {})
                market_cap = item.get('market_cap', 0)
                circulating_supply = item.get('circulating_supply', 0)
                data.append({'name': name, 'id': id, 'market_cap': market_cap, 'circulating_supply': circulating_supply})
        except Exception as e:
            print(f"Error fetching current data: {e}")
            for name, id in token_ids.items():
                data.append({'name': name, 'id': id, 'market_cap': 0, 'circulating_supply': 0})
    return data

# Fetch data (remove date for current data)
# For historical (e.g., Feb 23, 2024), set date='23-02-2024'
token_data = fetch_token_data(tokens)

# Compute median market cap
market_caps = [d['market_cap'] for d in token_data if d['market_cap'] > 0]
median_market_cap = np.median(market_caps) if market_caps else 500000000
print(f"Median Market Cap: ${median_market_cap:.2f}")

# Output for Pine Script
print("\nToken Data for Pine Script Input:")
for d in token_data:
    print(f"{d['name']}: Market Cap = ${d['market_cap']:,.2f}, Circulating Supply = {d['circulating_supply']:,.2f}")

# Convert token_data to a DataFrame
df = pd.DataFrame(token_data)

# Save to Excel file
df.to_excel("coingecko_token_data.xlsx", index=False)

print("\nResults saved to coingecko_market_cap.xlsx")