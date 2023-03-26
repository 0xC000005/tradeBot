# Import necessary libraries
import yfinance as yf
import matplotlib.pyplot as plt
import talib
import datetime
import mplfinance as mpf

# Get user input for start time
start_time = input("Enter start time (yyyy-mm-dd): ")

# Get user input for end time
end_time = input("Enter end time (yyyy-mm-dd): ")
# if end_time == "", set end_time to today
if end_time == "":
    end_time = datetime.date.today().strftime("%Y-%m-%d")

# Download Apple stock data and S&P500 data
apple = yf.Ticker("AAPL")
apple_data = apple.history(start=start_time, end=end_time)

sp500 = yf.Ticker("^GSPC")
sp500_data = sp500.history(start=start_time, end=end_time)

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

# Add columns to store daily profit
apple_data['DailyProfit'] = 0
apple_data['Volume_shifted'] = apple_data['Volume'].shift(1)
sp500_data['DailyProfit'] = 0
apple_data['Trade'] = ""

# The rest of the script remains the same until the end of the '__main__' section

def execute_trade_A(row, in_trade, entry_price, exit_price, total_profit, MA10, RSI, MACD):
    daily_profit = 0

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
        daily_profit = profit
    elif entry_price is not None and ((exit_price is None and abs(row["Close"] - entry_price) / entry_price > 0.02) or (exit_price is not None and (exit_price - entry_price) / entry_price <= 0.02)):
        # Implement stop-loss or take-profit
        in_trade = False
        exit_price = row["Close"];
        profit = exit_price - entry_price
        total_profit += profit
        daily_profit = profit
    elif entry_price is not None and row.name.time() >= datetime.time(15, 30) and row.name.time() <= datetime.time(16, 0):
        # Sell if buying volume is less than selling volume in the last half hour before market close and price is
        # above the 10-day moving average
        if row["Volume"] < row["Volume_shifted"] and row["Close"] > MA10:
            in_trade = False
            exit_price = row["Close"]
            profit = exit_price - entry_price
            total_profit += profit
            daily_profit = profit
        else:
            # Exit trade if condition not met
            in_trade = False
            exit_price = None

    return in_trade, entry_price, exit_price, total_profit, daily_profit



def execute_trade_B(row, in_trade, entry_price, exit_price, total_profit, MA10, RSI, MACD):
    daily_profit = 0

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
        daily_profit = profit / entry_price
    return in_trade, entry_price, exit_price, total_profit, daily_profit


def execute_trade_C(row, in_trade, entry_price, exit_price, total_profit, MA10, RSI, MACD):
    daily_profit = 0

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
        daily_profit = profit / entry_price
    elif entry_price is not None and ((exit_price is None and abs(row["Close"] - entry_price) / entry_price > 0.02) or (exit_price is not None and (exit_price - entry_price) / entry_price <= 0.02)):
        # Implement stop-loss or take-profit
        in_trade = False
        exit_price = row["Close"]
        profit = exit_price - entry_price
        total_profit += profit
        daily_profit = profit / entry_price

    return in_trade, entry_price, exit_price, total_profit, daily_profit


def test_multiple_strategies(execute_trade_functions, labels=None):
    if labels is None:
        labels = [f"Strategy {i}" for i in range(1, len(execute_trade_functions) + 1)]

    # Initialize variables for tracking trades and profits
    profits = []
    for execute_trade_function, label in zip(execute_trade_functions, labels):
        apple_in_trade = False
        apple_entry_price = None
        apple_exit_price = None
        apple_total_profit = 0
        apple_data['DailyProfit'] = 0

        for i, row in apple_data.iterrows():
            apple_in_trade, apple_entry_price, apple_exit_price, apple_total_profit, daily_profit = execute_trade_function(row, apple_in_trade, apple_entry_price, apple_exit_price, apple_total_profit, row["MA10"], row["RSI"], row["MACD"])
            if daily_profit != 0:
                apple_data.at[i, 'DailyProfit'] = daily_profit / apple_entry_price
            else:
                apple_data.at[i, 'DailyProfit'] = 0

        profits.append((1 + apple_data["DailyProfit"]).cumprod() - 1)

    sp500_data['DailyProfit'] = sp500_data['Close'].pct_change()
    sp500_profit = (1 + sp500_data["DailyProfit"]).cumprod() - 1

    plt.figure(figsize=(10, 6))
    for profit, label in zip(profits, labels):
        plt.plot(apple_data.index, profit, label=label)
    plt.plot(sp500_data.index, sp500_profit, label="S&P 500")
    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("Cumulative Profit Percentage")
    plt.title("Comparison of Apple Trading Strategies vs Investing in S&P 500")
    plt.show()

    for i, (profit, label) in enumerate(zip(profits, labels)):
        final_profit = profit.iloc[-1]
        print(f"{label} Profit: {final_profit:.2%}")

    sp500_final_profit = sp500_profit.iloc[-1]
    print(f"S&P 500 Profit: {sp500_final_profit:.2%}")




if __name__ == '__main__':
    test_multiple_strategies([execute_trade_A, execute_trade_B, execute_trade_C],
                             labels=["Strategy A", "Strategy B", "Strategy C"])

    # Plotting the candlestick chart
    plot_data = apple_data.loc[:, ['Open', 'High', 'Low', 'Close', 'Volume']]
    fig, ax = mpf.plot(plot_data, type='candle', style='charles', volume=True, returnfig=True)
    ax[0].set_title("Apple Stock - Candlestick Chart")

    # Indicating opening and closing of each trade day
    for i, row in apple_data.iterrows():
        if row['Trade'] == "Entry":
            ax[0].plot(i, row['Close'], marker='o', color='g', markersize=5)
        elif row['Trade'] == "Exit":
            ax[0].plot(i, row['Close'], marker='o', color='r', markersize=5)

    plt.show()
