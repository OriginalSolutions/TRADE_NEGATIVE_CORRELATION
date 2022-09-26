#!/usr/bin/env python3.8
from pybit import spot
from datetime import datetime
from time import time
from time import sleep
import pandas as pd # do wyświetlenia serii danych i obliczeń statystychnych
from pybit.spot import HTTP  
from config import api_key, api_secret


session_spot_testnet = HTTP(
    endpoint='https://api.bybit.com',   # real
    # endpoint= 'https://api-testnet.bybit.com',  # testnet
    #
    api_key=api_key,   
    api_secret=api_secret
)


session_unauth = spot.HTTP(endpoint="https://api.bybit.com")



##############################################################################################
#  IMPORT  DANYCH  
##############################################################################################

def long(symbol_long, interval):
    LONG = session_unauth.query_kline(
        symbol=symbol_long,
        interval=interval,
        limit = int(50)         ########   dla  celów  szybkich  wykonania  transakcji  (nie dla backtestu)
    )
    return LONG
    



def last_time_close_long(symbol_long, interval):
    LONG = session_unauth.query_kline(
        symbol=symbol_long,
        interval=interval,
        limit = int(1)
    )
    #
    ########  print(LONG)
    #
    if len(LONG['result']) > 0:
        time_long = LONG['result'][0][0]
        close_long = LONG['result'][0][4]
        #
    elif len(LONG['result']) ==0:
        time_long = int(0)
        close_long = int(0)
    #
    return [time_long, close_long]
   
    
   
 
def close_long(symbol_long, interval):
    #
    LONG = session_unauth.query_kline(
        symbol=symbol_long,
        interval=interval,
        limit = int(50)         ########   dla  celów  szybkich  wykonania  transakcji  (nie dla backtestu)
    )
    #
    klines_L = LONG['result']
    close_long =list()
    index_time_long = list()
    #
    for kline in klines_L:
        close_long.append(float(kline[4])) 
        index_time_long.append(int(kline[0]))    #  czas  jako  int()
        #
    return [close_long,  index_time_long]
    
    
######################################


def short(symbol_short, interval):
    SHORT = session_unauth.query_kline(
        symbol=symbol_short,
        interval=interval,
        limit = int(50)         ########   dla  celów  szybkich  wykonania  transakcji  (nie dla backtestu)
    )
    return SHORT
    
    
    

def last_time_close_short(symbol_short, interval):
    SHORT = session_unauth.query_kline(
        symbol=symbol_short,
        interval=interval,
        limit = int(1)
    )
    #
    ########  print(SHORT)
    #
    if len(SHORT['result']) >0:
        time_short = SHORT['result'][0][0]
        close_short = SHORT['result'][0][4]
        #
    elif len(SHORT['result']) ==0:
        time_short = int(0)
        close_short = int(0)
    #
    return [time_short, close_short]




def close_short(symbol_short, interval):
    SHORT = session_unauth.query_kline(
        symbol=symbol_short,
        interval=interval,
        limit = int(50)         ########   dla  celów  szybkich  wykonania  transakcji  (nie dla backtestu)
    )
    #
    klines_S = SHORT['result']
    close_short = list()
    index_time_short = list()
    #
    for kline in klines_S:
        close_short.append(float(kline[4]))
        index_time_short.append(int(kline[0]))    #  czas  jako  int()
        #
    return [close_short, index_time_short]




# ##############################################################################################
# #  OBLICZANIE BALANCU  DLA  POSZCZEGÓLNYCH  TOKENÓW
# ##############################################################################################

def balance_long(close_long, invested_capital, LONG):
    #
    i=0   
    balance_long = list()
    time_balance_long = list()
    #
    while i <= len(close_long)-1:
        if i==0:
            balance_long.append((invested_capital/2))
            #
            time_balance_long.append(datetime.fromtimestamp(round(LONG['result'][i][0]) / 1000).strftime("%Y-%m-%d %H:%M:%S"))  # SPOT
            #
        else:
            balance_long.append((invested_capital/2) * (float(float(close_long[i])/float(close_long[0]))))    #  wyrażone  w  ilorazie
            #
            time_balance_long.append(datetime.fromtimestamp(round(LONG['result'][i][0]) / 1000).strftime("%Y-%m-%d %H:%M:%S"))  # SPOT
            #
        i+=1
        #
    return balance_long
    
    
