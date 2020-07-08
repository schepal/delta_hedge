# Deribit Delta-Hedger
**Disclaimer: This tool is only for demonstration purposes and is not financial advice. Use at your own risk.**

A rebalancing tool to delta-hedge a portfolio of cryptocurrency options on Deribit Exchange. The portfolio delta is calculated every 30 seconds and automatically rebalances in the case a chosen delta threshold level is breached. In this case, the portfolio is delta-hedged using the chosen asset’s perpetual futures contract on Deribit. 

## Overview

Delta-hedging is a technique which removes a trader’s exposure to directional moves in the underlying asset. Traders who delta-hedge their portfolios are not concerned about the ***price*** of an asset going up or down, rather their focus is on how the ***volatility*** of an asset changes based on their option position. 

If a trader were to identify a mis-pricing of volatility for a particular option, they can buy or sell the option and then delta-hedge this position to remove any price exposure. Many volatility traders constantly monitor their portfolio delta and rebalance accordingly when the exposure becomes too large.

## Example
In the example below, the script is setup to delta-hedge Bitcoin (BTC) options and rebalance the portfolio in the case the delta exceeds +/- 10%. 
``` python
>>> import delta_hedge
>>> api_id = "replace_this_with_id" # replace your `api_id` in the quotes
>>> api_secret = "replace_this_with_secret" # replace your `api_secret` in the quotes
>>> dh = delta_hedge.Hedge(api_id, api_secret, "BTC", 0.10)

# Get current total portfolio delta exposure for the chosen asset
>>> dh.current_delta()
0.065

# Run continuous delta-hedging. Terminal log example shown below:
>>> dh.run_loop()
'''
No need to hedge. Current portfolio delta: 0.0122
No need to hedge. Current portfolio delta: 0.0136
No need to hedge. Current portfolio delta: 0.0224
No need to hedge. Current portfolio delta: 0.0163
No need to hedge. Current portfolio delta: 0.0536
# When delta rises above threshold (0.10 in this case)
Rebalancing trade to achieve delta-neutral portfolio: sell 0.4996 ETH
No need to hedge. Current portfolio delta: 0.0055
No need to hedge. Current portfolio delta: 0.0073
'''
```
## Installation of dependencies
Run the following command in terminal to install all of the required packages. Users will likely experience errors if they install a different version of `CCXT` from the exact version listed in the requirements.txt file.

```
pip install -r requirements.txt
```
