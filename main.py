import backtrader as bt
import backtrader.feeds as btfeeds
import yfinance as yf
import datetime
import pandas as pd

# Get user input for start time
start_time = input("Enter start time (yyyy-mm-dd): ")

# Get user input for end time
end_time = input("Enter end time (yyyy-mm-dd): ")
# if end_time == "", set end_time to today
if end_time == "":
    end_time = datetime.date.today().strftime("%Y-%m-%d")

# Download the data using yfinance
data_df = yf.download('AAPL', start=start_time, end=end_time)

# Convert the data to backtrader compatible format
data_df.index = pd.to_datetime(data_df.index)
data_df = data_df.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume',
                                  'Adj Close': 'adj_close'})
data_df['openinterest'] = 0


# Create a custom Pandas data feed
class PandasData(btfeeds.PandasData):
    lines = ('adj_close',)
    params = (
        ('datetime', None),
        ('open', -1),
        ('high', -1),
        ('low', -1),
        ('close', -1),
        ('volume', -1),
        ('openinterest', -1),
        ('adj_close', -1),
    )


# Create the data feed
data = PandasData(dataname=data_df)


# The rest of the code remains the same


# Create a custom strategy
class MyStrategy(bt.Strategy):
    params = (
        ('macd_fast', 12),
        ('macd_slow', 26),
        ('macd_signal', 9),
        ('stop_loss', 0.02),
        ('take_profit', 0.05),
        ('printlog', False),
    )

    def __init__(self):
        self.macd, self.macdsignal, self.macdhist = bt.indicators.MACDHisto(fastema=self.params.macd_fast,
                                                                            slowema=self.params.macd_slow,
                                                                            signal=self.params.macd_signal)


    def next(self):
        if self.order:
            return

        if not self.position:
            if self.dataclose[0] > self.ma[0] and self.rsi[0] < 70 and self.macdhist[0] > 0:
                self.order = self.buy()
        else:
            if self.dataclose[0] < self.ma[0] or (
                    self.dataclose[0] - self.position.price) / self.position.price > self.params.stop_loss:
                self.order = self.sell()

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f"BUY EXECUTED, {order.executed.price:.2f}")
            elif order.issell():
                self.log(f"SELL EXECUTED, {order.executed.price:.2f}")

        self.order = None

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f"{dt.isoformat()}, {txt}")


# Create a Cerebro instance
cerebro = bt.Cerebro()

# Add data feed to Cerebro
cerebro.adddata(data)

# Add the custom strategy
cerebro.addstrategy(MyStrategy)

# Set initial cash
cerebro.broker.setcash(100000.0)

# Print out the starting portfolio value
print(f"Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")

# Run the strategy
cerebro.run()

# Print out the final portfolio value
print(f"Final Portfolio Value: {cerebro.broker.getvalue():.2f}")

# Plot the result
cerebro.plot(style='candlestick')

if __name__ == '__main__':
    pass
