# -*- coding:utf-8 -*-
'''
-------------------------------------------------
   Description :  models
   Author :       machinelp
   Date :         2020-08-27
-------------------------------------------------

'''

import yaml
import numpy as np
import tensorflow as tf
from conf.config import config
# import IPython.display as ipd
from app.utils.logging import logging
from tensorflow_tts.inference import AutoConfig
from tensorflow_tts.inference import TFAutoModel
from tensorflow_tts.inference import AutoProcessor
from app.core.parse_text_add_pause import TTSSegPause
from app.core.parse_text_to_pyin import TTSPinYin

class TTSModel():

    def __init__(self):
        gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
        tf.config.experimental.set_visible_devices(devices=gpus[0:2], device_type='GPU')
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        self.__init_model()
        self.tts_pause = TTSSegPause()
        self.tts_py = TTSPinYin()

    def __init_model(self):
        tacotron2_config = AutoConfig.from_pretrained( config.tacotron2_baker )
        self.tacotron2 = TFAutoModel.from_pretrained( config=tacotron2_config, pretrained_path=config.tacotron2_pretrained_path, training=False,  name="tacotron2" )
        self.tacotron2.setup_window(win_front=5, win_back=5)


        mb_melgan_config = AutoConfig.from_pretrained( config.multiband_melgan_baker )
        self.mb_melgan = TFAutoModel.from_pretrained( config=mb_melgan_config, pretrained_path=config.multiband_melgan_pretrained_path, name="mb_melgan" )

        self.processor = AutoProcessor.from_pretrained(pretrained_path=config.baker_mapper_pretrained_path)


    def text_to_pinyin_sequence(self, text):
        # pinyin = self.processor.pinyin_parser(text, style=Style.TONE3, errors="ignore")
        pinyin, text = self.tts_py.get_pyin(text)
        new_pinyin = []
        for x in str(pinyin).split(" "):
            if "#" not in x:
                new_pinyin.append(x)
        phonemes = self.processor.get_phoneme_from_char_and_pinyin(text, new_pinyin)
        text = " ".join(phonemes)
        print("phoneme seq: {}".format( text ))
        logging.info( "[TTSModel] [text_to_pinyin_sequence] phoneme seq:{}".format( text ) )
        input_ids = self.processor.text_to_sequence(text, inference=False) 
        return input_ids


    def predict(self, input_text):
        input_text = self.tts_pause.add_pause(input_text)
        print ("input_text>>>>", input_text)
        logging.info( "[TTSModel] [do_synthesis] input_text:{}".format( input_text ) )
        input_ids = self.processor.text_to_sequence(input_text, inference=True) 
        
        _, mel_outputs, stop_token_prediction, alignment_history = self.tacotron2.inference(
            tf.expand_dims(tf.convert_to_tensor(input_ids, dtype=tf.int32), 0),
            tf.convert_to_tensor([len(input_ids)], tf.int32),
            tf.convert_to_tensor([0], dtype=tf.int32) )
        
        remove_end = 1024
        audio = self.mb_melgan.inference(mel_outputs)[0, :-remove_end, 0]
    
        return mel_outputs.numpy(), alignment_history.numpy(), audio.numpy() 



    '''
    input_text = "如果现在还不了，您可以想办法处理啊，您家人知道您的逾期情况吗？他们能不能帮您周转处理逾期账单？"
    mels, alignment_history, audios = do_synthesis(input_text)
    ipd.Audio(audios, rate=24000)
    '''

