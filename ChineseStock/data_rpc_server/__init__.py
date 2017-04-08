#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: __init__.py
# @Date: 2017-04-08
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import datetime

import pandas as pd

from ChineseStock.constants import Constant


class DataRpcServer(Constant):
    def __init__(self, data_file_path):
        self.data_df = pd.read_pickle(data_file_path)

    def load_stock_price(self, date, tic):
        date = datetime.datetime.strptime(date, '%Y%m%d')

        tmp_df = self.data_df[self.data_df[self.DATE] == date]
        tmp_df = tmp_df[tmp_df[self.TICKER] == tic]

        data_json = tmp_df.to_json(path_or_buf=None, orient='records',
                                   date_format='epoch', double_precision=10, force_ascii=True, date_unit='ms')
        return data_json


if __name__ == '__main__':
    from xmlrpc.server import SimpleXMLRPCServer

    server = SimpleXMLRPCServer('http://localhost:{}'.format(Constant.data_server_port))
    server.register_instance(DataRpcServer(Constant.STOCK_PRICE_20170408_FILE))
    server.serve_forever()
