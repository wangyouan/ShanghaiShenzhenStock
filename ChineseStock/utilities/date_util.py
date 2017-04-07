#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: date_util
# @Date: 2017-04-07
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import datetime
import calendar


def date_as_float(dt):
    size_of_day = 1. / 366.
    size_of_second = size_of_day / (24. * 60. * 60.)
    days_from_jan1 = dt - datetime.datetime(dt.year, 1, 1)
    if not calendar.isleap(dt.year) and days_from_jan1.days >= 31 + 28:
        days_from_jan1 += datetime.timedelta(1)
    return dt.year + days_from_jan1.days * size_of_day + days_from_jan1.seconds * size_of_second
