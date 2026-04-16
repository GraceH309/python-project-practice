import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# 下载股票数据
def download_stock_data(ticker, start="2023-01-01", end=None):
    if end is None:
        end = datetime.today().strftime("%Y-%m-%d")
    data = yf.download(ticker, start=start, end=end)
    return data

# 计算收益率、波动率、均线
def calculate_indicators(data):
    data["Daily Return"] = data["Adj Close"].pct_change()
    data["MA20"] = data["Adj Close"].rolling(window=20).mean()
    data["MA50"] = data["Adj Close"].rolling(window=50).mean()
    volatility = data["Daily Return"].std() * np.sqrt(252)
    return data, volatility

# 可视化
def plot_data(data, ticker):
    plt.figure(figsize=(12,6))
    plt.plot(data["Adj Close"], label="Price")
    plt.plot(data["MA20"], label="MA20")
    plt.plot(data["MA50"], label="MA50")
    plt.title(f"{ticker} Stock Analysis")
    plt.legend()
    plt.show()

# 主程序
if __name__ == "__main__":
    ticker = "AAPL"
    df = download_stock_data(ticker)
    df, vol = calculate_indicators(df)
    print(f"年化波动率: {vol:.2%}")
    print(df.tail())
    plot_data(df, ticker)