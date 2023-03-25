import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import talib
import datetime

# Get user input for start time
start_time = input("Enter start time (yyyy-mm-dd): ")

# Download Apple stock data and S&P500 data
apple = yf.Ticker("AAPL")
apple_data = apple.history(start=start_time)

sp500 = yf.Ticker("^GSPC")
sp500_data = sp500.history(start=start_time)

# Calculate MA10, RSI, and MACD for Apple stock
apple_data["MA10"] = apple_data["Close"].rolling(window=10).mean()
apple_data["RSI"] = talib.RSI(apple_data["Close"], timeperiod=14)
macd, macdsignal, macdhist = talib.MACD(apple_data["Close"], fastperiod=12, slowperiod=26, signalperiod=9)
apple_data["MACD"] = macdhist

# Calculate MA10 for S&P500
sp500_data["MA10"] = sp500_data["Close"].rolling(window=10).mean()

# Initialize variables for tracking trades and profits
apple_in_trade = False
apple_entry_price = None
apple_exit_price = None
apple_total_profit = 0

sp500_in_trade = False
sp500_entry_price = None
sp500_exit_price = None
sp500_total_profit = 0


# Define function to execute trades based on the strategy
def execute_trade(row, in_trade, entry_price, exit_price, total_profit, MA10, RSI, MACD):
    if row["Close"] > MA10 and not in_trade and RSI < 70 and MACD > 0:
        # Enter trade
        in_trade = True
        entry_price = row["Close"]
    elif row["Close"] < MA10 and in_trade:
        # Exit trade
        in_trade = False
        exit_price = row["Close"]
        profit = exit_price - entry_price
        total_profit += profit
    elif entry_price is not None and ((exit_price is None and abs(row["Close"] - entry_price) / entry_price > 0.02) or (
            exit_price is not None and (exit_price - entry_price) / entry_price <= 0.02)):
        # Implement stop-loss or take-profit
        in_trade = False
        exit_price = row["Close"]
        profit = exit_price - entry_price
        total_profit += profit
    elif entry_price is not None and row.name.time() >= datetime.time(15, 30) and row.name.time() <= datetime.time(16, 0):
        # Sell if buying volume is less than selling volume in the last half hour before market close and price is
        # above the 10-day moving average
        if row["Volume"] < apple_data["Volume"].iloc[i - 1] and row["Close"] > MA10:
            in_trade = False
            exit_price = row["Close"]
            profit = exit_price - entry_price
            total_profit += profit
        else:
            # Exit trade if condition not met
            in_trade = False
            exit_price = None
    return in_trade, entry_price, exit_price, total_profit


# Execute trades for each row in the data for Apple
for i, row in apple_data.iterrows():
    apple_in_trade, apple_entry_price, apple_exit_price, apple_total_profit = execute_trade(row, apple_in_trade, apple_entry_price, apple_exit_price, apple_total_profit, row["MA10"], row["RSI"], row["MACD"])

# Buy S&P500 at the beginning and hold until the end
sp500_entry_price = sp500_data["Close"][0]
sp500_exit_price = sp500_data["Close"][-1]
sp500_total_profit = sp500_exit_price - sp500_entry_price

# Calculate total return for Apple stock and S&P500
apple_return = (apple_data["Close"][-1] - apple_data["Close"][0]) / apple_data["Close"][0]
sp500_return = (sp500_data["Close"][-1] - sp500_data["Close"][0]) / sp500_data["Close"][0]

# Calculate cumulative profit for Apple and S&P500
apple_cumulative_profit = apple_total_profit / apple_data["Close"][0]
sp500_cumulative_profit = sp500_total_profit / sp500_data["Close"][0]

# Create a plot of the profits for the two strategies
plt.plot(apple_data.index, apple_cumulative_profit, label="Apple Strategy")
plt.plot(sp500_data.index, sp500_cumulative_profit * np.ones_like(sp500_data["Close"]), label="S&P500")
plt.legend()
plt.xlabel("Date")
plt.ylabel("Normalized Profit Percentage")
plt.title("Comparison of Apple Trading Strategy vs Investing in S&P500")
plt.show()

# Print the total return and profit for both strategies
print("Apple Profit: {:.2%}".format(apple_cumulative_profit))
print("S&P500 Profit: {:.2%}".format(sp500_cumulative_profit))




if __name__ == '__main__':
    pass
