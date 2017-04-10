#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: calculate_wealth_info
# @Date: 2017-04-10
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
from dateutil.relativedelta import relativedelta

import pandas as pd

from ChineseStock.constants import Constant as const


# test information
# import logging
# import sys

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
#                     format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')

# logger = logging.getLogger('Test Strategies')


def calculate_raw_alpha_wealth_series(hday, sr, irrp, rp, ap, tag, p):
    """
    Generate wealth series
    :param hday: holding days
    :param sr: stop loss rate
    :param irrp: input return report path
    :param rp: raw series result path
    :param ap: alpha series result path
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

    raw_free = alpha_free = const.initial_wealth
    free_p = p

    # holding list info {sell_date: [{tic, a_amount, r_amount, sell_price, buy_price, index_price, sell_type,
    #                                 buy_date}]}
    holding_list = {}

    tday_list = pd.read_pickle(const.TRADING_DAYS_20170408_FILE)
    raw_series = pd.Series()
    alpha_series = pd.Series()

    raw_series.loc[tday_list[0] - relativedelta(days=1)] = raw_free
    alpha_series.loc[tday_list[0] - relativedelta(days=1)] = alpha_free

    # logger.info('Start generate wealth')
    for current_date in tday_list:

        # check whether we can buy some stocks
        today_report = report_df[report_df[const.REPORT_BUY_DATE] == current_date]
        today_index = index_df.loc[current_date]

        # logger.debug('Current free portfolio is {}, start to handle buy info'.format(free_p))
        if free_p > 0 and not today_report.empty:
            for i in today_report.index:
                # get some useful info
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
                raw_amount = raw_free / free_p
                raw_free -= raw_amount
                trading_info['raw_amount'] = raw_amount * (1 - const.transaction_cost)

                # buy alpha
                alpha_amount = alpha_free / free_p
                alpha_free -= alpha_amount
                trading_info['alpha_amount'] = alpha_amount * (1 - const.transaction_cost)
                trading_info['index_price'] = today_index[buy_type]

                if sell_date in holding_list:
                    holding_list[sell_date].append(trading_info)

                else:
                    holding_list[sell_date] = [trading_info]

                free_p -= 1
                if free_p == 0:
                    break
        # logger.debug('Current free portfolio is {}, handle buy info finished'.format(free_p))

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
                raw_free += raw_amount

                # handle alpha account
                isell_price = today_index[sell_info[const.REPORT_SELL_TYPE]]  # index sell price
                alpha_amount *= (sell_price / buy_price * (1 - const.transaction_cost) - isell_price / ibuy_price + 1)
                alpha_free += alpha_amount

                free_p += 1

            # delete unused info
            del holding_list[current_date]
        # logger.debug('Current free portfolio is {}, handle sell info finished'.format(free_p))

        # Calculate current amount of raw and alpha
        raw_wealth = raw_free
        alpha_wealth = alpha_free

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
    return raw_series, alpha_series


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

    raw_free = alpha_free = const.initial_wealth
    free_p = p

    # holding list info {sell_date: [{tic, a_amount, r_amount, sell_price, buy_price, index_price, sell_type,
    #                                 buy_date}]}
    holding_list = {}

    tday_list = pd.read_pickle(const.TRADING_DAYS_20170408_FILE)
    raw_series = pd.Series()
    alpha_series = pd.Series()

    raw_series.loc[tday_list[0] - relativedelta(days=1)] = raw_free
    alpha_series.loc[tday_list[0] - relativedelta(days=1)] = alpha_free
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
        if free_p > 0 and not today_report.empty:
            for i in today_report.index:
                # get some useful info
                buy_sell_df.loc[buy_sell_index] = today_report.loc[i]
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
                raw_amount = raw_free / free_p
                raw_free -= raw_amount
                trading_info['raw_amount'] = raw_amount * (1 - const.transaction_cost)
                buy_sell_df.loc[buy_sell_index, 'amount'] = trading_info['raw_amount']

                # buy alpha
                alpha_amount = alpha_free / free_p
                alpha_free -= alpha_amount
                trading_info['alpha_amount'] = alpha_amount * (1 - const.transaction_cost)
                trading_info['index_price'] = today_index[buy_type]

                if sell_date in holding_list:
                    holding_list[sell_date].append(trading_info)

                else:
                    holding_list[sell_date] = [trading_info]
                buy_sell_index += 1

                free_p -= 1
                if free_p == 0:
                    break
        # logger.debug('Current free portfolio is {}, handle buy info finished'.format(free_p))

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
                raw_free += raw_amount

                # handle alpha account
                isell_price = today_index[sell_info[const.REPORT_SELL_TYPE]]  # index sell price
                alpha_amount *= (sell_price / buy_price * (1 - const.transaction_cost) - isell_price / ibuy_price + 1)
                alpha_free += alpha_amount

                free_p += 1

            # delete unused info
            del holding_list[current_date]
        # logger.debug('Current free portfolio is {}, handle sell info finished'.format(free_p))

        # Calculate current amount of raw and alpha
        raw_wealth = raw_free
        alpha_wealth = alpha_free

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


if __name__ == '__main__':
    import pathos
    import multiprocessing

    portfolio_range = [15, 20, 22, 25, 30]
    # input_report_path = [os.path.join(const.TEMP_PATH, '20170409_test', 'input_return_report') for _ in portfolio_range]
    # raw_wealth_path = [os.path.join(const.TEMP_PATH, '20170409_test', 'raw_wealth') for _ in portfolio_range]
    # alpha_wealth_path = [os.path.join(const.TEMP_PATH, '20170409_test', 'alpha_wealth') for _ in portfolio_range]
    # tag = ['test' for _ in portfolio_range]
    input_report_path = os.path.join(const.TEMP_PATH, '20170409_test', 'input_return_report')
    raw_wealth_path = os.path.join(const.TEMP_PATH, '20170409_test', 'raw_wealth')
    alpha_wealth_path = os.path.join(const.TEMP_PATH, '20170409_test', 'alpha_wealth')
    buy_sell_path = os.path.join(const.TEMP_PATH, '20170409_test', 'buy_sell_record')

    if not os.path.isdir(buy_sell_path):
        os.makedirs(buy_sell_path)

    tag = 'test'


    def multi_process_wealth_series(portfolio_info):
        hday = portfolio_info['hday']
        sr = portfolio_info['sr']
        p = portfolio_info['p']
        return calculate_raw_alpha_wealth_series_record(hday, sr, input_report_path, raw_wealth_path, alpha_wealth_path,
                                                        buy_sell_path, tag, p)


    pool = pathos.multiprocessing.ProcessingPool(multiprocessing.cpu_count() - 2)

    import time

    start_time = time.time()
    # calculate_raw_alpha_wealth_series(5, 1, input_report_path, raw_wealth_path, alpha_wealth_path, tag, 15)
    # print(time.time() - start_time)

    parameter_list = []
    for hday in [5, 10, 12, 15, 20]:
        for sr in [1, 2, 3, 4, 5]:
            for p in portfolio_range:
                parameter_list.append({'hday': hday, 'sr': sr, 'p': p})

    pool.map(multi_process_wealth_series, parameter_list)
    print(time.time() - start_time)
