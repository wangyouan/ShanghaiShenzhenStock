#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step1_generate_insider_learning
# @Date: 2017-04-07
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime

import pandas as pd
from xvfbwrapper import Xvfb

from ChineseStock.constants import Constant as const
from ChineseStock.utilities.data_util import merge_result_data_path, generate_review_strategies
from ChineseStock.utilities.plot_picture import plot_multiline_picture_text

# step1 merge insider and insider runup data
insider_result_path = os.path.join(const.RESULT_PATH, 'insider_exe_gt2')
insider_runup_result_path = os.path.join(const.RESULT_PATH, 'insider_exe_gt2_runup')

save_result_path = os.path.join(const.RESULT_PATH, 'insider_exe_gt2_learn')

if not os.path.isdir(save_result_path):
    os.makedirs(save_result_path)

insider_alpha_df, insider_raw_df = merge_result_data_path(insider_result_path)
insider_runup_alpha_df, insider_runup_raw_df = merge_result_data_path(insider_runup_result_path)

insider_alpha_data = pd.merge(insider_alpha_df, insider_runup_alpha_df, left_index=True, right_index=True)
insider_raw_data = pd.merge(insider_raw_df, insider_runup_raw_df, left_index=True, right_index=True)

tmp_df = pd.DataFrame(insider_raw_data.keys(), columns=['strategy'])
tmp_df['portfolio_num'] = tmp_df['strategy'].apply(lambda x: int(x.split('_')[1][:-1]))
meet_strategies = tmp_df[tmp_df.portfolio_num >= 25].strategy

insider_alpha_data = insider_alpha_data[meet_strategies]
insider_raw_data = insider_raw_data[meet_strategies]

insider_alpha_data.to_pickle(os.path.join(save_result_path, '20170407_merged_alpha_data.p'))
insider_raw_data.to_pickle(os.path.join(save_result_path, '20170407_merged_raw_data.p'))

insider_alpha_data = insider_alpha_data[insider_alpha_data.index >= datetime.datetime(2013, 1, 1)]
insider_raw_data = insider_raw_data[insider_raw_data.index >= datetime.datetime(2013, 1, 1)]

insider_alpha_data.to_pickle(os.path.join(save_result_path, '20170407_merged_alpha_data_after_13.p'))
insider_raw_data.to_pickle(os.path.join(save_result_path, '20170407_merged_raw_data_after_13.p'))

# Step2 Generate Learning Series
alpha_df = insider_alpha_data
raw_df = insider_raw_data

vdisplay = Xvfb(1366, 768)
vdisplay.start()
base_df_type = 'raw'
go_over_list = []

for r in range(1, 7):
    for f in range(1, r + 1):
        go_over_list.append((r, f))

alpha_learning_df = pd.DataFrame(index=alpha_df.index)
raw_learning_df = pd.DataFrame(index=raw_df.index)

for review, forward in go_over_list:
    print(datetime.datetime.today(), review, forward)
    name = 'learning_r{}_f{}_{}'.format(review, forward, base_df_type)

    alpha_series, raw_series = generate_review_strategies(alpha_df, raw_df, base_df_type=base_df_type,
                                                          review=review, forward=forward)

    plot_multiline_picture_text(name, [raw_series, alpha_series],
                                ['Raw Strategy', 'Alpha Strategy'],
                                save_path=os.path.join(save_result_path, '{}.png'.format(name)),
                                stop_loss_rate='NaN')

    alpha_learning_df[name] = alpha_series
    raw_learning_df[name] = raw_series

alpha_learning_df.to_pickle(os.path.join(save_result_path, '20170407_alpha_learning.p'))
raw_learning_df.to_pickle(os.path.join(save_result_path, '20170407_raw_learning.p'))

vdisplay.stop()
