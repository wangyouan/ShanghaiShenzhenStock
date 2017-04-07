#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: data_util
# @Date: 2017-04-07
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import os
import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd


def merge_result_data_path(result_path):
    dir_list = os.listdir(result_path)

    for dir_name in dir_list:
        if not dir_name.startswith('cost'):
            continue

        current_path = os.path.join(result_path, dir_name)

        if not os.path.isdir(current_path):
            continue

        file_list = os.listdir(current_path)

        alpha_df_list = []
        raw_df_list = []

        for file_name in file_list:
            if file_name.endswith('alpha.p'):
                alpha_df_list.append(pd.read_pickle(os.path.join(current_path, file_name)))

            elif file_name.endswith('raw.p'):
                raw_df_list.append(pd.read_pickle(os.path.join(current_path, file_name)))

        if alpha_df_list:
            alpha_df = pd.concat(alpha_df_list, axis=1)

        else:
            alpha_df = pd.DataFrame()

        if raw_df_list:
            raw_df = pd.concat(raw_df_list, axis=1)

        else:
            raw_df = pd.DataFrame()

        return alpha_df, raw_df


def generate_review_strategies(alpha_data, raw_data, base_df_type='alpha', review=6, forward=6):
    daily_alpha_return = alpha_data / alpha_data.shift(1) - 1
    daily_raw_return = raw_data / raw_data.shift(1) - 1

    date_index = alpha_data.index

    # start_date = datetime.datetime(year=date_index[0].year, month=date_index[0].month, day=1)
    start_date = datetime.datetime(year=date_index[0].year, month=date_index[0].month, day=1)
    middle_date = start_date + relativedelta(months=review)
    end_date = start_date + relativedelta(months=(review + forward))

    if end_date > date_index[-1]:
        end_date = date_index[-1] + relativedelta(days=1)

    if base_df_type == 'alpha':
        base_df = daily_alpha_return

    else:
        base_df = daily_raw_return

    learning_alpha_series = pd.Series(index=date_index)
    learning_raw_series = pd.Series(index=date_index)

    while middle_date < date_index[-1]:
        trading_index = date_index[date_index >= start_date]
        trading_index = trading_index[trading_index < middle_date]

        filling_index = date_index[date_index < end_date]
        filling_index = filling_index[filling_index >= middle_date]

        sub_learning_strategy_name = base_df.loc[trading_index].mean().idxmax()

        learning_alpha_series.loc[filling_index] = daily_alpha_return.loc[filling_index, sub_learning_strategy_name]
        learning_raw_series.loc[filling_index] = daily_raw_return.loc[filling_index, sub_learning_strategy_name]

        middle_date = end_date
        start_date = middle_date - relativedelta(months=review)
        end_date = middle_date + relativedelta(months=forward)

        if end_date > date_index[-1]:
            end_date = date_index[-1] + relativedelta(days=1)

    learning_alpha_wealth = (learning_alpha_series.fillna(0) + 1).cumprod() * 10000
    learning_raw_wealth = (learning_raw_series.fillna(0) + 1).cumprod() * 10000

    return learning_alpha_wealth, learning_raw_wealth
