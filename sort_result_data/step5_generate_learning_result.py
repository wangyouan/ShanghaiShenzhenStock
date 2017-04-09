#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step5_generate_learning_result
# @Date: 2017-04-09
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime
# import multiprocessing

import pandas as pd
# import numpy as np
# import pathos

from ChineseStock.constants import Constant as const
# from ChineseStock.utilities.calc_util import get_max_draw_down, get_annualized_return
# from ChineseStock.utilities.plot_picture import plot_multiline_picture_text
from ChineseStock.utilities.data_util import generate_review_strategies

save_result_path = os.path.join(const.RESULT_PATH, 'iegt2_f_fr_learning')

raw_df = pd.read_pickle(os.path.join(save_result_path, '20170409_no_learning_raw_data.p'))
alpha_df = pd.read_pickle(os.path.join(save_result_path, '20170409_no_learning_alpha_data.p'))

# step2 start to generate learning result
alpha_learning_df = pd.DataFrame(index=alpha_df.index)
raw_learning_df = pd.DataFrame(index=raw_df.index)


def process_information(portfolio_info):
    result_dict = {}

    total_length = len(portfolio_info)

    for j, i in enumerate(portfolio_info):
        review = int(i[0])
        forward = int(i[1])
        base_type = i[2]
        max_method = i[3]

        short_method = ''.join(map(lambda x: x[0], max_method.split('_')))
        name = 'learn_{}_{}_{}r_{}f'.format(base_type, short_method, review, forward)

        alpha_series, raw_series = generate_review_strategies(alpha_df, raw_df, base_df_type=base_type, review=review,
                                                              forward=forward, max_method=max_method)
        result_dict[name] = [alpha_series, raw_series]

        print('{}: {}% finished'.format(datetime.datetime.today(), float(j) / total_length))

    return result_dict


parameter_list = []
for r in range(1, 7):
    for f in range(1, r + 1):
        for base_type in ['alpha', 'raw']:
            for max_method in ['daily_return', 'sharpe_ratio', 'ann_return']:
                parameter_list.append([r, f, base_type, max_method])

# process_num = 4

# pool = pathos.multiprocessing.ProcessingPool(process_num)
# pool = multiprocessing.Pool(4)

# parameter_lists = np.array_split(parameter_list, process_num)

# result_list = pool.map(process_information, parameter_lists)
result = process_information(parameter_list)

# for item in result_list:
for key in result:
    raw_learning_df[key] = result[key][1]
    alpha_learning_df[key] = result[key][0]

alpha_learning_df.to_pickle(os.path.join(save_result_path, '20170409_alpha_learning.p'))
raw_learning_df.to_pickle(os.path.join(save_result_path, '20170409_raw_learning.p'))
