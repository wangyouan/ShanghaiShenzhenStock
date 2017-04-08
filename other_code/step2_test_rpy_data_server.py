#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step2_test_rpy_data_server
# @Date: 2017-04-08
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

from xmlrpc.server import SimpleXMLRPCServer

from ChineseStock.constants import Constant
from ChineseStock.data_rpc_server import DataRpcServer

server = SimpleXMLRPCServer(('localhost', Constant.data_server_port))
server.register_instance(DataRpcServer(Constant.STOCK_PRICE_20170408_FILE))
server.serve_forever()
