# -*- coding:utf-8 -*-
'''
-------------------------------------------------
   Description :  TTSPinYin [拼音及多音字处理]
   Author :       liupeng
   Date :         2020-08-26
-------------------------------------------------

'''

import re 
import os
import logging
from conf.config import config 


class TTSPinYin():
    def __init__(self):

        self._init_pinyin()
        self._init_large_pinyin()

    
    def _init_pinyin(self):

        self.hz = {}
        with open(os.path.join(config.SUFFIX, config.PINYIN_TXT), 'r', encoding='utf-8') as f:
            i = 0 
            for line in f:
                if i < 2:
                    i += 1
                    continue 
                line = line.strip()
                line = re.sub(r'\s+', '', line)
                line = line.split(':')[1].split('#')
                word = line[1].strip()
                py = line[0].strip().split(',')
                self.hz[word] = py
    
    def _init_large_pinyin(self):

        self.phrase = {}
        with open(os.path.join(config.SUFFIX, config.LARGE_PINYIN_TXT), 'r', encoding='utf-8') as f:
            i = 0 
            for line in f:
                if i < 2:
                    i += 1
                    continue
        
                line = line.strip().split(':')
                pz = line[0].strip()
                py = line[1].strip().split(' ')
    
                self.phrase[pz[0]] = self.phrase.get(pz[0], [])
                self.phrase[pz[0]].append((pz, py))


    def preprocess(self, text, tone=config.tone):
        if not tone:
            text = re.sub(r'#\d+', '', text)
    
        text = text.lower()
        text = re.sub(r'[）（]', '', text)
        #text = re.sub(r'[0-9]{0,}\.?[0-9]+', '', text)
        text = text.replace('：“', '，').replace('：', '，').replace('”！', '！').replace('”。', '。')
        text = text.replace('……”', '。').replace('……', '。').replace('…。', '。').replace('…”', '。').replace('…', '。').replace('.', '。')
        text = text.replace('”', '').replace('“', '').replace('、', '，').replace('-', '，')
        text = text.replace('—', '，').replace('-', '，').replace('；', '。')
        text = re.sub(r'，[，\s]+', '，', text)
        text = re.sub(r'。[。，\s]+', '。', text)
        text = re.sub(r'，。+', '。', text)

        text = re.sub(r'？[？\s]+', '？', text)
        text = re.sub(r'，？+', '？', text)

        text = re.sub(r'！[！\s]+', '！', text)
        text = re.sub(r'，！+', '！', text)
        text = re.sub('\.+', '。', text)
        text = re.sub(',+', '，', text)
        text = re.sub('!+', '！', text)
        text = re.sub('\?+', '？', text)

        text = re.sub(r'\s+', ' ', text)
        text = text.replace('|', '') 
        text = text.strip()

        '''
        for t in text:
            if not ('\u4e00' <= t <= '\u9fff' or t in ['，', '。', '？', '！'] or t in ['#', '1', '2', '3', '4']):
                print(t, text)
                break 
        '''
        return text 

    def split_pyin(pyin):

        if pyin[:2] in ['ch', 'sh', 'zh']:
            return pyin[:2] + ' ' + pyin[2:]
        elif pyin[0] in ['a', 'e', 'o']:
            return pyin
        elif len(pyin) == 2 and pyin[-1].isdigit():
            return pyin
        else:
            return pyin[0] + ' ' + pyin[1:]
    

    def tone_to_digit(self, pyin):
        for i in range(len(pyin)):
            if pyin[i] in config.toneMap:
                pyin = pyin[:i] + config.toneMap[pyin[i]][0] + pyin[i+1:] + config.toneMap[pyin[i]][1]
                break 
        # pyin = self.split_pyin(pyin)

        return pyin


    def get_pyin(self, text, tone=config.tone):
        text = self.preprocess(text, tone)
        print(text)
        res = []
        i = 0
        while i < len(text):
            if text[i] == 'p' and text[i : i+3] == 'pi1':
                res.append(text[i : i+3]) 
                i += 3
                continue 
            if text[i] == 'b' and text[i : i+3] == 'bi1':
                res.append(text[i : i+3]) 
                i += 3
                continue

            if text[i] == '#':
                i += 1
                if i < len(text) and text[i] in ['1', '2', '3', '4']:
                    res.append('#' + text[i])
                    i += 1

                continue 

            if 'a' <= text[i] <= 'z': 
                j = i 
                while i < len(text) and 'a' <= text[i] <= 'z':
                    i += 1
            
                if i < len(text) and text[i] in ['1', '2', '3', '4']:
                    i += 1

                res.append(text[j:i])
                if text[i] == ' ':
                    i += 1
                continue
            
            tmp = '' 
            while i < len(text) and text[i].isdigit():
                tmp = tmp + text[i]
                i += 1
            if len(tmp) > 0:
                words= int_to_words(tmp)
                pyin1, words = get_pyin(words)
                res.extend(pyin1.split(' '))
                continue 
        
            t = text[i]
            if t in self.phrase:
                flag = 0 
                for item in self.phrase[t]:
                    pz, py = item
                    if text[i:i+len(pz)] == pz:
                        for j in range(len(pz)):
                            res.append(self.tone_to_digit(py[j]))
                        i += len(pz)
                        flag = 1
                        break 
                if flag == 1:
                    continue

            if t in self.hz:
                res.append(self.tone_to_digit(self.hz[t][0]))
            else:
               res.append(t)
        
            i += 1

        return ' '.join(res), text
