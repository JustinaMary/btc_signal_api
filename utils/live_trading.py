# btc buy / sell signals for luke private mastermind


# import modules
import asyncio
import statistics
import time as epoch
import pandas as pd
import pprint

from utils import repo


# previous data storage
buy_volume = []
buy_size = []
sell_volume = []
sell_size = []

def luke():

    #while True:
        # ------------ Funding Data ------------

        funding = repo.get_funding_data(symbol=repo.const_symbol, limit=repo.const_limit)
        funding_reverse = funding[::-1]
        current_rate = funding_reverse[0]['funding_rate']
        funding_rate = [d['funding_rate'] for d in funding_reverse][:repo.const_mean_length]
        funding_mean = statistics.mean(funding_rate)
        funding_std = repo.calculate_std_dev(data=funding_rate)
        funding_upper_bb = funding_mean + (2 * funding_std)
        funding_lower_bb = funding_mean - (2 * funding_std)
        #await asyncio.sleep(0.2)
        epoch.sleep(0.2)

        # ------------ Candlestick Data ------------

        candles = repo.get_ohlc(symbol=repo.const_symbol, interval=repo.const_interval, limit=repo.const_limit)
        candles_reverse = candles[::-1]
        current_close = candles_reverse[0]['close']
        candle_close = [d['close'] for d in candles_reverse][:repo.const_mean_length]
        candle_mean = statistics.mean(candle_close)
        candle_std = repo.calculate_std_dev(data=candle_close)
        candle_upper_bb = candle_mean + (2 * candle_std)
        candle_lower_bb = candle_mean - (2 * candle_std)

        long_candle_close = [d['close'] for d in candles_reverse][:repo.const_long_mean_length]
        long_candle_mean = statistics.mean(long_candle_close)
        #await asyncio.sleep(0.2)
        epoch.sleep(0.2)
        signal_value = ''
        
        # ------------ Signals ------------

        if current_rate < funding_lower_bb and current_close < candle_lower_bb:
            print('buy signal')
            signal_value = 'buy'
            #order_size_usd = ((equity * candle_mean / current_close) - equity) * 1.2
            #order_size_base = order_size_usd / current_close
        elif current_rate > funding_upper_bb and current_close > candle_upper_bb and current_close > long_candle_mean:
            print('sell signal')
            signal_value = 'sell'
            #order_size_usd = ((equity * candle_mean / current_close) - equity)
            #order_size_base = order_size_usd / current_close
        else:
            print('waiting for next signal. previous signals: ')
            signal_value = 'waiting for next'
            # remaining time until next signal
        now_epoch = int(epoch.time())
        next_signal_time = ((candles_reverse[0]['close_time'] / 1000) - now_epoch)

        # data
        funding_df = pd.DataFrame(funding)
        ohlc_df = pd.DataFrame(candles)

        # funding data

        # time
        funding_df['hr_time'] = pd.to_datetime(funding_df['timestamp'], unit='ms')
        funding_df['hr_time'] = funding_df['hr_time'].dt.round('S')

            # bbs
        funding_df['mid_bb'] = funding_df['funding_rate'].rolling(window=repo.const_mean_length).mean()
        funding_df['funding_std'] = funding_df['funding_rate'].rolling(window=repo.const_mean_length).std()
        funding_df['upper_bb'] = funding_df['mid_bb'] + (2 * funding_df['funding_std'])
        funding_df['lower_bb'] = funding_df['mid_bb'] - (2 * funding_df['funding_std'])

        # ohlc data

        # time
        ohlc_df['hr_open_time'] = pd.to_datetime(ohlc_df['open_time'], unit='ms')
        ohlc_df['hr_open_time'] = ohlc_df['hr_open_time'].dt.round('S')
        ohlc_df['hr_close_time'] = pd.to_datetime(ohlc_df['close_time'], unit='ms')
        ohlc_df['hr_close_time'] = ohlc_df['hr_close_time'].dt.round('S')

        # bbs
        ohlc_df['mid_bb'] = ohlc_df['close'].rolling(window=repo.const_mean_length).mean()
        ohlc_df['ohlc_std'] = ohlc_df['close'].rolling(window=repo.const_mean_length).std()
        ohlc_df['upper_bb'] = ohlc_df['mid_bb'] + (2 * ohlc_df['ohlc_std'])
        ohlc_df['lower_bb'] = ohlc_df['mid_bb'] - (2 * ohlc_df['ohlc_std'])

        # long ma
        ohlc_df['200sma'] = ohlc_df['close'].rolling(window=repo.const_long_mean_length).mean()

        # signals
        buy_signal = (ohlc_df['close'] < ohlc_df['lower_bb']) & (funding_df['funding_rate'] < funding_df['lower_bb'])
        sell_signal = (ohlc_df['close'] > ohlc_df['upper_bb']) & (funding_df['funding_rate'] > funding_df['upper_bb']) & (ohlc_df['close'] > ohlc_df['200sma'])

        # buy signal
        filtered_buy_signal_funding = funding_df[buy_signal]
        filtered_buy_signal_ohlc = ohlc_df[buy_signal]

        print('buy signals: ')
        for index, row in filtered_buy_signal_ohlc.iterrows():
            time = row['hr_open_time']

            close = row['close']
                #order_size_usd = ((equity * (row['mid_bb'] / close)) - equity) * 1.2
                #order_size_base = order_size_usd / close

                # buy_volume.append(order_size_usd)
                # buy_size.append(order_size_base)
                # average_entry = sum(buy_volume) / sum(buy_size)

                #print(f'time: {time}, price: {close}, order size: {order_size_usd}, average entry: {average_entry}')

        # sell signal
        filtered_sell_signal_funding = funding_df[sell_signal]
        filtered_sell_signal_ohlc = ohlc_df[sell_signal]

        print('\nsell signals: ')
        for index, row in filtered_sell_signal_ohlc.iterrows():
            time = row['hr_open_time']

            close = row['close']
                #order_size_usd = ((equity * (close / row['mid_bb'])) - equity)
                #order_size_base = order_size_usd / close

                # sell_volume.append(order_size_usd)
                # sell_size.append(order_size_base)
                # average_exit = sum(sell_volume) / sum(sell_size)

                #print(f'time: {time}, price: {close}, order size: {order_size_usd}, average entry: {average_exit}')

        print('\ncurrent position: ')

            #position_size = sum(buy_volume) - sum(sell_volume)
            #average_entry = sum(buy_volume) / sum(buy_size)
            #average_exit = sum(sell_volume) / sum(sell_size)
        price = ohlc_df.iloc[-1]['close']
            #sum_open = sum(buy_size) * price
            #sum_exit = sum(sell_size) * price
            # realized_profit = ((average_exit / average_entry) * sum_exit) - sum_exit
            # unrealized_profit = ((price / average_entry) * position_size) - position_size
            # message = ''
            # remaining_time = ''
            # if price > average_entry:
            #      message = (f'Congratulations. You are in ${round(realized_profit + unrealized_profit, 2)} of profits. Or %{round((((equity + realized_profit + unrealized_profit) / equity) - 1) * 100, 2)} returns.')
            #      remaining_time = (f'{round(next_signal_time / 3600)}h remaining until next potential signal.')
            # else:
            #      remaining_time = (f'{round(next_signal_time / 3600)}h remaining until next potential signal.')  
            # position_dict = {
            #     'starting_equity': equity,
            #     'symbol': repo.const_symbol,
            #     'price': price,
            #     'average_entry': round(average_entry, 2),
            #     'average_exit': round(average_exit, 2),
            #     'position_size': round(position_size, 2),
            #     'realized_pnl': round(realized_profit, 2),
            #     'unrealized_pnl': round(unrealized_profit, 2),
            #     'total_pnl': round(realized_profit + unrealized_profit, 2),
            #     'current_equity': round(equity + realized_profit + unrealized_profit, 2),
            #     'percent_returns': round((((equity + realized_profit + unrealized_profit) / equity) - 1) * 100, 2),
            #     'message' : message,
            #     'remaining_time': remaining_time
            # }
        remaining_time = round(next_signal_time / 3600)
        position_dict = {
            'price': price,
            'signal': signal_value,
            'remaining_time': remaining_time
        }

        return position_dict 
    
            # if price > average_entry:
            #     print(f'Congratulations. You are in ${round(realized_profit + unrealized_profit, 2)} of profits. Or %{round((((equity + realized_profit + unrealized_profit) / equity) - 1) * 100, 2)} returns.')
            #     print(f'{round(next_signal_time / 3600)}h remaining until next potential signal.')
            # else:
            #     print(f'{round(next_signal_time / 3600)}h remaining until next potential signal.')

            # await asyncio.sleep(next_signal_time)
