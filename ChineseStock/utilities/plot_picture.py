#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: plot_picture
# @Date: 2017-04-07
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from ChineseStock.constants import Constant as const
from ChineseStock.utilities.calc_util import get_sharpe_ratio, get_annualized_return, get_max_draw_down


def plot_multiline_alpha(data_list, legend_list, picture_title, picture_save_path, text1, text2):
    """ Draw data series info """

    # plot file and save picture
    fig = plt.figure(figsize=(15, 8))

    left = 0.1
    bottom = 0.3
    width = 0.75
    height = 0.60
    ax = fig.add_axes([left, bottom, width, height])
    ax.set_title(picture_title)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.figtext(0.01, 0.01, text1, horizontalalignment='left')
    plt.figtext(0.51, 0.01, text2, horizontalalignment='left')

    date_series = data_list[0].index

    color_list = ['r-', 'b-', 'y-', 'g-']

    for i, data_series in enumerate(data_list):
        # get data series info
        plt.plot(date_series, data_series, color_list[i], label=legend_list[i])

    min_date = date_series[0]
    max_date = date_series[-1]
    plt.gca().set_xlim(min_date, max_date)
    plt.legend(loc=0)
    fig.autofmt_xdate()
    # fig.suptitle(picture_title)

    # print dir(fig)
    fig.savefig(picture_save_path)
    plt.close()


def plot_multiline_picture_text(pic_title, data_list, legends, save_path, stop_loss_rate):
    line1 = 'Transaction cost 0.2% SR {}%'.format(stop_loss_rate)

    info_list = [line1]

    raw_strategy = data_list[0]
    alpha_strategy = data_list[1]

    time_period = ['all', '13_16', 'after_16']
    period_list = [(None, None),
                   (datetime.datetime(2013, 7, 22), datetime.datetime(2016, 7, 20)),
                   (datetime.datetime(2016, 2, 1), None)]

    def generate_line_info(i, date_tuple):
        current_line = 'Date {}'.format(time_period[i])
        result_list = [current_line]

        def get_line_not_alpha(data_series, prefix_info):
            if date_tuple[0] is not None:
                sub_data_series = data_series[data_series.index > date_tuple[0]]
            else:
                sub_data_series = data_series

            if date_tuple[1] is not None:
                sub_data_series = sub_data_series[sub_data_series.index < date_tuple[1]]

            sharpe_ratio = get_sharpe_ratio(sub_data_series, df_type=const.WEALTH_DATAFRAME)
            ann_return = get_annualized_return(sub_data_series, df_type=const.WEALTH_DATAFRAME) * 100
            max_draw_down = get_max_draw_down(sub_data_series) * 100

            current_line = '{}: Sharpe Ratio {:.3f}, Annualized Return {:.2f}%, Max Drawdown rate {:.2f}%'.format(
                prefix_info, sharpe_ratio, ann_return, max_draw_down
            )
            return current_line

        for prefix in ['Raw', 'Alpha']:

            if prefix == 'Raw':
                result_list.append(get_line_not_alpha(raw_strategy, prefix))

            else:
                result_list.append(get_line_not_alpha(alpha_strategy, prefix))

        return result_list

    for i, date_tuple in enumerate(period_list[:2]):
        info_list.extend(generate_line_info(i, date_tuple))

    text1 = '\n'.join(info_list)

    info_list = []
    for i, date_tuple in enumerate(period_list[2:]):
        info_list.extend(generate_line_info(i + 2, date_tuple))

    text2 = '\n'.join(info_list)

    plot_multiline_alpha(data_list,
                         legend_list=legends,
                         picture_title=pic_title,
                         picture_save_path=save_path,
                         text1=text1, text2=text2)
