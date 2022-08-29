import config
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data import Bar
from alpaca.data.live import CryptoDataStream, StockDataStream
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import LimitOrderRequest, MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from datetime import datetime, timedelta
import talib
import pandas
# no keys required for crypto data
client = CryptoHistoricalDataClient()
wss_client = CryptoDataStream(config.KEY_ID, config.KEY_SECRET)
trading_client = TradingClient(config.KEY_ID, config.KEY_SECRET, paper=True)
# async handler
async def bar_data_handler(data):
    request_params = CryptoBarsRequest(
                        symbol_or_symbols=["BTC/USD"],
                        timeframe=TimeFrame.Minute,
                        start=datetime.now()-timedelta(days=30)
                 )
    bars = client.get_crypto_bars(request_params).df
    rsi = talib.RSI(bars["close"])
    sma = talib.SMA(bars["close"],200)
    up, mid, low = talib.BBANDS(bars["close"])
    price = bars["close"][-1]
    print(f">>> price:{price}, sma:{sma[-1]}, rsi:{rsi[-1]},    bol:{low[-1]} {up[-1]}: ")
    if price > up[-1] and price > sma[-1] and rsi[-1] > 70:
        
        # SELL
        print("SELL")
        market_order_data = MarketOrderRequest(
            symbol="BTC/USD",
            notional=4000,
            side=OrderSide.SELL,
            time_in_force='gtc'
            )
        # Market order
        market_order = trading_client.submit_order(
                order_data=market_order_data
              )
        
    elif price < low[-1] and price < sma[-1] and rsi[-1] < 30:
        # BUY
        print("BUY")
        market_order_data = MarketOrderRequest(
                    symbol="BTC/USD",
                    notional=4000,
                    side=OrderSide.BUY,
                    time_in_force='gtc'
                   )
        # Market order
        market_order = trading_client.submit_order(
                order_data=market_order_data
              )
    else:
        print("HOLD")
wss_client.subscribe_bars(bar_data_handler, "BTC/USD")
wss_client.run()
