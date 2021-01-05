# -*- coding:utf-8 -*-
'''
-------------------------------------------------
   Description :  TTSSegPause [专为标贝数据格式：卡尔普#2陪外孙#1玩滑梯#4。]
   Author :       liupeng
   Date :         2020-08-26
-------------------------------------------------

'''

import re 
import os
import jieba
import logging
import pandas as pd
from conf.config import config 


class TTSSegPause():
    def __init__(self):
        jieba.load_userdict( config.MY_DICT ) 
        self.zh_pattern = re.compile(config.ch_regex)
        self.words_dict = self._gen_words_mapping()

    @staticmethod
    def _gen_words_mapping():
        words_mapping_df = pd.read_csv(config.WORDS_MAPPING_PATH)
        words_dict = {}
        for per_en_name,per_ch_name in zip(words_mapping_df['en_name'].values, words_mapping_df['ch_name'].values):
            words_dict[ str(per_en_name).lower() ] = str(per_ch_name)
        return words_dict
    
    def _is_zh(self, word):
        match = self.zh_pattern.search(word)
        return match is not None
    
    def add_pause(self, text):
        text = self.preprocess(text)
        seg_list = list( jieba.cut( text ) )
        new_text = ""
        if seg_list !=[]:
            for index, per_seg in enumerate(seg_list):
                if (self._is_zh(per_seg)) and (index!=len(seg_list)-1):
                    new_text = new_text + per_seg
                    #if len(per_seg) >1:
                    #    new_text = new_text + per_seg + "#2"
                    #else:
                    #    new_text = new_text + per_seg + "#1"
                elif (self._is_zh(per_seg)) and (index==len(seg_list)-1):
                    new_text = new_text + per_seg
                else:
                    new_text = new_text + "#3" + per_seg   #标点
        else:
            return ""
        if self._is_zh(new_text[-1])==False:
            new_text = new_text[:-3] + new_text[-1]
        return new_text

    def preprocess(self, text):
        text = text.lower()
        for per_en_name,per_ch_name in self.words_dict.items():
            text = text.replace(per_en_name, per_ch_name)
        text = text.replace(" ", "")
        digit_list = re.findall("\d+(?:\.\d+)?",text) 
        for per_digit in digit_list:
            text = text.replace(per_digit, self.float_to_words( per_digit ) )
        return text
    

    def int_to_words(self, astr):

        res = ''
        i = len(astr) - 1
        zero_occur = False 
        i = 0 
        flag = True 

        while i < len(astr):
            j = len(astr) - 1 - i 
            if astr[i] == '0':
                zero_occur = True 
            else:
                if zero_occur:
                    res = res + '零'
                zero_occur = False 

                if not (astr[i] == '1' and len(astr) == 2 and j % 4 == 1):
                    res = res + config.digit[astr[i]]

                res = res + config.amap2[j % 4]

            if j % 4 == 0 and j // 4 > 0:
    
                res = res + config.amap1[j // 4]
                if flag:
                    res = res + '，'

                zero_occur = False 

            i += 1
	
        aastr = astr 
        for i in range(len(astr)-1, -1, -4):
            if i != len(astr) - 1:
                aastr = aastr[:i+1] + ', ' + aastr[i+1:]

        return res 


    def digit_to_words(self, astr):
	    digit = config.digit
	    digit['.'] = '点'
	    res = ''
	    for ch in astr:
	    	res = res + digit[ch]

	    return res 


    def float_to_words(self, astr):
        if '.' in astr:
	        part1, part2 = astr.split('.')
	        return self.int_to_words(part1) + '点' + self.digit_to_words(part2)
        else:
            return self.int_to_words(astr)
    
