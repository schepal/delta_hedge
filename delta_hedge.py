import numpy as np
import ccxt
import time

class Hedge:
    def __init__(self, api_id, api_secret, symbol, threshold):
        """
        Initializing Hedge class.
        Parameters
        ----------
        api_id: string
            The `api_id` can be found under API management under account settings.
        api_secret: string
            The `api_secret` can be found under API management under account settings.
        symbol: string (default "BTC")
            The asset you wish to delta-hedge. Currently only "BTC" and "ETH" are supported.
        threshold: float (default 10%)
            The maximum absolute value of delta exposure to have at any given time. The default
            value is currently 10% meaning a portfolio will have maximum of 10% positive or negative
            delta at any given time before being delta-hedged to 0%.

        Example
        ---------
        >>> import delta_hedge
        >>> api_id = "..." # replace your `api_id` in the quotes
        >>> api_secret = "..." # replace your `api_secret` in the quotes
        >>> dh = delta_hedge.Hedge(api_id, api_secret, "BTC", 0.05)
        """
        self.api_id = api_id
        self.api_secret = api_secret
        self.load = ccxt.deribit({'apiKey':name, 'secret':secret})
        self.symbol = symbol
        self.threshold = abs(float(threshold))

        if ((self.symbol != 'BTC') and (self.symbol !='ETH')):
            raise ValueError("Incorrect symbol - please choose between 'BTC' or 'ETH'")

    def current_delta(self):
        """
        Retrives the current portfolio delta.

        Example
        ---------
        >>> dh.current_delta()
        0.065 # portfolio delta is 6.5%
        """
        return self.load.fetch_balance({'currency': str(self.symbol)})['info']['result']['delta_total']

    def delta_hedge(self):
        """
        Rebalances entire portfolio to be delta-neutral based on current delta exposure.
        """
        current_delta = self.current_delta()
        # if delta is negative, we must BUY futures to hedge our negative delta
        if current_delta < 0:
            sign = 'buy'
        # if delta is positive, we must SELL futures to hedge our positive delta
        if current_delta > 0:
            sign = 'sell'
        # retrieve the average price of the perpetual future contract for the asset
        avg_price = np.mean(self.load.fetch_ohlcv(str(self.symbol)+"-PERPETUAL", limit=10)[-1][1:5])
        # if the absolute delta exposure is greater than our threshold then we place a hedging trade
        if abs(current_delta) >= self.threshold:
            asset = str(self.symbol) + "-PERPETUAL"
            order_size = abs(current_delta*avg_price)
            self.load.create_market_order(asset, sign, order_size)
            print("Rebalancing trade to achieve delta-neutral portfolio:", str(sign), str(order_size/avg_price), str(self.symbol))
        else:
            pass
            print("No need to hedge. Current portfolio delta:", current_delta)

    def run_loop(self):
        """
        Runs the delta-hedge script in continuous loop.
        """
        while True:
            try:
                self.delta_hedge()
                time.sleep(30)
            except:
                print("Script is broken - trying again in 30 seconds. Current Delta:", self.current_delta())
                time.sleep(30)
                pass
