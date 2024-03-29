import plotly.graph_objects as go
import yfinance
import talib

data = yfinance.download('BTC-USD', period='2y')
print(data.tail())
data['MA200'] = talib.SMA(data.Close, 200) 
fig = go.Figure(data=[go.Candlestick(x=data.index,
                                     open=data.Open, 
                                     high=data.High,
                                     low=data.Low,
                                     close=data.Close,
                                     name="Daily Candlestick"),
                                     ])

fig.add_trace(go.Scatter(   x=data.index, 
                            y=data.MA200, 
                            line=dict(color='magenta', width=1), 
                            name="Moving Average 200"
                        )
            )
fig.show()
