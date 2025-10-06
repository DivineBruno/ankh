from pycoingecko import CoinGeckoAPI
import pandas as pd

cg = CoinGeckoAPI()

# Fetch all coins (IDs, symbols, names)
coins = cg.get_coins_list()

# Convert to DataFrame
df = pd.DataFrame(coins)

# Save to Excel
df.to_excel("coingecko_all_coins.xlsx", index=False)

print("Saved all CoinGecko coins and IDs to coingecko_all_coins.xlsx")