# -*- coding:utf-8 -*-
import os

class config:

    CWD = os.getcwd()
    SUFFIX = '' if 'pinyin' in CWD else './'
    GRPC_HOST_LIST = ['localhost:47260']
    LOG_PATH = './logs/server.log'
    
