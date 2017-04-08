#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step3_find_best_strategies_of_insider
# @Date: 2017-04-07
# @Author: Mark Wang
# @Email: wangyouan@gmial.com



import os
import datetime

import pandas as pd
from xvfbwrapper import Xvfb

from ChineseStock.constants import Constant as const
from ChineseStock.utilities.calc_util import get_max_draw_down, get_annualized_return
from ChineseStock.utilities.plot_picture import plot_multiline_picture_text

# Step1 merge original data and learning data
learning_path = os.path.join(const.RESULT_PATH, 'insider_exe_gt2_learn')
ori_alpha_df = pd.read_pickle(os.path.join(learning_path, '20170407_merged_alpha_data_after_13.p'))
l_alpha_df = pd.read_pickle(os.path.join(learning_path, '20170407_alpha_learning.p'))

ori_raw_df = pd.read_pickle(os.path.join(learning_path, '20170407_merged_raw_data_after_13.p'))
l_raw_df = pd.read_pickle(os.path.join(learning_path, '20170407_raw_learning.p'))

alpha_df = pd.merge(ori_alpha_df, l_alpha_df, left_index=True, right_index=True)
raw_df = pd.merge(ori_raw_df, l_raw_df, left_index=True, right_index=True)

alpha_df = alpha_df[alpha_df.index >= datetime.datetime(2013, 1, 1)]
raw_df = raw_df[raw_df.index >= datetime.datetime(2013, 1, 1)]

alpha_df.to_pickle(os.path.join(learning_path, '20170407_merged_alpha_learning_result.p'))
raw_df.to_pickle(os.path.join(learning_path, '20170407_merged_raw_learning_result.p'))

# Step 2 find best strategies with max draw down no more than 5%

sub_raw_df = raw_df[raw_df.index >= datetime.datetime(2016, 2, 1)]
raw_df_max_draw_down = sub_raw_df.apply(get_max_draw_down, axis=0)
sub_keys = raw_df_max_draw_down[raw_df_max_draw_down <= 0.05].keys()

raw_df_less_than_5 = sub_raw_df[sub_keys]

ann_return = get_annualized_return(raw_df_less_than_5, const.WEALTH_DATAFRAME)

best_strategies = ann_return.idxmax()

vdisplay = Xvfb()
vdisplay.start()

plot_multiline_picture_text(best_strategies, [raw_df[best_strategies], alpha_df[best_strategies]],
                            ['Raw Strategy', 'Alpha Strategy'],
                            save_path=os.path.join(learning_path, '20170407_best_strategy_after_16.png'),
                            stop_loss_rate='NaN'
                            )

vdisplay.stop()
