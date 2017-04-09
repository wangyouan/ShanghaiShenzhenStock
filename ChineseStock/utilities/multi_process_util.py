#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: multi_process_util
# @Date: 2017-04-09
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import multiprocessing

import pandas as pd
import pathos


def parallel_pandas(dfGrouped, func):
    pool = pathos.multiprocessing.ProcessingPool(multiprocessing.cpu_count() - 2)

    dfs = [df for name, df in dfGrouped]

    result_dfs = pool.map(func, dfs)

    return pd.concat(result_dfs)
