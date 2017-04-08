#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: __init__.py
# @Date: 2017-04-07
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

from ChineseStock.constants.path_info import Path


class Constant(Path):
    # Common constant
    TICKER = 'tic'
    DATE = 'date'

    # Other information
    REPORT_SELL_DATE = 'sell_date'
    REPORT_BUY_DATE = 'buy_date'
    REPORT_BUY_PRICE = 'buy_price'
    REPORT_BUY_TYPE = 'buy_type'
    REPORT_SELL_TYPE = 'sell_type'
    REPORT_SELL_PRICE = 'sell_price'

    STOCK_OPEN_PRICE = 'open'
    STOCK_HIGH_PRICE = 'high'
    STOCK_LOW_PRICE = 'low'
    STOCK_CLOSE_PRICE = 'close'
    STOCK_VOLUME = 'vol'

    # Parameters used in strategy calculating
    HOLDING_DAYS = 'holding_days'
    PORTFOLIO_NUM = 'portfolio_num'
    STOPLOSS_RATE = 'stoploss_rate'
    TRANSACTION_COST = 'transaction_cost'
    WEALTH_DATA_PATH = 'wealth_data_path'
    RUN_UP_THRESHOLD = 'run_up_threshold'
    RUN_UP_X = 'run_up_x'
    RUN_UP_Y = 'run_up_y'
    INPUT_REPORT_PATH = 'input_report_path'
    REPORT_DESCRIPTION = 'desciption'

    # Frame type mainly used in some calculating functicons
    WEALTH_DATAFRAME = 'wealth_df'
    RETURN_DATAFRAME = 'return_df'

    RESULT_SAVE_PATH = 'report_save_path'

    # report between this period would be neglected
    SAVE_TYPE_PICKLE = 'pickle'
    SAVE_TYPE_EXCEL = 'excel'
    SAVE_TYPE_CSV = 'csv'

    ALPHA_STRATEGY_LEGENDS = ['Raw Strategy', 'Beta Strategy', 'Alpha Strategy']

    BEST_RAW_SHARPE_RATIO = 'best_raw_sharpe_ratio'
    BEST_RAW_ANNUALIZED_RETURN = 'best_raw_ann_return'
    BEST_ALPHA_RETURN = 'best_alpha_return'
    BEST_ALPHA_SHARPE = 'best_alpha_sharpe'
    MINIMAL_ALPHA_DRAWDOWN = 'minimal_alpha_drawdown'
    MINIMAL_RAW_DRAWDOWN = 'minimal_raw_drawdown'
    PICTURE_PATH = 'pic_path'
    VALUE = 'value'

    SHARPE_RATIO = 'sharpe_ratio'
    ANNUALIZED_RETURN = 'ann_return'
    RETURN = 'return'

    RAW_STRATEGY = 'raw'
    ALPHA_STRATEGY = 'alpha'
    BETA_STRATEGY = 'beta'
