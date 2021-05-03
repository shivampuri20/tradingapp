import sqlite3, config
import alpaca_trade_api as tradeapi
import pandas as pd
from datetime import date
from timezone import is_dst
import tulipy
# print(date.datetime.now())
connection = sqlite3.connect(config.DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("""
    select id from strategy where name ="bollinger_bands"
""")

strategy_id=cursor.fetchone()['id']
cursor.execute("""
    select symbol , name
    from stock 
    join stock_strategy  on stock_strategy.stock_id =  stock.id
    where stock_strategy.strategy_id = ?
""", (strategy_id,))

stocks=cursor.fetchall()
symbols=[stock['symbol'] for stock in stocks]
print(symbols)

current_date="2021-04-21"
# current_date=date.today()
print(current_date)
if is_dst():
    start_minute_bar = f"{current_date} 09:30:00-05:00"
    end_minute_bar = f"{current_date} 16:00:00-05:00"
print(start_minute_bar,end_minute_bar)

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)

orders = api.list_orders(status='all',limit=500, after= current_date)
existing_order_symbols = [order.symbol for order in orders if order.status != 'canceled']
print(existing_order_symbols)

for symbol in symbols:
    print(symbol)
    minute_bars = api.get_barset(symbol, '5Min',start=pd.Timestamp(current_date),end=pd.Timestamp(current_date)).df
    print(minute_bars)
    market_open_mask = (minute_bars.index >= start_minute_bar) & (minute_bars.index < end_minute_bar)
    market_open_bars=minute_bars.loc[market_open_mask]
    print(market_open_bars)

    if len(market_open_bars) >=20:
        closes=market_open_bars.columns
        print(closes)

        # bands=tulipy.bbands(closes,20,2)




