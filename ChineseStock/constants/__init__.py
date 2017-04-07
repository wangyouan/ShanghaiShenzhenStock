#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: __init__.py
# @Date: 2017-04-07
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

from ChineseStock.constants.path_info import Path


class Constant(Path):
    working_days = 251
    initial_wealth = 10000.0

    # Other information
    ALL = 'all'
    OVERWEIGHT = u'增持'
    REDUCTION = u'减持'
    SENIOR = u'高管'
    COMPANY = u'公司'
    DIRECTOR = u'董事'
    PERSON = u'个人'
    SUPERVISOR = u'监事'

    SPOUSE = u'配偶'
    SELF = u'本人'
    PARENTS = u'父母'
    FATHER = u'父亲'
    MOTHER = u'母亲'
    OTHERS = u'其他'
    BROTHERS = u'兄弟姐妹'
    OTHER_RELATIONS = u'其他关联'

    CONTROLLED_CORPORATION = u'受控法人'
    LISTED_COMPANY = u'上市公司'

    REPORT_TICKER = 'VAR1'
    REPORT_COMPANY_NAME = 'VAR2'
    REPORT_ANNOUNCE_DATE = 'anndate'
    REPORT_ACTION = 'VAR10'
    REPORT_RELATIONSHIP = 'relation'
    REPORT_TYPE = 'type'
    REPORT_CHANGER_NAME = 'name'
    REPORT_AVERAGE_PRICE = 'average_price'
    REPORT_REASON = 'reason'
    REPORT_POSITION = 'position'
    REPORT_CHANGE_NUMBER = 'number'

    REPORT_SELL_DATE = 'sell_date'
    REPORT_RETURN_RATE = 'return'
    REPORT_BUY_DATE = 'buy_date'
    REPORT_MARKET_TICKER = 'market_ticker'
    REPORT_MARKET_TYPE = 'market_type'
    REPORT_BUY_PRICE = 'buy_price'
    REPORT_BUY_TYPE = 'buy_type'
    REPORT_SELL_TYPE = 'sell_type'

    STOCK_TICKER = 'Stkcd'
    STOCK_DATE = 'Trddt'
    STOCK_OPEN_PRICE = 'Opnprc'
    STOCK_OPEN_PRICE2 = 'Opnprc2'
    STOCK_HIGH_PRICE = 'Hiprc'
    STOCK_LOW_PRICE = 'Loprc'
    STOCK_CLOSE_PRICE = 'Clsprc'
    STOCK_CLOSE_PRICE2 = 'Clsprc2'
    STOCK_VOLUME = 'Dnshrtrd'
    STOCK_MARKET_TYPE = 'Markettype'
    STOCK_ADJPRCWD = 'Adjprcwd'
    STOCK_ADJPRCND = 'Adjprcnd'

    HOLDING_DAYS = 'holding_days'
    PORTFOLIO_NUM = 'portfolio_num'
    STOPLOSS_RATE = 'stoploss_rate'
    INFO_TYPE = 'info_type'
    TRANSACTION_COST = 'transaction_cost'
    REPORT_RETURN_PATH = 'report_return_path'
    WEALTH_DATA_PATH = 'wealth_data_path'

    WEALTH_DATAFRAME = 'raw_strategy_df'
    RETURN_DATAFRAME = 'return_df'

    REPORT_PATH = 'report path'
    TRADING_SIGNAL_PATH = 'trading signal path'

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

    RUN_UP_RATE = 'run_up'
    RUN_UP_X = 'run_up_x'
    RUN_UP_Y = 'run_up_y'
