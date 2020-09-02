# -*- coding:utf-8 -*-
import os

class config:

    CWD = os.getcwd()
    SUFFIX = '' if 'pinyin' in CWD else './'
    GRPC_HOST_LIST = ['127.0.0.1:47260', '127.0.0.1:47261']
    
