#!/usr/bin/env python3.8
from bybit_trade_funcions_git_hub import *
# t_1 = time()
session_unauth = spot.HTTP(endpoint="https://api.bybit.com")


# PARAMETRY
##############################################################################################
symbol_long = "BTC3LUSDT" 
symbol_short ="BTC3SUSDT"

# symbol_short ="BTCUSDT"
# symbol_long = "BTCUSDT" 

# symbol_long = "ATOM2LUSDT" 
# symbol_short ="FTM2SUSDT" 


##############################################################################################
interval = "1m"   
range_log = 28   #  18  dla derywatów,  4  dla spot 

invested_capital = int(200)  # $
commission = float(0.001)

multiplier_plus_log = float(1.0)    # dla  dodatniego  odchylenia standardowego    #  1.5   dla derywatów,   ##  1.0 dla:  spot + derywat
indicator_minus_log = float(2.0)  # dla  ujemnego   odchylenia standardowego     #  1.0   dla derywatów,   ##  1.5 dla:  spot + derywat   ####  2.5


# START
##############################################################################################
last_time_long, last_close_long = last_time_close_long(symbol_long, interval)
last_time_short, last_close_short = last_time_close_short(symbol_short, interval)
    
start = 1   #  wykonujemy obliczenia i uruchamiamy handel 
start_close = 1
i=1



