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


from threading import Lock, Thread

import pandas as pd
from pyhomebroker import HomeBroker


class MervalSocket():

    __autoreconnect = True
    __connect_thread = None
    __connect_thread_lock = None

    def __init__(self, merval_data, config):
        self.merval_data = merval_data
        self.config = config

        self.__create_server()

    def __create_server(self):
        self.hb = HomeBroker(self.config['broker_id'],
                             on_open=self.on_open,
                             on_securities=self.merval_data.on_securities,
                             on_options=self.merval_data.on_options,
                             on_error=self.on_error,
                             on_close=self.on_close)

    def start(self):
        self.__connect_thread_lock = Lock()
        self.__connect_thread = Thread(target=self.__connect)
        self.__connect_thread.start()

    def __connect(self):
        with self.__connect_thread_lock:
            self.__autoreconnect = False

            try:
                print("Login to server.")

                self.hb.auth.login(
                    dni=self.config.dni,
                    user=self.config.user,
                    password=self.config.password,
                    raise_exception=True
                )

                print("Logged in to server.")
            except Exception as ex:
                print("Login failed.")
                return

            self.__autoreconnect = True

            print("Connecting to socket...")

            while self.__autoreconnect:
                try:
                    self.hb.online.connect()

                    print("Connected to socket.")
                    break
                except Exception as ex:
                    print("Error connecting to socket.")

    def on_open(self, connection):
        print('=================== CONNECTION OPENED ====================')

        self.hb.online.subscribe_securities('bluechips', '48hs')
        self.hb.online.subscribe_securities('general_board', '48hs')
        self.hb.online.subscribe_securities('cedears', '48hs')
        self.hb.online.subscribe_securities('government_bonds', '48hs')

        self.hb.online.subscribe_options()

        print("Subscribed to assets.")

    def on_error(self, connection, exception, connection_lost):
        print("Detected connection error.")
        if connection_lost:
            print("Detected connection lost: %s" % exception)
            self.on_close(connection)

    def on_close(self, connection):
        print('=================== CONNECTION CLOSED ====================')

        if self.__autoreconnect:
            print("Reconnecting due to connection loss...")
            self.__create_server()

            self.start()

    def stop(self):
        print("Disconnecting from server")

        self.__autoreconnect = False

        if self.hb.online.is_connected():
            self.hb.online.disconnect()
