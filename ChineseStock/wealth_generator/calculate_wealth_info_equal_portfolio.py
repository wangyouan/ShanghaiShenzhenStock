#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: ShanghaiShenzhenStock
# File name: calculate_wealth_info_equal_portfolio
# Author: warn
# Date: 2017/4/10

import os
from dateutil.relativedelta import relativedelta

import pandas as pd
import numpy as np

from ChineseStock.constants import Constant as const


def calculate_raw_alpha_wealth_series_record(hday, sr, irrp, rp, ap, bp, tag, p):
    """
    Generate wealth series
    :param hday: holding days
    :param sr: stop loss rate
    :param irrp: input return report path
    :param rp: raw series result path
    :param ap: alpha series result path
    :param bp: buy and sell record path
    :param tag: name tag
    :param p: portfolio num
    :return: None
    """
    if isinstance(sr, float):
        sr = int(100 * abs(sr))

    series_name = '{}_{}p_{}d_2cost_{}sr'.format(tag, p, hday, sr)
    report_file_name = 'hday{}_sr{}.p'.format(hday, sr)

    report_df = pd.read_pickle(os.path.join(irrp, report_file_name))
    stock_df = pd.read_pickle(const.STOCK_PRICE_20170408_FILE_13_2)
    index_df = pd.read_pickle(const.SZ_399300_PATH)

    raw_free_account = [const.initial_wealth / p for _ in range(p)]
    alpha_free_account = [const.initial_wealth / p for _ in range(p)]

    # holding list info {sell_date: [{tic, a_amount, r_amount, sell_price, buy_price, index_price, sell_type,
    #                                 buy_date}]}
    holding_list = {}

    tday_list = pd.read_pickle(const.TRADING_DAYS_20170408_FILE)
    raw_series = pd.Series()
    alpha_series = pd.Series()

    raw_series.loc[tday_list[0] - relativedelta(days=1)] = sum(raw_free_account)
    alpha_series.loc[tday_list[0] - relativedelta(days=1)] = sum(alpha_free_account)
    keys = list(report_df.keys())
    keys.append('amount')
    buy_sell_df = pd.DataFrame(columns=report_df.keys())
    buy_sell_index = 0

    # logger.info('Start generate wealth')
    for current_date in tday_list:

        # check whether we can buy some stocks
        today_report = report_df[report_df[const.REPORT_BUY_DATE] == current_date]
        today_index = index_df.loc[current_date]

        # logger.debug('Current free portfolio is {}, start to handle buy info'.format(free_p))
        if raw_free_account and not today_report.empty:
            for i in today_report.index:
                # get some useful info
                buy_sell_df.loc[buy_sell_index] = today_report.loc[i]
                # if np.isnan(today_report.loc[i, const.REPORT_SELL_PRICE]):
                #     continue
                trading_info = {const.REPORT_BUY_PRICE: today_report.loc[i, const.REPORT_BUY_PRICE],
                                const.REPORT_SELL_PRICE: today_report.loc[i, const.REPORT_SELL_PRICE],
                                const.REPORT_SELL_TYPE: today_report.loc[i, const.REPORT_SELL_TYPE],
                                const.TICKER: today_report.loc[i, const.TICKER],
                                # const.REPORT_BUY_DATE: current_date,
                                'last_price': today_report.loc[i, const.REPORT_BUY_PRICE],
                                }
                sell_date = today_report.loc[i, const.REPORT_SELL_DATE]
                buy_type = today_report.loc[i, const.REPORT_BUY_TYPE]

                # buy raw
                raw_amount = raw_free_account.pop(0)
                trading_info['raw_amount'] = raw_amount * (1 - const.transaction_cost)
                buy_sell_df.loc[buy_sell_index, 'amount'] = trading_info['raw_amount']

                # buy alpha
                alpha_amount = alpha_free_account.pop(0)
                trading_info['alpha_amount'] = alpha_amount * (1 - const.transaction_cost)
                trading_info['index_price'] = today_index[buy_type]

                if sell_date in holding_list:
                    holding_list[sell_date].append(trading_info)

                else:
                    holding_list[sell_date] = [trading_info]
                buy_sell_index += 1

                if len(raw_free_account) == 0:
                    break

        # check whether there are some stocks to sell or not
        if current_date in holding_list:

            # sell holding accounts
            for sell_info in holding_list[current_date]:
                buy_price = sell_info[const.REPORT_BUY_PRICE]
                sell_price = sell_info[const.REPORT_SELL_PRICE]
                raw_amount = sell_info['raw_amount']
                alpha_amount = sell_info['alpha_amount']
                ibuy_price = sell_info['index_price']  # index buy price

                # handle raw account
                raw_amount *= sell_price / buy_price * (1 - const.transaction_cost)
                raw_free_account.append(raw_amount)

                # handle alpha account
                isell_price = today_index[sell_info[const.REPORT_SELL_TYPE]]  # index sell price
                alpha_amount *= (sell_price / buy_price * (1 - const.transaction_cost) - isell_price / ibuy_price + 1)
                alpha_free_account.append(alpha_amount)

            # delete unused info
            del holding_list[current_date]
        # logger.debug('Current free portfolio is {}, handle sell info finished'.format(free_p))

        # Calculate current amount of raw and alpha
        raw_wealth = sum(raw_free_account)
        alpha_wealth = sum(alpha_free_account)

        ic_price = today_index[const.STOCK_CLOSE_PRICE]

        # logger.debug('Start to calculate today wealth'.format(free_p))
        for i_date in holding_list:
            for sell_info in holding_list[i_date]:
                tic = sell_info[const.TICKER]
                buy_price = sell_info[const.REPORT_BUY_PRICE]
                ibuy_price = sell_info['index_price']
                a_amount = sell_info['alpha_amount']
                r_amount = sell_info['raw_amount']

                # get stock price. If today has no such info, use yesterday's price
                if (current_date, tic) not in stock_df.index:
                    tc_price = sell_info['last_price']
                else:
                    tc_price = sell_info['last_price'] = stock_df.ix[(current_date, tic), const.STOCK_CLOSE_PRICE]

                # handle raw wealth
                raw_wealth += r_amount * tc_price / buy_price

                # handle alpha wealth
                alpha_wealth += a_amount * (tc_price / buy_price - ic_price / ibuy_price + 1)

        # logger.debug('Handle today wealth finished, raw wealth is {}, alpha wealth is {}'.format(raw_wealth,
        #                                                                                          alpha_wealth))
        raw_series.loc[current_date] = raw_wealth
        alpha_series.loc[current_date] = alpha_wealth

    # logger.info('Generate finished')
    raw_series.to_pickle(os.path.join(rp, '{}.p'.format(series_name)))
    alpha_series.to_pickle(os.path.join(ap, '{}.p'.format(series_name)))
    buy_sell_df.to_pickle(os.path.join(bp, '{}.p'.format(series_name)))
    buy_sell_df.to_csv(os.path.join(bp, '{}.csv'.format(series_name)))
    return raw_series, alpha_series