######################################


def balance_short(close_short, invested_capital, SHORT):
    #
    i=0  
    balance_short = list()
    time_balance_short = list()
    #
    while i <= len(close_short)-1:
        if i==0:
            balance_short.append((invested_capital/2))
            #
            time_balance_short.append(datetime.fromtimestamp(round(SHORT['result'][i][0]) / 1000).strftime("%Y-%m-%d %H:%M:%S"))  
            #
        else:
            balance_short.append((invested_capital/2) * (float(float(close_short[i])/float(close_short[0]))))     #  wyrażone  w   $
            #
            time_balance_short.append(datetime.fromtimestamp(round(SHORT['result'][i][0]) / 1000).strftime("%Y-%m-%d %H:%M:%S"))  
            #
        i+=1
        #
    return balance_short        





# #########################################################################
# # OBLICZANIE  CAŁKOWITEJ WARTOŚĆI PORTFELA    (WZGLĘDEM PIERWSZEJ CENY ZAMKNIĘCIA)
# #########################################################################

def balance_sl(balance_short, balance_long):
    #
    i=0
    balance = list()
    #
    while i <= len(balance_short)-1: 
        balance.append(float(balance_short[i] + balance_long[i]))         #  dodawanie zysków lub strat  ( short + long )
        i+=1
        #
    return balance



# #########################################################################
# # OBLICZANIE  CAŁKOWITEJ WARTOŚĆI PORTFELA    -  DODANIE INDEXU CZASU 
# #########################################################################

def timeseries_log(LONG, balance):
    #
    log=0
    timeseries_log = dict()
    #
    while log <= len(balance)-1:           
        timeseries_log[datetime.fromtimestamp(round(LONG['result'][log][0]) / 1000).strftime("%Y-%m-%d %H:%M:%S")] = balance[log]  # SPOT
        log+=1
        #
    return timeseries_log



# #########################################################################
# # OBLICZANIE DANYCH STATYSTYCZNYCH 
# #########################################################################

def ts_log(timeseries_log):
    #
    ts_log =  pd.Series(timeseries_log)
    statistyc_log = ts_log.describe()
    return ts_log



# #########################################################################
# #  OBLICZANIE ŚREDNICH KROCZĄCYCH   ( NA PODSTAWIE WSZEŚNIEJ OBLICZONYCH DANYCH STATYSTYCZNYCH )   
# #########################################################################

def MA_log__MSTD_log(ts_log, range_log):   # dlugo  oblicza !
    s_log=0
    MA_log = dict()
    MSTD_log= dict()
    #
    while s_log <= len(ts_log)-range_log:  
        MA_log[s_log+range_log] = ts_log[s_log:s_log+range_log].describe()[1]          # krocząca  średnia
        MSTD_log[s_log+range_log] = ts_log[s_log:s_log+range_log].describe()[2]     # krączące  jedno  odchylenia standardowe
        s_log+=1
    #
    return [MA_log, MSTD_log]
    
 

# #########################################################################
# #  OBLICZANIE ŚREDNICH KROCZĄCYCH  c.d.
# #########################################################################

def ma_log__std_plus_log__std_minus_log(balance, range_log, multiplier_plus_log: float(), indicator_minus_log: float(), data_log, invested_capital, MA_log, MSTD_log):
    #
    ma_log = list()
    std_plus_log = list()
    std_minus_log = list()
    multiplier_minus_log =  indicator_minus_log * multiplier_plus_log 
    m_log = 0
    #
    #
    for balance[m_log] in balance:    
        #
        if int(m_log) <= int(range_log-1): 
            #
            ma_log.append((data_log[m_log]-data_log[m_log]) + invested_capital)        
            std_plus_log.append((data_log[m_log]-data_log[m_log]) + invested_capital)
            std_minus_log.append((data_log[m_log]-data_log[m_log]) + invested_capital)
            m_log+=1
            #
        else:
            #
            ma_log.append((data_log[m_log]-data_log[m_log]) + MA_log[m_log])
            std_plus_log.append((data_log[m_log]-data_log[m_log]) + (MA_log[m_log]+(MSTD_log[m_log]*multiplier_plus_log)))
            std_minus_log.append((data_log[m_log]-data_log[m_log]) + (MA_log[m_log]-(MSTD_log[m_log]*multiplier_minus_log)))
            m_log+=1
            if m_log == len(balance)+1:
                break
        #
    return [ma_log, std_plus_log, std_minus_log]



