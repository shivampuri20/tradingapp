import sqlite3, config
import alpaca_trade_api as tradeapi
import datetime as date

connection = sqlite3.connect(config.DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("""
    select id from strategy where name ="opening_range_breakout"
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


api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)
current_date="2021-03-11"
# current_date=date.datetime.today().isoformat()
# print(current_date)
start_minute_bar=f"{current_date} 09:30:00-04:00 "
end_minute_bar=f"{current_date} 09:45:00-04:00"
print(start_minute_bar,end_minute_bar)
for symbol in symbols:
    minute_bar = api.get_barset(symbol, 'minute', "", start=current_date,end=current_date).df
    print(symbols)
    print(minute_bar.index)
    # opening_range_mask=(minute_bar.index >= start_minute_bar) & (minute_bar.index <end_minute_bar)
    # opening_range_bars=minute_bar.loc(opening_range_mask)
    # print(opening_range_mask)