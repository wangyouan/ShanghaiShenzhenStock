#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: os_related
# @Date: 2017-04-07
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


import os


def get_root_path():
    if hasattr(os, 'uname'):
        if os.uname()[1] == 'ewin3102':
            return '/home/zigan/Documents/WangYouan/trading/ChineseStock'
        elif os.uname()[0] == 'Darwin':
            return '/Users/warn/PycharmProjects/QuestionFromProfWang/ChineseStock'
        else:
            return '/home/wangzg/Documents/WangYouan/Trading/ShanghaiShenzhen'
    else:
        return r'C:\Users\CFID\Documents\ChinaStock'


def get_process_num():
    if hasattr(os, 'uname'):
        if os.uname()[1] == 'ewin3102':
            return 38
        else:
            return 18
    else:
        return 38


def make_dirs(dir_or_dirs):
    for dir_path in dir_or_dirs:
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)


def get_target_file_name(target_path, keyword, suffix):
    current_path_files = os.listdir(target_path)
    for file_name in current_path_files:
        if keyword in file_name and file_name.endswith(suffix):
            return file_name

    else:
        return None
