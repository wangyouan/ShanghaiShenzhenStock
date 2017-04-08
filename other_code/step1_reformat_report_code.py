#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step1_reformat_report_code
# @Date: 2017-04-08
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd

root_path = '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen'
data_path = os.path.join(root_path, 'data')
input_report_data_path = os.path.join(data_path, 'report_data')
forecast_runup_path = os.path.join(input_report_data_path, 'report_data_20170303', 'forecast_run_up')
# forecast_report = os.path.join(input_report_data_path, 'report_data_20170224', 'forecast_report')
# insider_exe_gt2_path = os.path.join(input_report_data_path, 'report_data_20170228', 'insider_exe_gt_2')
insider_exe_gt2_runup_path = os.path.join(input_report_data_path, 'report_data_20170303', 'insider_exe_gt2_runup')
save_path = os.path.join(input_report_data_path, 'report_data_20170408')


# Step1 read insider exe gt2 runup and forcast_runup data
def sort_input_report(report_path):
    file_list = os.listdir(report_path)

    df_list = []

    for f in file_list:
        if not f.endswith('.p'):
            continue

        tmp_df = pd.read_pickle(os.path.join(report_path, f))

        tmp_df = tmp_df.rename(index=str, columns={'market_ticker': 'tic', 'anndate': 'date'})
        tmp_df = tmp_df.drop(['type', 'relation'], axis=1)
        df_list.append(tmp_df)

    return pd.concat(df_list, axis=0, ignore_index=True)


insider_exe_gt2_runup_df = sort_input_report(insider_exe_gt2_runup_path)
forecast_runup_df = sort_input_report(forecast_runup_path)

insider_exe_gt2_runup_df.to_pickle(os.path.join(save_path, 'insider_exe_gt2_runup.p'))
forecast_runup_df.to_pickle(os.path.join(save_path, 'forecast_runup.p'))
