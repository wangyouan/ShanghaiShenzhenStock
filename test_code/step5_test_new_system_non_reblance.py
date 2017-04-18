#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: ShanghaiShenzhenStock
# File name: step5_test_new_system_non_reblance
# Author: warn
# Date: 2017/4/18


import os
import multiprocessing

import pandas as pd
import pathos

from ChineseStock.constants import Constant as const
from ChineseStock.return_calculator.generate_holding_returns_20170417 import calculate_return_data
from ChineseStock.utilities.calc_util import get_annualized_return, get_sharpe_ratio, get_max_draw_down
from ChineseStock.wealth_generator.calculate_wealth_info_20170417 import calculate_raw_alpha_wealth_series_record

portfolio_range = [15, 20, 22, 25, 30]
hday_list = [5, 10, 12, 15, 20]
sr_list = range(1, 6)
file_path = '20170418_non_reblance'
is_reblance = False
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
                                                    buy_sell_path, tag, p, is_reblance)


if __name__ == '__main__':
    import time

    # report_file = '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen/data/report_data/report_data_20170409'
    report_file = os.path.join(const.REPORT_DATA_PATH, 'report_data_20170409')
    report_data_file = os.path.join(report_file, 'Insider_purchase_event_list_2017_4_9.p')
    report_file = pd.read_pickle(report_data_file)

    start_time = time.time()

    for hday in hday_list:
        for sr in sr_list:
            sr_rate = -float(sr) / 100
            calculate_return_data(hday, sr_rate, over=True, report_df=report_file,
                                  save_path=input_report_path)

    pool = pathos.multiprocessing.ProcessingPool(multiprocessing.cpu_count() - 2)

    parameter_list = []
    for hday in hday_list:
        for sr in sr_list:
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

    result_df.to_excel(os.path.join(const.TEMP_PATH, file_path, '20170418_insider_reblance_test_result.xlsx'))
    sta_df = pd.DataFrame(columns=result_df.keys())
    sta_df.loc[const.ANNUALIZED_RETURN] = get_annualized_return(result_df, const.WEALTH_DATAFRAME)
    sta_df.loc[const.SHARPE_RATIO] = get_sharpe_ratio(result_df, const.WEALTH_DATAFRAME)
    sta_df.loc['max_drawdown'] = result_df.apply(get_max_draw_down)

    sta_df.to_excel(os.path.join(const.TEMP_PATH, file_path, '20170418_insider_reblance_test_statistics.xlsx'))

    print(time.time() - start_time)
