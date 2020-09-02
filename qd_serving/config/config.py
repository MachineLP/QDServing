# -*- coding:utf-8 -*-
import os

class config:

    CWD = os.getcwd()
    SUFFIX = '' if 'pinyin' in CWD else './'
    
