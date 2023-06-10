from iqoptionapi.stable_api import IQ_Option
import logging      
import pandas as pd
from tradingview_ta import TA_Handler, Interval, Exchange   
import iqoptionapi
import tradingview_ta
import time
import sys

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
I_want_money=IQ_Option("twopointfive@gmail.com","twopointfive@gmail.com")
#Default is "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
header={"User-Agent":r"Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0"}
cookie={"I_want_money":"GOOD"}
MODE="PRACTICE"
I_want_money.set_session(header,cookie)
I_want_money.connect()#connect to iqoption
print(I_want_money.check_connect())
I_want_money.connect()
I_want_money.get_server_timestamp()
I_want_money.change_balance(MODE)
                        #MODE: "PRACTICE"/"REAL
I_want_money.get_balance()

API = IQ_Option("twopointfive@gmail.com", "twopointfive@gmail.com")
check, reason = API.connect()
if not check:
    print("Connection failed. Reason: {}".format(reason))
    exit()
print("Connection successful")
#parameters
bollinger_length = 20
bollinger_deviation = 2.3
x = 5
amount = 1
direction = ""
balance_before = I_want_money.get_balance()
balance_after = I_want_money.get_balance()
profit_result = 0
loss_result = 0
trade_placed = False
#EmaHandler
handler = TA_Handler(
    symbol="EURUSD",
    exchange="FX_IDC",
    screener="forex",
    interval="5m",
    timeout=None
)
while True:
    then=int(time.time())
    current_price = API.get_candles("EURUSD-OTC", 60 * x, 1, time.time())[0]["close"]
    analysis = handler.get_analysis()
    ema = analysis.indicators["EMA100"]
    #Uptrend
    # if (current_price > ema) and profit_result<30 and loss_result<1 :
    if (current_price > ema) :
        candles = API.get_candles("EURUSD-OTC", 60 * x, 100, time.time())
        close_prices = [candle["close"] for candle in candles]
        df = pd.DataFrame(candles)        
        df['sma'] = df['close'].rolling(window=bollinger_length).mean()
        df['std_dev'] = df['close'].rolling(window=bollinger_length).std()
        df['lower_band'] = df['sma'] - bollinger_deviation * df['std_dev']
        lower_band = df['lower_band'].iloc[-1]
        #balance_before = I_want_money.get_balance()
        if (current_price <= 10 ) :
            if not trade_placed:
                direction = "call"
                now = time.time()
                def get_remaining_seconds(x):
                  current_time = time.localtime()
                  current_minute = current_time.tm_min
                  remaining_seconds = (x - (current_minute % x)) * 60 - current_time.tm_sec
                  return remaining_seconds
                remaining_seconds = get_remaining_seconds(x)

                if remaining_seconds < 30:
                    continue
                elif remaining_seconds >= 91 and remaining_seconds <= 150:
                    value = 2
                elif remaining_seconds >= 151 and remaining_seconds <= 210:
                    value = 3
                elif remaining_seconds >= 211 and remaining_seconds <= 270:
                    value = 4
                elif remaining_seconds >= 271 and remaining_seconds <= 330:
                    value = 5
                else:
                    continue
                
                result, order_id = API.buy(amount, "EURUSD-OTC", direction, value)
                if result:
                    print("CALL Trade placed successfully at : ",current_price)
                    trade_placed = True
                else:
                    print("Error placing trade:")
    #downtrend
    elif (current_price <= ema) :
        candles = API.get_candles("EURUSD-OTC", 60 * x, 100, time.time())
        close_prices = [candle["close"] for candle in candles]
        df = pd.DataFrame(candles)        
        df['sma'] = df['close'].rolling(window=bollinger_length).mean()
        df['std_dev'] = df['close'].rolling(window=bollinger_length).std()
        df['upper_band'] = df['sma'] + bollinger_deviation * df['std_dev']
        upper_band = df['upper_band'].iloc[-1]
        if (current_price >= 0 ) :
            if not trade_placed:
                direction = "put"
                now = time.time()
                def get_remaining_seconds(x):
                  current_time = time.localtime()
                  current_minute = current_time.tm_min
                  remaining_seconds = (x - (current_minute % x)) * 60 - current_time.tm_sec
                  return remaining_seconds
                remaining_seconds = get_remaining_seconds(x)

                if remaining_seconds < 30:
                    continue
                elif remaining_seconds >= 91 and remaining_seconds <= 150:
                    value = 2
                elif remaining_seconds >= 151 and remaining_seconds <= 210:
                    value = 3
                elif remaining_seconds >= 211 and remaining_seconds <= 270:
                    value = 4
                elif remaining_seconds >= 271 and remaining_seconds <= 330:
                    value = 5
                else:
                    continue
               
                result, order_id = API.buy(amount, "EURUSD-OTC", direction, value)
                if result:
                    print("PUT Trade placed successfully ")
                    trade_placed = True
                else:
                    print("Error placing trade:")
    if trade_placed and time.time() > now + remaining_seconds:
       
        trade_result = API.check_win_v3(order_id)
        balance_after = I_want_money.get_balance()
        if (balance_after > balance_before):
          profit_result = profit_result+1
          print("Win")
        elif (balance_after < balance_before):
          loss_result = loss_result + 1
          print("Loss")
        if trade_result == "win":
            print("Trade won!")
        elif trade_result == "loose":
            print("Trade lost.")
        else:
            print("Trade result unknown.")
       
        trade_placed = False
    print(then)
    time.sleep(0.5)