import httpx
import pandas as pd
from datetime import datetime

res = httpx.get("https://www.binance.com/api/v3/klines?symbol=BTCUSDT&interval=15m")
data = res.json()
Time = []
Open = []
High = []
Low = []
Close = []
for dt in data:
  Time.append(datetime.utcfromtimestamp((float(dt[0])/1000)+19800).strftime('%Y-%m-%d %H:%M:%S'))
  Open.append(float(dt[1]))
  High.append(float(dt[2]))
  Low.append(float(dt[3]))
  Close.append(float(dt[4]))
candles = {"Time":Time,"Open":Open,"High":High,"Low":Low,"Close":Close}
df = pd.DataFrame(candles)
df['Dema'] = 2 * df.ta.ema(length=15) - df.ta.ema(close=df.ta.ema(length=15),length=15)
df['Upper'] = df.ta.sma(length=20) + (2.0 * df.ta.stdev(length=20))
df['Lower'] = df.ta.sma(length=20) - (2.0 * df.ta.stdev(length=20))
df.ta.stoch(high=df['High'],low=df['Low'],k=9,append=True)
df.ta.sma(close=df['STOCHk_9_3_3'], length=3,append=True)
df.ta.rsi(length=2,append=True)
df['Short'] = (df.Open > df.Close) & (df.Close < df.Dema) & ( (df.High > df.Upper) | (df.High.shift(1) > df.Upper) ) & (df.STOCHk_9_3_3.shift(1) > 65) & ( (df.RSI_2 > 91) | (df.RSI_2.shift(1) > 91) | (df.RSI_2.shift(2) > 91) | (df.RSI_2.shift(1) > 91) )
df['Long'] =  (df.Open < df.Close) & (df.Close > df.Dema) & ( (df.Low < df.Lower) | (df.Low.shift(1) < df.Lower) ) & (df.STOCHk_9_3_3.shift(1) < 35) & ( (df.RSI_2 < 9) | (df.RSI_2.shift(1) < 9) | (df.RSI_2.shift(2) < 9) | (df.RSI_2.shift(3) > 9) )
df[(df.Short == True) | (df.Long ==  True)]