while True:
    # t_2 = time()
    ##############################################################################################
    #
    #  DATA IMPORT
    #
    ##############################################################################################
    
    if start == 2:
        last_time_long, last_close_long = last_time_close_long(symbol_long, interval)
        sleep(0.05)
        last_time_short, last_close_short = last_time_close_short(symbol_short, interval)
        #
        if last_time_long == int(0) or last_time_short == int(0) :
            continue
        #
        elif float(last_time_short) != float(last_time_long):
            continue
        #
        else:
            if last_time_long == index_time_long[len(index_time_long)-1] and last_time_short == index_time_short[len(index_time_short)-1]:
                continue
                #
            elif start_close == 2:
                close_l.append(last_close_long)
                close_s.append(last_close_short)
                del close_l[0]
                del close_s[0]
                index_time_long.append(last_time_long)
                index_time_short.append(last_time_short)
                del index_time_long[0]
                del index_time_short[0]
                #
                #
                #
            start = 1   #  wykonujemy obliczenia i uruchamiamy handel 
        #
        #
        #
    elif start == 1 and float(last_time_short) == float(last_time_long):
        if start_close == 1:
            close_l, index_time_long = close_long(symbol_long, interval)
            close_s, index_time_short = close_short(symbol_short, interval)
            start_close = 2
        #
        LONG = long(symbol_long, interval)   #  zwraca wszystkie dane o: BTC3LUSDT
        SHORT = short(symbol_short, interval)


    ##############################################################################################
    #
    #   CALCULATE
    #
    ##############################################################################################
    
        #  OBLICZANIE BALANCU  DLA  POSZCZEGÓLNYCH  TOKENÓW
        ##########################################################################
        balance_l = balance_long(close_l, invested_capital*float(1.0), LONG)   # 1.1 
        balance_s = balance_short(close_s, invested_capital*float(1.0), SHORT)
        
        # OBLICZANIE  CAŁKOWITEJ WARTOŚĆI PORTFELA    
        # (WZGLĘDEM PIERWSZEJ CENY ZAMKNIĘCIA)
        ##########################################################################
        balance = balance_sl(balance_s, balance_l)

        # OBLICZANIE  CAŁKOWITEJ WARTOŚĆI PORTFELA    -  DODANIE INDEXU CZASU 
        ##########################################################################
        times_log = timeseries_log(LONG, balance)
        # t_3 = time()

        # OBLICZANIE DANYCH STATYSTYCZNYCH 
        ##########################################################################
        ts = ts_log(times_log)                              #  "timeseries_log"   opakowane w:   pandas.Series
        time_log  = ts.index                                 #  tylko   czas,   bez indeksu danych 
        data_log = ts.reset_index(drop=True)       #  tylko   dane,   bez indeksu czasu     -    cała kowita wartość portfela  (nie uwzględniająca prowizji)

        #  OBLICZANIE ŚREDNICH KROCZĄCYCH   
        # ( NA PODSTAWIE WSZEŚNIEJ OBLICZONYCH DANYCH STATYSTYCZNYCH )
        ##########################################################################
        MA_log, MSTD_log = MA_log__MSTD_log(ts, range_log)
        
        #  OBLICZANIE ŚREDNICH KROCZĄCYCH  c.d.
        ##########################################################################
        ma_log, std_plus_log, std_minus_log = \
        ma_log__std_plus_log__std_minus_log(balance, range_log, multiplier_plus_log, indicator_minus_log, data_log, invested_capital, MA_log, MSTD_log)

        start = 2           #   dla handlu od_komentować
        
        
        # #############################################################################################
        # #     START  BACKTESTING  SPEED        #     do handlu  za_komentować
        # #############################################################################################
        # #   t_4 = time()
        # # print(str(t_1)+"    "+str(t_2)+"    "+str(t_3)+"    "+str(t_4))
        # # print("czas wykonywania opreacji statystycznych  (w sekundach)  =   " f'{ (float(t_4) - float(t_2)) }')  
        
        # ########################################################################
        # #                   CALCULATION OF GROSS PROFIT - no commission
        # ########################################################################
        # time_buy, time_sell, profit_from_one_transaction_log, profit_net_from_one_transaction_log = \
        # profit_net_and_gross_from_one_transaction_log(range_log, commission, data_log, std_minus_log, std_plus_log, time_log)
        
        # start = 2   
        
        # print(profit_from_one_transaction_log)
        # profit =  pd.Series(profit_from_one_transaction_log, dtype='object')
        # cumsum_profit = profit.cumsum()
        # print("CUMSUM PROFIT BRUTTO")
        # print(cumsum_profit)
        # #############################################################################################
        # #     STOP  BACKTESTING  SPEED 
        # #############################################################################################


    ##############################################################################################
    #
    #   PRINT  LOGS
    #
    ##############################################################################################
        print(datetime.fromtimestamp(round(index_time_long[len(index_time_long)-1]) / 1000).strftime("%Y-%m-%d %H:%M:%S")) 
        print(close_l[len(close_l)-1])

        print(datetime.fromtimestamp(round(index_time_short[len(index_time_short)-1]) / 1000).strftime("%Y-%m-%d %H:%M:%S")) 
        print(close_s[len(close_s)-1])  
        
        print(data_log[len(data_log)-1])
        print(std_minus_log[len(std_minus_log)-1])
        print(std_plus_log[len(std_plus_log)-1])
        
        print(" "*10)


    ##############################################################################################
    #
    #   TRADE  
    #
    ##############################################################################################
        
        latest_information_short = session_unauth.latest_information_for_symbol(symbol=symbol_short)
        last_price_short = round(float(latest_information_short['result']['lastPrice']) * float(1.02), 4)

        latest_information_buy = session_unauth.latest_information_for_symbol(symbol=symbol_long)
        last_price_buy = round(float(latest_information_buy['result']['lastPrice']) * float(1.02), 4)

        if last_price_short > last_price_buy:
            last_price = last_price_short
            #
        elif last_price_short <= last_price_buy:
            last_price = last_price_buy  


        ########################################################################    
        #           BUY          #          if there is sufficient capital
        ########################################################################
        
        if data_log[len(data_log)-1] < std_minus_log[len(std_minus_log)-1] and  get_balance("USDT") >= last_price * float(2.1): 
            print(" WYGENEROWANO  SYGNAL:    KUPNA ")
            print("wartosc wolnych srodkow  USDT   przed   transakcja   =   " f'{round(get_balance("USDT"), 2)}')
            
            ####################
            #   SYMBOL    LONG
            ####################
            trade_buy_long = buy_long(symbol_long, last_price)                 #  kupuje np.  za  20 $
            executed_qty_buy_long = trade_buy_long['result']['origQty']     #  za  ile  $  faktycznie  kupiło

            while True:
                if float(executed_qty_buy_long) <= float(last_price * float(0.95)):  #  w $
                    #
                    trade_buy_long = buy_long(symbol_long, last_price)          # na zasadzie:     timeInForce =  "FOK"     (realizuj w całosci)
                    executed_qty_buy_long = trade_buy_long['result']['origQty']
                else:
                    print("Kupiono  BTC3_L  za  USDT:         " f'{executed_qty_buy_long}')
                    break
                  
            ####################
            #   SYMBOL    SHORT
            ####################
            trade_buy_short = buy_short(symbol_short, last_price)
            executed_qty_buy_short = trade_buy_short['result']['origQty']

            while True:
                if float(executed_qty_buy_short) <= float(last_price * float(0.95)):   #  w $
                    #
                    trade_buy_short = buy_short(symbol_short, last_price)
                    executed_qty_buy_short = trade_buy_short['result']['origQty']
                else:
                    print("Kupiono  BTC3_S  za  USDT:         " f'{executed_qty_buy_short}')
                    break


        ########################################################################    
        #           SELL            # 
        ########################################################################
        
        elif data_log[len(data_log)-1] > std_plus_log[len(std_plus_log)-1]: 
            print(" WYGENEROWANO  SYGNAL:    SPRZEDAJ ")
            
            ####################
            #   SYMBOL    LONG
            ####################
            symbol_long_coin = "BTC3L"
            qty_buy_long = float(str(round(get_balance(symbol_long_coin) * 10000, 3))[0:-3]) / 10000
            
            while True:
                if float(qty_buy_long) >= float(1.0):        #  jeśeli  wynosi poniżej:    1.0   coina    nie wykonuje transakcji sprzedaży - bo nie ma conina w portfelu.  
                    trade_sell_long = sell_long(symbol_long, qty_buy_long)  
                    qty_sell_long = trade_sell_long['result']['origQty']
                    print("Sprzedano  BTC3_L   w ilosci  coin:         " f'{qty_sell_long}')
                    #
                    qty_buy_long = float(str(round(get_balance(symbol_long_coin) * 10000, 3))[0:-3]) / 10000
                    #
                else:
                    print("Brak wystarczjacej ilosci coinow  BTC3_L ")
                    print("Ilosc posiadanych coinów BTC3_L    =     " f'{qty_buy_long}')
                    break
 
            ####################
            #   SYMBOL    SHORT
            ####################
            symbol_short_coin = "BTC3S"
            qty_buy_short = float(str(round(get_balance(symbol_short_coin) * 10000, 3))[0:-3]) / 10000
            
            while True:
                if float(qty_buy_short) >= float(1.0): 
                    trade_sell_short = sell_short(symbol_short, qty_buy_short)
                    qty_sell_short = trade_sell_short['result']['origQty']
                    print("Sprzedano  BTC3_S   w ilosci  coin:         " f'{qty_sell_short}')   
                    #
                    qty_buy_short = float(str(round(get_balance(symbol_short_coin) * 10000, 3))[0:-3]) / 10000
                    #
                else:
                    print("Brak wystarczjacej ilosci coinow  BTC3_S ")
                    print("Ilosc posiadanych coinow  BTC3_S    =     " f'{qty_buy_short}')
                    print(" "*10)
                    break
                    
            print("wartosc wolnych srodkow  USDT   po   transakcji   =   " f'{round(get_balance("USDT"), 2)}')
            print(" "*10)
        ###################################################


# END