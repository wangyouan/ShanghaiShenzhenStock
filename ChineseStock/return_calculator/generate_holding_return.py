#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: generate_holding_return
# @Date: 2017-04-09
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import multiprocessing
# import shutil

import pathos
import dill
import pandas as pd
import numpy as np

from ChineseStock.constants import Constant as const


# from ChineseStock.utilities.multi_process_util import parallel_pandas

def run_dill_encoded(payload):
    fun, args = dill.loads(payload)
    return fun(*args)


def calculate_trade_info(date, stock_data, sr, hday, tdays,
                         buy_type=const.STOCK_OPEN_PRICE, sell_type=const.STOCK_CLOSE_PRICE,
                         sell_type2=const.STOCK_OPEN_PRICE):
    """
    This function used to calculate stock trading info stock price would be read from hard disk
    :param date: information announce date
    :param stock_data: stock price data
    :param sr: stop loss rate
    :param hday: the days of holding
    :param buy_type: use which price as buy
    :param sell_type: use which price as sell
    :param sell_type2: if target date is not trading day, use which price to sell
    :param sell_date: sell_date of target stock
    :return: a dict of temp result
    """
    temp_result = {const.REPORT_SELL_TYPE: np.nan, const.REPORT_SELL_DATE: np.nan,
                   const.REPORT_BUY_DATE: np.nan, const.REPORT_SELL_PRICE: np.nan,
                   const.REPORT_BUY_PRICE: np.nan, const.REPORT_BUY_TYPE: buy_type}

    # Get buy day
    trading_days = tdays[tdays > date].tolist()

    # not enough days to hold this stock
    if len(trading_days) < hday:
        return temp_result
    buy_date = trading_days[0]

    if buy_date not in stock_data.index:
        return temp_result

    buy_price = stock_data.ix[buy_date, buy_type]
    if stock_data.ix[buy_date, const.STOCK_VOLUME] < 1:
        return temp_result
    temp_result[const.REPORT_BUY_PRICE] = buy_price
    temp_result[const.REPORT_BUY_DATE] = buy_date
    sell_date = trading_days[hday - 1]
    highest_prc = stock_data.ix[buy_date, const.STOCK_CLOSE_PRICE]

    for day in trading_days[1:]:
        if day in stock_data.index:
            sell_info = stock_data.ix[day]
            if sell_info[const.STOCK_VOLUME] < 1:
                continue
            clc_prc = sell_info[const.STOCK_CLOSE_PRICE]
            rate = (clc_prc / highest_prc - 1) * 100 + sr
            if day > sell_date:
                temp_result[const.REPORT_SELL_PRICE] = sell_info[sell_type2]
                temp_result[const.REPORT_SELL_TYPE] = sell_type2
                temp_result[const.REPORT_SELL_DATE] = day
                return temp_result

            elif day == sell_date or rate < 0:
                temp_result[const.REPORT_SELL_PRICE] = sell_info[sell_type]
                temp_result[const.REPORT_SELL_TYPE] = sell_type
                temp_result[const.REPORT_SELL_DATE] = day
                return temp_result

            highest_prc = max(highest_prc, sell_info[const.STOCK_CLOSE_PRICE])

    return temp_result


def calculate_return_data(hday, sr, report_df, save_path, over=False):
    """
    Get return report
    :param hday: holding days
    :param sr: stop loss rate
    :param over: need to override files or not
    :param report_df: report data file used in this test
    :return: None
    """
    save_file_name = 'hday{}_sr{}.p'.format(hday, int(abs(sr) * 100))

    trading_days_list = pd.read_pickle(const.TRADING_DAYS_20170228_FILE)

    if os.path.isfile(os.path.join(save_path, save_file_name)):
        if not over:
            return
            # else:
            # os.remove(os.path.join(save_path, save_file_name))

    def calculate_return(tmp_df):
        result_df = tmp_df.copy()
        for key in [const.REPORT_BUY_DATE, const.REPORT_BUY_TYPE, const.REPORT_BUY_PRICE,
                    const.REPORT_SELL_DATE, const.REPORT_SELL_PRICE, const.REPORT_SELL_TYPE]:
            result_df.loc[:, key] = np.nan

        tic = tmp_df.ix[tmp_df.first_valid_index(), const.TICKER]

        stock_file_path = os.path.join(const.STOCK_PRICE_TICKER_SEP_PATH_05, '{}.p'.format(tic))

        if os.path.isfile(stock_file_path):
            stock_data = pd.read_pickle(stock_file_path)

            for i in tmp_df.index:
                date = tmp_df.ix[i, const.DATE]

                return_dict = calculate_trade_info(date, stock_data, sr, hday, trading_days_list,
                                                   const.stock_buy_type, const.stock_sell_type,
                                                   const.stock_sell_type2)
                for key in return_dict:
                    result_df.loc[i, key] = return_dict[key]

        return result_df

    grouped_df = report_df.groupby(const.TICKER)
    dfs = [df for index, df in grouped_df]
    pool = pathos.multiprocessing.ProcessingPool(multiprocessing.cpu_count() - 2)
    result_dfs = pool.map(calculate_return, dfs)
    return_input_report = pd.concat(result_dfs)

    for key in [const.REPORT_SELL_DATE, const.REPORT_BUY_DATE]:
        return_input_report[key] = pd.to_datetime(return_input_report[key])

    return_input_report.dropna(subset=[const.REPORT_SELL_PRICE]).to_pickle(os.path.join(save_path, save_file_name))


if __name__ == '__main__':
    report_file = '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen/data/report_data/report_data_20170409'
    report_data_file = os.path.join(report_file, 'Insider_purchase_event_list_2017_4_9.p')
    save_path = '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen/temp/20170409_test/input_return_report2'
    report_file = pd.read_pickle(report_data_file)

    for hday in [5, 10, 12, 15, 20]:
        for sr in [1, 2, 3, 4, 5]:
            calculate_return_data(hday, sr, over=True, report_df=report_file,
                                  save_path=save_path)
