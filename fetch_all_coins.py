from pycoingecko import CoinGeckoAPI
import pandas as pd

cg = CoinGeckoAPI()

# Fetch top 200 coins by market cap
top_coins = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page=200, page=1)

# Prepare data
token_data = []
for coin in top_coins:
    token_data.append({
        'name': coin['name'],
        'symbol': coin['symbol'],
        'id': coin['id'],
        'market_cap': coin.get('market_cap', 0),
        'circulating_supply': coin.get('circulating_supply', 0)
    })

# Save to Excel
df = pd.DataFrame(token_data)
df.to_excel("coingecko_top200_market_cap.xlsx", index=False)

print("Saved top 200 coins by market cap to coingecko_top200_market_cap.xlsx")