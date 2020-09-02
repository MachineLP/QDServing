# -*- coding:utf-8 -*-
'''
-------------------------------------------------
   Description :  models
   Author :       machinelp
   Date :         2020-08-27
-------------------------------------------------

'''

import os
import sys
import time
import json
import librosa
import numpy as np
import IPython.display as ipd
from app.core.models import TTSModel


if __name__ == '__main__':

    tts_model = TTSModel()
    text = "我们本次谈话内容录音备案记录，如果您可以在规定时间内下载来分期 艾普 处理逾期账单，我会帮您申请恢复额度，额度恢复以后如果您还有资金需求可以在来分期 艾普 上申请下单，系统审核通过以后，可以再把额度周转出来使用，但若与您协商却无法按时处理，造成的负面影响需自行承担，请提前告知他们有关去电事宜，再见"
    print ("text>>>>", text)
    for i in range(10):
        start_time = time.time()
        mels, alignment_history, audios = tts_model.do_synthesis(text)
        print ("time>>>>>>>", time.time() - start_time)
    # print( "audios>>>>", audios  )
    ipd.Audio(audios, rate=24000)
    librosa.output.write_wav("output_seq.wav", audios, 24000)

'''
time>>>>>>> 23.533220767974854 
'''

