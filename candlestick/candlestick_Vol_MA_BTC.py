import plotly.graph_objects as go
import yfinance
import talib
from plotly.subplots import make_subplots

data = yfinance.download('BTC-USD', period='2y')
print(data.tail())
data['MA200'] = talib.SMA(data.Close, 200) 

fig = make_subplots(specs=[[{"secondary_y": True}]]) 

fig.add_trace(go.Candlestick(
                                     open=data.Open, 
                                     high=data.High,
                                     low=data.Low,
                                     close=data.Close,
                                     name="Daily Candlestick"),
                secondary_y=True)


fig.add_trace(go.Scatter(   y=data.MA200, 
                            line=dict(color='magenta', width=1), 
                            name="Moving Average 200"
                        ),
                 secondary_y=True
            )

fig.add_trace(go.Bar(y=data.Volume, name="Volume"),  secondary_y=False)

fig.layout.yaxis2.showgrid=False
fig.show()

