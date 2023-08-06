from vcsc_data_common.live_price_data import DataFetcher as LiveDataFetcher, MarketStatus
from vcsc_data_common.offline_price_data import DataFetcher as OfflineDataFetcher
import pandas as pd
import time
import logging


class IntervalFetching:
    offline_data_df: pd.DataFrame
    live_data_df: pd.DataFrame

    def __init__(self, aws_access_key: str, aws_secret_key: str, time_frame: str, interval: int, callback: callable, is_fill_gap: bool = False) -> None:
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.time_frame = time_frame
        self.callback = callback
        self.interval = interval
        self.live_modification_time = None
        self.is_fill_gap = is_fill_gap

        self.live_data_fetcher = LiveDataFetcher(
            aws_access_key, aws_secret_key, time_frame, is_fill_gap)

        self.offline_data_fetcher = OfflineDataFetcher(
            aws_access_key, aws_secret_key, time_frame, is_fill_gap)

    def start(self):
        self.offline_data_df = self.offline_data_fetcher.get_data()

        while True:

            new_live_modification_time = self.live_data_fetcher.get_latest_modification_time()

            if(self.live_modification_time != new_live_modification_time):

                self.live_data_df = self.live_data_fetcher.get_data()

                # bỏ những cây nến chưa complete trong LO_AFTERNOON và LO_MORNING
                self.live_data_df = self.filter_completed_candles(
                    self.live_data_df)

                union_df = pd.concat([self.offline_data_df, self.live_data_df])

                self.callback(union_df, new_live_modification_time)

            else:
                logging.debug(
                    f'data has no change, modification time {new_live_modification_time}')

            self.live_modification_time = new_live_modification_time
            time.sleep(self.interval)

    def filter_completed_candles(self, df: pd.DataFrame):

        market_status_df = self.live_data_fetcher.get_market_status()

        hnx_market_status = market_status_df[market_status_df['marketCode']
                                             == 'HNX'].iloc[-1]['status']

        if hnx_market_status in [MarketStatus.LO_AFTERNOON.name, MarketStatus.LO_MORNING.name]:
            max_trading_date = df['TradingDate'].max()

            return df[df['TradingDate'] < max_trading_date]

        return df
