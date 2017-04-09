#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step6_select_best_strategies
# @Date: 2017-04-09
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime
# import multiprocessing

import pandas as pd
from xvfbwrapper import Xvfb
# import numpy as np
# import pathos

from ChineseStock.constants import Constant as const
from ChineseStock.utilities.calc_util import get_max_draw_down, get_annualized_return, get_sharpe_ratio
from ChineseStock.utilities.plot_picture import plot_multiline_picture_text
# from ChineseStock.utilities.data_util import generate_review_strategies

save_result_path = os.path.join(const.RESULT_PATH, 'iegt2_f_fr_learning')

raw_df = pd.read_pickle(os.path.join(save_result_path, '20170409_no_learning_raw_data.p'))
alpha_df = pd.read_pickle(os.path.join(save_result_path, '20170409_no_learning_alpha_data.p'))

raw_learn_df = pd.read_pickle(os.path.join(save_result_path, '20170409_raw_learning.p'))
alpha_learn_df = pd.read_pickle(os.path.join(save_result_path, '20170409_alpha_learning.p'))

merged_raw_df = pd.merge(raw_df, raw_learn_df, left_index=True, right_index=True)
merged_alpha_df = pd.merge(alpha_df, alpha_learn_df, left_index=True, right_index=True)

def find_best_str_name(base_df, method_type, drawdown_limit=None):

    sub_base_df = base_df[base_df.index >= datetime.datetime(2016, 2, 1)]
    if drawdown_limit is not None:
        base_df_max_draw_down = sub_base_df.apply(get_max_draw_down, axis=0)
        sub_keys = base_df_max_draw_down[base_df_max_draw_down <= drawdown_limit].keys()

        sub_base_df = sub_base_df[sub_keys]

    # annualized return
    if method_type == 'ar':
        sta_df = get_annualized_return(sub_base_df, const.WEALTH_DATAFRAME)

    else:
        sta_df = get_sharpe_ratio(sub_base_df, const.WEALTH_DATAFRAME)

    return sta_df.idxmax()

vdisplay = Xvfb()
vdisplay.start()

tags = ['raw', 'alpha']
for method in ['ar', 'sp']:
    # for i, base_df in enumerate([merged_raw_df, merged_alpha_df]):
    for i, base_df in enumerate([raw_learn_df, alpha_learn_df]):
        save_name = '20170409_best_{}_learn_{}_max_drawdown_5.png'.format(tags[i], method)

        col_name = find_best_str_name(base_df, method, 0.05)

        plot_multiline_picture_text(col_name, [raw_learn_df[col_name], alpha_learn_df[col_name]],
                                    ['Raw Strategy', 'Alpha Strategy'],
                                    save_path=os.path.join(save_result_path, save_name),
                                    stop_loss_rate=None
                                    )



vdisplay.stop()