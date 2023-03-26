# TradeBot: Apple Trading Strategy Comparison
My dad wouldn't stop bragging about how he can out-trade everybody so I decide to **quantitatively** slap his face by building this instead of caching up my 5 weeks worth of ECE259.
This repository contains a set of Python scripts that implement and compare different trading strategies for Apple Inc. (AAPL) stock. The main purpose of this project is to explore various trading algorithms and evaluate their performance against a buy-and-hold strategy in the S&P 500 index.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- Retrieves historical stock price data for Apple Inc. and the S&P 500 index.
- Calculates and applies technical indicators (e.g., moving averages, RSI, and MACD) to the data.
- Implements various trading strategies and iterates over the data to simulate trades.
- Calculates and plots cumulative profit percentages for each strategy.
- Compares the performance of each strategy to the S&P 500 index.

## Installation

To get started with this project, follow these steps:

1. Clone the repository:
    ```angular2html
    git clone https://github.com/your_username/tradebot.git
    ```
2. Create a virtual environment and activate it:
    ```angular2html
    python -m venv venv
    source venv/bin/activate # for Unix-based systems
    venv\Scripts\activate # for Windows
    ```
3. Install the required dependencies:
    ```angular2html
    pip install -r requirements.txt
    ```


## Usage

1. Open the `main.py` file and set the appropriate API key for the data provider.

2. Adjust the trading strategy parameters and the stock data timeframe as needed.

3. Run the `main.py` script:

    ```angular2html
    python main.py
    ```
   

4. Analyze the results by examining the cumulative profit percentage plots and the printed total returns and profits for each strategy.
    ```angular2html
    Enter start time (yyyy-mm-dd): 2022-01-01
    Strategy A Profit: -99.96%
    Strategy B Profit: 0.25%
    Strategy C Profit: -4.38%
    S&P 500 Profit: -17.21%
    ```
    ![Cumulative Profit Percentage Plots](screenshot.png)
## Contributing

We welcome contributions to improve the existing strategies or to add new ones. If you would like to contribute, please follow these steps:

1. Fork the repository.

2. Create a new branch with a descriptive name for your changes:

    ```angular2html
    git checkout -b my_new_feature
    ```

3. Make your changes, commit them, and push the branch to your fork:

    ```angular2html
    git add .
    git commit -m "Added my new feature"
    git push origin my_new_feature
    ```

4. Create a pull request with a clear description of your changes.

## Creating Your Own Trading Strategy

To create your own trading strategy, you need to follow the input and output format requirements. Your custom trading strategy should be implemented as a Python function, which will be used as input to the `compare_strategies` function. Here is a guide on how to create your own trading strategy function:

### Input Format

Your custom trading strategy function should accept the following input parameters:

1. `row`: A Pandas DataFrame row containing the stock data for a specific date, including columns such as 'Open', 'Close', 'High', 'Low', 'Volume', and any additional technical indicators you may want to use.
2. `in_trade`: A boolean value that indicates whether the trade is currently active.
3. `entry_price`: A float representing the entry price of the trade. If no trade is active, this value should be `None`.
4. `exit_price`: A float representing the exit price of the trade. If no trade is active, this value should be `None`.
5. `total_profit`: A float representing the total profit accumulated up to the current row.
6. Any additional parameters representing technical indicators or other data relevant to your trading strategy (e.g., `MA10`, `RSI`, `MACD`).

### Output Format

Your custom trading strategy function should return the following values:

1. `in_trade`: An updated boolean value representing whether the trade is active after the current row.
2. `entry_price`: An updated float representing the entry price of the trade, if a new trade has been initiated. If no trade is active, this value should be `None`.
3. `exit_price`: An updated float representing the exit price of the trade, if a trade has been closed. If no trade is active, this value should be `None`.
4. `total_profit`: An updated float representing the total profit accumulated up to the current row, including any profit or loss from trades executed on the current row.
5. `daily_profit`: A float representing the profit or loss from trades executed on the current row. If no trade has been executed on the current row, this value should be 0.

### Example

Below is an example of a custom trading strategy function:

```python
def custom_trading_strategy(row, in_trade, entry_price, exit_price, total_profit, MA10, RSI, MACD):
    daily_profit = 0

    # Implement your custom trading logic here.
    # You can use the input parameters and any additional indicators as needed.

    return in_trade, entry_price, exit_price, total_profit, daily_profit
```
Once your custom trading strategy function is implemented, you can use it as input to the compare_strategies function, along with any other strategies you'd like to compare:
```angular2html
compare_strategies(apple_data, sp500_data, [custom_trading_strategy, execute_trade_A])
```


## License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for more details.




