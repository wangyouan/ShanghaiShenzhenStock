#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: path
# @Date: 2017-04-07
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

from ChineseStock.utilities.os_related import get_root_path


class Path(object):
    ROOT_PATH = get_root_path()
    TEMP_PATH = os.path.join(ROOT_PATH, 'temp')
    DATA_PATH = os.path.join(ROOT_PATH, 'data')
    RESULT_PATH = os.path.join(ROOT_PATH, 'result')

    REPORT_DATA_PATH = os.path.join(DATA_PATH, 'report_data')
    STOCK_DATA_PATH = os.path.join(DATA_PATH, 'stock_price_data')

    STOCK_PRICE_20170408_FILE = os.path.join(DATA_PATH, 'stock_price_data', 'stock_price_20170408', 'stock_price.p')

    # Run up combinations x in [5, 10, 15, 20], y = 1
    INSIDER_EXE_GT2_RUN_UP_FILE = os.path.join(REPORT_DATA_PATH, 'report_data_20170408', 'insider_exe_gt2_runup.p')
    FORECAST_RUN_UP_REPORT_FILE = os.path.join(REPORT_DATA_PATH, 'report_data_20170408', 'forecast_runup.p')

    SZ_399300_PATH = os.path.join(STOCK_DATA_PATH, 'index_date', '399300_daily.p')

    # The longest trading days list from 1990 to 2017 from 1990-12-19 to 2017-02-13
    TRADING_DAYS_20170214_FILE = os.path.join(DATA_PATH, 'trading_days_list', 'trading_days_20170214.p')

    # This trading days list only cover 399300.SZ date from 2004-01-05 to 2017-02-13
    TRADING_DAYS_20170216_FILE = os.path.join(DATA_PATH, 'trading_days_list', 'trading_days_20170216.p')

    # This trading days list only cover 399300.SZ date from 2005-01-04 to 2017-02-13
    TRADING_DAYS_20170228_FILE = os.path.join(DATA_PATH, 'trading_days_list', 'trading_days_20170228.p')

    # This trading days list only cover 399300.SZ date from 2016-01-01 to 2017-02-13
    TRADING_DAYS_20170408_FILE = os.path.join(DATA_PATH, 'trading_days_list', 'trading_days_20170408.p')
