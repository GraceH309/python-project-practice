import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 数据加载
class DataLoader:
    @staticmethod
    def get_data(ticker, start, end):
        df = yf.download(ticker, start=start, end=end)
        df = df.dropna()
        return df

# 指标计算
class Indicator:
    @staticmethod
    def add_tech_indicators(df):
        df["MA5"] = df["Adj Close"].rolling(5).mean()
        df["MA20"] = df["Adj Close"].rolling(20).mean()
        df["Return"] = df["Adj Close"].pct_change()
        df["CumReturn"] = (1 + df["Return"]).cumprod()
        return df

# 策略基类
class BaseStrategy:
    def generate_signal(self, df):
        raise NotImplementedError("请实现具体策略")

class DualMAStrategy(BaseStrategy):
    def generate_signal(self, df):
        df["Signal"] = 0
        df.loc[(df["MA5"] > df["MA20"]) & (df["MA5"].shift(1) <= df["MA20"].shift(1)), "Signal"] = 1
        df.loc[(df["MA5"] < df["MA20"]) & (df["MA5"].shift(1) >= df["MA20"].shift(1)), "Signal"] = -1
        return df

# 回测引擎
class BacktestEngine:
    def __init__(self, df, signal_col="Signal", init_capital=100000, fee=0.0003):
        self.df = df
        self.signal_col = signal_col
        self.init_capital = init_capital
        self.fee = fee
        self.capital = init_capital
        self.position = 0
        self.df["Position"] = 0
        self.df["Asset"] = init_capital

    def run(self):
        for i in range(1, len(self.df)):
            sig = self.df.iloc[i][self.signal_col]
            ret = self.df.iloc[i]["Return"]
            if sig == 1 and self.position == 0:
                self.position = 1
                self.capital *= (1 - self.fee)
            elif sig == -1 and self.position == 1:
                self.position = 0
                self.capital *= (1 - self.fee)
            if self.position == 1:
                self.capital *= (1 + ret)
            self.df.iloc[i, self.df.columns.get_loc("Position")] = self.position
            self.df.iloc[i, self.df.columns.get_loc("Asset")] = self.capital
        return self.df

# 绩效分析
class Performance:
    @staticmethod
    def calc_metrics(df, annual=252):
        asset = df["Asset"]
        ret_series = asset.pct_change().dropna()
        total_ret = asset.iloc[-1] / asset.iloc[0] - 1
        annual_ret = (1 + total_ret) ** (annual / len(df)) - 1
        vol = ret_series.std() * np.sqrt(annual)
        sharpe = annual_ret / vol if vol != 0 else 0
        rolling_max = asset.cummax()
        drawdown = (asset - rolling_max) / rolling_max
        max_dd = drawdown.min()
        metrics = {
            "总收益率": f"{total_ret:.2%}",
            "年化收益率": f"{annual_ret:.2%}",
            "年化波动率": f"{vol:.2%}",
            "夏普比率": f"{sharpe:.2f}",
            "最大回撤": f"{max_dd:.2%}"
        }
        return metrics, drawdown

# 绘图
def plot_backtest(df):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    ax1.plot(df["Adj Close"], label="Price")
    ax1.plot(df["MA5"], label="MA5")
    ax1.plot(df["MA20"], label="MA20")
    ax1.scatter(df[df["Signal"] == 1].index, df.loc[df["Signal"] == 1, "Adj Close"],
                marker="^", c="g", s=60, label="Buy")
    ax1.scatter(df[df["Signal"] == -1].index, df.loc[df["Signal"] == -1, "Adj Close"],
                marker="v", c="r", s=60, label="Sell")
    ax1.set_title("Price & Trade Signal")
    ax1.legend()
    ax2.plot(df["Asset"], label="Total Asset", c="orange")
    ax2.set_title("Account Net Asset")
    ax2.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    loader = DataLoader()
    data_df = loader.get_data("AAPL", start="2022-01-01", end="2026-01-01")
    data_df = Indicator.add_tech_indicators(data_df)
    strategy = DualMAStrategy()
    data_df = strategy.generate_signal(data_df)
    bt = BacktestEngine(data_df)
    result_df = bt.run()
    metrics, _ = Performance.calc_metrics(result_df)
    print("===== 回测绩效指标 =====")
    for k, v in metrics.items():
        print(f"{k}: {v}")
    plot_backtest(result_df)