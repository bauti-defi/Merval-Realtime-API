#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Home Broker API - Market data downloader
# https://github.com/crapher/pyhomebroker.git
#
# Copyright 2020 Diego Degese
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import pandas as pd
from pyhomebroker import HomeBroker

from appSettings import AppSettings

appSettings = AppSettings()

government_bonds = pd.DataFrame()
cedears = pd.DataFrame()
general_board = pd.DataFrame()
bluechips = pd.DataFrame()
options_df = pd.DataFrame()


def start():
    hb.auth.login(dni=appSettings.config['dni'], user=appSettings.config['user'],
                  password=appSettings.config['password'], raise_exception=True)

    hb.online.connect()

    hb.online.subscribe_securities('bluechips', '48hs')
    hb.online.subscribe_securities('general_board', '48hs')
    hb.online.subscribe_securities('cedears', '48hs')
    hb.online.subscribe_securities('government_bonds', '48hs')

    hb.online.subscribe_options()


def stop():
    hb.online.unsubscribe_options()

    hb.online.unsubscribe_securities('bluechips', '48hs')
    hb.online.unsubscribe_securities('general_board', '48hs')
    hb.online.unsubscribe_securities('cedears', '48hs')
    hb.online.unsubscribe_securities('government_bonds', '48hs')
    hb.online.unsubscribe_securities('corporate_bonds', '48hs')

    hb.online.disconnect()


def on_open(online):
    print('=================== CONNECTION OPENED ====================')


def on_securities(online, quotes):
    global government_bonds, cedears, bluechips, general_board
    if (quotes['group'] == 'bluechips').all():
        if bluechips.empty:
            bluechips = quotes.copy()
        else:
            bluechips.update(quotes)
    elif (quotes['group'] == 'general_board').all():
        if general_board.empty:
            general_board = quotes.copy()
        else:
            general_board.update(quotes)
    elif (quotes['group'] == 'cedears').all():
        if cedears.empty:
            cedears = quotes.copy()
        else:
            cedears.update(quotes)
    elif (quotes['group'] == 'government_bonds').all():
        if government_bonds.empty:
            government_bonds = quotes.copy()
        else:
            government_bonds.update(quotes)


def on_options(online, quotes):
    global options_df
    if options_df.empty:
        options_df = quotes.copy()
    else:
        options_df.update(quotes)


def on_error(online, exception, connection_lost):
    print('@@@@@@@@@@@@@@@@@@@@@@@@@ Error @@@@@@@@@@@@@@@@@@@@@@@@@@')
    print(exception)


def on_close(online):
    print('=================== CONNECTION CLOSED ====================')


def get_merval_data(ticker):
    global options_df, general_board, bluechips, cedears, government_bonds
    result = None
    if general_board.index.isin([(ticker, '48hs')]).any():
        result = general_board.loc[(ticker, '48hs')]
    elif bluechips.index.isin([(ticker, '48hs')]).any():
        result = bluechips.loc[(ticker, '48hs')]
    elif cedears.index.isin([(ticker, '48hs')]).any():
        result = cedears.loc[(ticker, '48hs')]
    elif government_bonds.index.isin([(ticker, '48hs')]).any():
        result = government_bonds.loc[(ticker, '48hs')]
    elif options_df.index.isin([ticker]).any():
        result = options_df.loc[ticker]
    return result.to_json(orient='columns').replace('"', '') if result is not None else result


hb = HomeBroker(appSettings.config['broker_id'],
                on_open=on_open,
                on_securities=on_securities,
                on_options=on_options,
                on_error=on_error,
                on_close=on_close)
