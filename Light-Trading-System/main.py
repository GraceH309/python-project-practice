from fastapi import FastAPI, Query
from pydantic import BaseModel
import sqlite3
import pandas as pd
import yfinance as yf
from datetime import datetime

app = FastAPI(title="Light Trading System", version="1.0")
DB_PATH = "trading.db"

# 初始化数据库
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT,
        order_type TEXT,
        price REAL,
        volume INTEGER,
        create_time TEXT
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS position (
        ticker TEXT PRIMARY KEY,
        volume INTEGER,
        avg_price REAL
    )
    ''')
    conn.commit()
    conn.close()

init_db()

# 数据模型
class OrderModel(BaseModel):
    ticker: str
    order_type: str
    price: float
    volume: int

# 同步行情
@app.get("/data/sync", summary="同步股票行情到数据库")
def sync_stock_data(ticker: str = Query("AAPL", description="股票代码")):
    df = yf.download(ticker, period="1y")
    df = df.reset_index()
    conn = sqlite3.connect(DB_PATH)
    df.to_sql(f"stock_{ticker}", conn, if_exists="replace", index=False)
    conn.close()
    return {
        "code": 200,
        "msg": f"{ticker} 行情数据同步完成",
        "data_count": len(df)
    }

# 创建订单
@app.post("/order/create", summary="创建交易订单")
def create_order(order: OrderModel):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute(
        "INSERT INTO orders (ticker, order_type, price, volume, create_time) VALUES (?,?,?,?,?)",
        (order.ticker, order.order_type, order.price, order.volume, now)
    )
    if order.order_type == "buy":
        cur.execute(
            "INSERT OR REPLACE INTO position (ticker, volume, avg_price) VALUES (?,?,?)",
            (order.ticker, order.volume, order.price)
        )
    elif order.order_type == "sell":
        cur.execute(
            "UPDATE position SET volume = volume - ? WHERE ticker = ?",
            (order.volume, order.ticker)
        )
    conn.commit()
    conn.close()
    return {"code": 200, "msg": "订单创建成功", "order": order.dict()}

# 查询持仓
@app.get("/position/list", summary="查询当前持仓")
def get_position():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM position", conn)
    conn.close()
    return df.to_dict(orient="records")

# 查询订单
@app.get("/order/list", summary="查询历史订单")
def get_order():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM orders", conn)
    conn.close()
    return df.to_dict(orient="records")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000