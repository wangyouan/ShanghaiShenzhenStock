#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step4_merge_result_together_and_find_best_result
# @Date: 2017-04-08
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


import os
import datetime

import pandas as pd
import pathos

from ChineseStock.constants import Constant as const
# from ChineseStock.utilities.calc_util import get_max_draw_down, get_annualized_return
# from ChineseStock.utilities.plot_picture import plot_multiline_picture_text
from ChineseStock.utilities.data_util import generate_review_strategies

# Step1 merge forecast, forecast run up and insider data
save_result_path = os.path.join(const.RESULT_PATH, 'iegt2_f_fr_learning')

# read forecast and forecast run up result
f_fr_raw_df = pd.read_pickle(os.path.join(const.RESULT_PATH, 'forecast_learning_result',
                                          'merged_forecast_raw_drop_unuseful.p'))
f_fr_alpha_df = pd.read_pickle(os.path.join(const.RESULT_PATH, 'forecast_learning_result',
                                            'merged_forecast_alpha_drop_unuseful.p'))

# read insider exe gt2 data
iegt2_raw_df = pd.read_pickle(os.path.join(const.RESULT_PATH, 'insider_exe_gt2_learn',
                                           '20170407_merged_raw_data_after_13.p'))
iegt2_alpha_df = pd.read_pickle(os.path.join(const.RESULT_PATH, 'insider_exe_gt2_learn',
                                             '20170407_merged_alpha_data_after_13.p'))

raw_df = pd.merge(f_fr_raw_df, iegt2_raw_df, left_index=True, right_index=True)
alpha_df = pd.merge(f_fr_alpha_df, iegt2_alpha_df, left_index=True, right_index=True)

raw_df = raw_df[raw_df.index >= datetime.datetime(2013, 1, 1)]
alpha_df = alpha_df[alpha_df.index >= datetime.datetime(2013, 1, 1)]

raw_df.to_pickle(os.path.join(save_result_path, '20170409_no_learning_raw_data.p'))
alpha_df.to_pickle(os.path.join(save_result_path, '20170409_no_learning_alpha_data.p'))

