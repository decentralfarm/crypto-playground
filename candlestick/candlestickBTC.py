import plotly.graph_objects as go
import yfinance

data = yfinance.download('BTC-USD', period='2y')
print(data.tail())

fig = go.Figure(data=[go.Candlestick(x=data.index,
                                     open=data.Open, 
                                     high=data.High,
                                     low=data.Low,
                                     close=data.Close)
                                     ])
fig.show()
