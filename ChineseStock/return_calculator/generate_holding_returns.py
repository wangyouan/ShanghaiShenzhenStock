#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: generate_holding_returns
# @Date: 2017-04-09
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os

import pandas as pd
import numpy as np

from ChineseStock.constants import Constant
from ChineseStock.utilities.data_util import calculate_trade_info
from ChineseStock.utilities.multi_process_util import parallel_pandas


class GenerateHoldingReturns(Constant):
    def __init__(self, save_path, input_report_path):
        self._save_path = save_path
        self._input_report = pd.read_pickle(input_report_path)

    def calculate_return_date(self, hday, sr, over=False):
        """
        Get return report
        :param hday: holding days
        :param sr: stop loss rate
        :param over: need to override files or not
        :return: None
        """
        save_file_name = 'hday{}_sr{}.p'.format(hday, sr)

        trading_days_list = pd.read_pickle(self.TRADING_DAYS_20170228_FILE)

        if not over and os.path.isfile(os.path.join(self._save_path, save_file_name)):
            return

        def calculate_return(tmp_df):
            result_df = tmp_df.copy()
            for key in [self.REPORT_BUY_DATE, self.REPORT_BUY_TYPE, self.REPORT_BUY_PRICE,
                        self.REPORT_SELL_DATE, self.REPORT_SELL_PRICE, self.REPORT_SELL_TYPE]:
                result_df.loc[:, key] = np.nan
            for i in tmp_df.index:
                row_info = tmp_df.ix[i]
                tic = row_info[self.TICKER]
                date = row_info[self.DATE]

                return_dict = calculate_trade_info(date, tic, sr, hday, trading_days_list,
                                                   self.stock_buy_type, self.stock_sell_type,
                                                   self.stock_sell_type2)
                for key in return_dict:
                    result_df.loc[:, key] = return_dict[key]

            return result_df

        grouped_df = self._input_report.groupby(self._input_report.index)
        return_input_report = parallel_pandas(grouped_df, calculate_return)

        return_input_report.to_pickle(os.path.join(self._save_path, save_file_name))


if __name__ == '__main__':
    report_path = '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen/data/report_data/report_data_20170409'
    report_data_file = os.path.join(report_path, 'Insider_purchase_event_list_2017_4_9.p')
    save_path = '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen/temp/20170409_test'

    tmp = GenerateHoldingReturns(save_path, report_data_file)

    for hday in [5, 10, 12, 15, 20]:
        for sr in [1, 2, 3, 4, 5]:
            sr_rate = -float(sr) / 100
            tmp.calculate_return_date(hday, sr_rate)
