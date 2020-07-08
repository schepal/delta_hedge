# Deribit Delta-Hedger
### Disclaimer: This tool is only for demonstration purposes and is not financial advice. Use at your own risk.

A rebalancing tool to delta-hedge a portfolio of cryptocurrency options on Deribit Exchange. 

## Overview

Delta-hedging is a technique which removes a trader’s exposure to directional moves in the underlying asset. Traders who delta-hedge their portfolios are not concerned about the ***price*** of an asset going up or down, rather their focus is on how the ***volatility*** of an asset changes based on their option position. 

If a trader were to identify a mis-pricing of volatility for a particular option, they can buy or sell the option and then delta-hedge this position to remove any price exposure. Many volatility traders constantly monitor their portfolio delta and rebalance accordingly when the exposure becomes too large.

To avoid having to constantly watch open positions, this tool calculates the portfolio delta every 30 seconds and automatically rebalances in the case a delta threshold level is breached. The portfolio is delta-hedged using the chosen asset’s perpetual futures contract on Deribit. 

## Function Parameters
- `api_id` (string): The ID can be found under API management under account settings on the Deribit website.
- `api_secret` (string): The secret can be found under API management under account settings on the Deribit website.  
- `symbol` (string): The asset you wish to delta-hedge. Currently only "BTC" and "ETH" are supported with the default value set to "BTC".
- `threshold` (float): The maximum absolute value of delta exposure to have at any given time. The default value is currently 10% which means the portfolio delta will fluctuate between -10% to 10%. Any breach beyond this level will result in the portfolio being delta-hedged.

## Example
In the example below, the script is setup to delta-hedge Bitcoin (BTC) exposures and rebalance the portfolio in case the delta exceeds +/- 10%. 
``` python
>>> import delta_hedge
>>> id = "replace_this_with_id" # replace your `api_id` in the quotes
>>> secret = "replace_this_with_secret" # replace your `api_secret` in the quotes
>>> dh = delta_hedge.Hedge(api_id=id, api_secret=secret, symbol="BTC", threshold=0.10)

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
Rebalancing trade to achieve delta-neutral portfolio: sell 0.1000 BTC
No need to hedge. Current portfolio delta: 0.0055
No need to hedge. Current portfolio delta: 0.0073
'''
```
## Installation of dependencies
Run the following command in terminal to install all of the required packages. Users will likely experience errors if they install a different version of the `CCXT` library compared to the version listed in `requirements.txt`.

```
pip install -r requirements.txt
```
