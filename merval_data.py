import json
from threading import Lock

import pandas as pd


class MervalData():

    __data_thread_lock = None

    def __init__(self):
        self.government_bonds = pd.DataFrame()
        self.cedears = pd.DataFrame()
        self.general_board = pd.DataFrame()
        self.bluechips = pd.DataFrame()
        self.options_df = pd.DataFrame()

    def on_securities(self, online, quotes):
        if (quotes['group'] == 'bluechips').all():
            if self.bluechips.empty:
                self.bluechips = quotes.copy()
            else:
                self.bluechips.update(quotes)
        elif (quotes['group'] == 'general_board').all():
            if self.general_board.empty:
                self.general_board = quotes.copy()
            else:
                self.general_board.update(quotes)
        elif (quotes['group'] == 'cedears').all():
            if self.cedears.empty:
                self.cedears = quotes.copy()
            else:
                self.cedears.update(quotes)
        elif (quotes['group'] == 'government_bonds').all():
            if self.government_bonds.empty:
                self.government_bonds = quotes.copy()
            else:
                self.government_bonds.update(quotes)

    def on_options(self, online, quotes):
        if self.options_df.empty:
            self.options_df = quotes.copy()
        else:
            self.options_df.update(quotes)

    def get_merval_data(self, ticker):
        result = None
        self.__data_thread_lock = Lock()
        with self.__data_thread_lock:
            if self.general_board.index.isin([(ticker, '48hs')]).any():
                result = self.general_board.loc[(ticker, '48hs')]
            elif self.bluechips.index.isin([(ticker, '48hs')]).any():
                result = self.bluechips.loc[(ticker, '48hs')]
            elif self.cedears.index.isin([(ticker, '48hs')]).any():
                result = self.cedears.loc[(ticker, '48hs')]
            elif self.government_bonds.index.isin([(ticker, '48hs')]).any():
                result = self.government_bonds.loc[(ticker, '48hs')]
            elif self.options_df.index.isin([ticker]).any():
                result = self.options_df.loc[ticker]

        return json.loads(result.to_json()) if result is not None else None
