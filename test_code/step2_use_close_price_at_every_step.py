#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: ShanghaiShenzhenStock
# File name: step2_use_close_price_at_every_step
# Author: warn
# Date: 2017/4/11

import os
import multiprocessing

import pandas as pd
import pathos

from ChineseStock.constants import Constant as const
from ChineseStock.return_calculator.generate_holding_returns import calculate_return_data
from ChineseStock.utilities.calc_util import get_annualized_return, get_sharpe_ratio, get_max_draw_down
from ChineseStock.wealth_generator.calculate_wealth_info_equal_portfolio import calculate_raw_alpha_wealth_series_record

portfolio_range = [15, 20, 22, 25, 30]
file_path = '20170411_test_equal_portfolio'
input_report_path = os.path.join(const.TEMP_PATH, file_path, 'input_return_report')
raw_wealth_path = os.path.join(const.TEMP_PATH, file_path, 'raw_wealth')
alpha_wealth_path = os.path.join(const.TEMP_PATH, file_path, 'alpha_wealth')
buy_sell_path = os.path.join(const.TEMP_PATH, file_path, 'buy_sell_record')

for path_name in [raw_wealth_path, alpha_wealth_path, buy_sell_path, input_report_path]:
    if not os.path.isdir(path_name):
        os.makedirs(path_name)

tag = 'test'


def multi_process_wealth_series(portfolio_info):
    hday = portfolio_info['hday']
    sr = portfolio_info['sr']
    p = portfolio_info['p']
    return calculate_raw_alpha_wealth_series_record(hday, sr, input_report_path, raw_wealth_path, alpha_wealth_path,
                                                    buy_sell_path, tag, p)


if __name__ == '__main__':
    import time

    report_file = '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen/data/report_data/report_data_20170409'
    report_data_file = os.path.join(report_file, 'Insider_purchase_event_list_2017_4_9.p')
    report_file = pd.read_pickle(report_data_file)

    start_time = time.time()

    for hday in [5, 10, 12, 15, 20]:
        for sr in [1, 2, 3, 4, 5]:
            sr_rate = -float(sr) / 100
            calculate_return_data(hday, sr_rate, over=True, report_df=report_file,
                                  save_path=input_report_path)

    pool = pathos.multiprocessing.ProcessingPool(multiprocessing.cpu_count() - 2)
    # calculate_raw_alpha_wealth_series(5, 1, input_report_path, raw_wealth_path, alpha_wealth_path, tag, 15)
    # print(time.time() - start_time)

    parameter_list = []
    for hday in [5, 10, 12, 15, 20]:
        for sr in [1, 2, 3, 4, 5]:
            for p in portfolio_range:
                parameter_list.append({'hday': hday, 'sr': sr, 'p': p})

    pool.map(multi_process_wealth_series, parameter_list)

    file_list = os.listdir(raw_wealth_path)
    df = pd.read_pickle(os.path.join(raw_wealth_path, file_list[0]))

    result_df = pd.DataFrame(index=df.index)

    for f in file_list:
        df = pd.read_pickle(os.path.join(raw_wealth_path, f))
        col_name = f[:-2]
        result_df[col_name] = df

    result_df.to_excel(os.path.join(const.TEMP_PATH, file_path, '20170410_insider_test_result.xlsx'))
    sta_df = pd.DataFrame(columns=result_df.keys())
    sta_df.loc[const.SHARPE_RATIO] = get_sharpe_ratio(result_df, const.WEALTH_DATAFRAME)
    sta_df.loc[const.ANNUALIZED_RETURN] = get_annualized_return(result_df, const.WEALTH_DATAFRAME)
    sta_df.loc['max_drawdown'] = result_df.apply(get_max_draw_down)

    sta_df.to_excel(os.path.join(const.TEMP_PATH, file_path, '20170410_insider_test_statistics.xlsx'))

    print(time.time() - start_time)
