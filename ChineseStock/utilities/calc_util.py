#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: calc_util
# @Date: 2017-04-07
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import numpy as np

from ChineseStock.constants import Constant as const
from ChineseStock.utilities.date_util import date_as_float


def get_annualized_return(df, df_type=None):
    """ input should be wealth own_report_df """
    if df_type is None:
        df_type = const.WEALTH_DATAFRAME

    if df_type == const.WEALTH_DATAFRAME:
        start_date = df.first_valid_index()
        end_date = df.last_valid_index()
        return (df.ix[end_date] / df.ix[start_date]) ** (
            1 / (date_as_float(end_date) - date_as_float(start_date))) - 1

    elif df_type == const.RETURN_DATAFRAME:
        wealth_df = (df + 1).cumprod()
        return get_annualized_return(wealth_df, df_type=const.WEALTH_DATAFRAME)

    else:
        raise ValueError('Unknown dataframe type {}'.format(df_type))


def get_sharpe_ratio(df, df_type=None, working_days=None):
    """ Input should be return own_report_df """
    if df_type is None:
        df_type = const.RETURN_DATAFRAME

    if working_days is None:
        working_days = const.working_days

    if df_type == const.RETURN_DATAFRAME:
        return df.mean() / df.std() * np.sqrt(working_days)

    elif df_type == const.WEALTH_DATAFRAME:
        return_df = (df - df.shift(1)) / df.shift(1)
        # return_df.loc[return_df.first_valid_index(), :] = 0.0
        return get_sharpe_ratio(return_df, df_type=const.RETURN_DATAFRAME, working_days=working_days)

    else:
        raise ValueError('Unknown dataframe type {}'.format(df_type))


def get_max_draw_down(data_series):
    max_wealth = data_series[0]
    draw_back_rate = float('-inf')

    for i in data_series[1:]:
        draw_back_rate = max(draw_back_rate, 1 - i / max_wealth)
        max_wealth = max(max_wealth, i)

    return draw_back_rate