# #########################################################################
# #  OBLICZANIE ZYSKU   BRUTTO  -  bez prowizji
# #########################################################################

def profit_net_and_gross_from_one_transaction_log(range_log, commission: float(), data_log, std_minus_log, std_plus_log, time_log):
    #
    buy = list()
    buy_minus_commission = list()
    profit_from_one_transaction_log = list()  #  bez  uwzględniania  prowizji
    profit_net_from_one_transaction_log = list()  #  po uwzględniania  prowizji
    b=range_log
    #
    time_buy = list()
    time_sell = list()
    #
    while b <= len(data_log)-1:
        #
        if data_log[b] < std_minus_log[b] and len(buy) == 0:  
            #
            buy_minus_commission.append(data_log[b] - (data_log[b] * commission))      # wartość  całego portfela (long+short)  po uwzględnieniu prowizji
            buy.append(data_log[b])     #  bez prowizji
            time_buy.append(time_log[b])  
            #
            #
        elif data_log[b] > std_plus_log[b] and len(buy_minus_commission) == 1 and len(buy) == 1:  #  Po uwzględnieniu prowizji 
            #
            balance_gross = (buy_minus_commission[0] * (data_log[b]/buy[0]))
            profit_net_from_one_transaction_log.append(balance_gross - (balance_gross * commission) - buy[0])   # po uwzględnieniu prowizji 
            profit_from_one_transaction_log.append(data_log[b] - buy[0])   #  bez  uwzględniania  prowizji
            #
            del(buy[0])
            del(buy_minus_commission[0])
            #
            time_sell.append(time_log[b]) 
            #
            #
        b+=1
        #
        #
        #
    return [time_buy, time_sell, profit_from_one_transaction_log, profit_net_from_one_transaction_log]
   
   
   
   
#########################################################################
# TRADE
#########################################################################


def buy_long(symbol_long, qty_short):
    buy_long_market = session_spot_testnet.place_active_order(
    symbol = symbol_long,
    side="BUY",             # drukowane ?
    type = "MARKET",
    qty = qty_short,      #  "10",     #   w $        #   dla zleceń rynkowych: kiedy side jest Buy, jest to waluta kwotowana.
    timeInForce =  "FOK"      # -->  FOK - Fill or Kill - realizuj w całosci ,     #  -->   IOC - Immediate or Cancel  - realizuj ile sie da,  reszte anuluj
    )
    return buy_long_market



def buy_short(symbol_short, qty_short):
    buy_short_market = session_spot_testnet.place_active_order(
    symbol = symbol_short,
    side="BUY",             
    type = "MARKET",
    qty = qty_short,    #  "22",     #  w $ 
    timeInForce =  "FOK"
    )
    return buy_short_market


###################################################


def sell_long(symbol_long, executed_qty_buy_long):
    sell_long_market = session_spot_testnet.place_active_order(
    symbol = symbol_long,
    side="SELL",            
    type = "MARKET",
    qty = executed_qty_buy_long,     # dla zleceń rynkowych: kiedy side jest Buy, jest to waluta kwotowana.  W przeciwnym razie ilość jest w walucie bazowej.  #  Na przykład na BTCUSDT Buy zamówienie jest w USDT, w przeciwnym razie w BTC.   
    timeInForce =  "FOK"
    )
    return sell_long_market



def sell_short(symbol_short, executed_qty_buy_short):
    sell_short_market = session_spot_testnet.place_active_order(
    symbol = symbol_short,
    side="SELL",             
    type = "MARKET",
    qty = executed_qty_buy_short,     
    timeInForce =  "FOK"
    )
    return sell_short_market




def get_balance(symbol):
    balance = session_spot_testnet.get_wallet_balance()
    len_balance = int(len(balance['result']['balances']))
    qty_long = float(0.0)
    i=int(0)
        #
    while i <= len_balance-1:
        if balance['result']['balances'][i]['coin'] == symbol:   #  symbol   -   przechodzi w cudzysłowiu, nie musi być apostrof
            qty_long = float(balance['result']['balances'][i]['total'])
        i+=1
        #
    if i == len_balance and qty_long == float(0.0):   # już wyszukuje prawidłowo
        qty_long = float(0.0)     
        #
    return qty_long


# END