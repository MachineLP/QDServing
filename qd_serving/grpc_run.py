# -*- coding:utf-8 -*-
'''
-------------------------------------------------
   Description :  grpc server 
   Author :       liupeng
   Date :         2020-09-01
-------------------------------------------------

'''

import sys
import time
import grpc
import json
import multiprocessing
from concurrent import futures
from app.core.models import TTSModel
from app.utils.logging import logging
from app.grpc import call_ant_pb2_grpc, call_ant_pb2


_ONE_DAY_IN_SECONDS = 60 * 60 * 24
tts_model = TTSModel()


def inference(text):
    mels, alignment_history, audios = tts_model.do_synthesis(text)
    return 200, audios.tolist() 
    # return 200, text

class Greeter(call_ant_pb2_grpc.GreeterServicer):

    def SendData(self, request, context):
        logging.info("start_get_img_feature, url: %s", request.name)
        start = time.time()
        code, audios_data = inference(request.name)
        end = time.time()

        if code == 0:
            logging.info("success_get_img_feature, time: %fs, data_size: %d, url: %s", (end - start), len(audios_data), request.name)
        else:
            logging.error("fail_get_img_feature, time: %fs, data_size: %d, url: %s", (end - start), len(audios_data), request.name)

        return call_ant_pb2.AntReply(code=code, data=audios_data)

def serve(port):
    host = "[::1]:"
    host += str(port)
    logging.info(host)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    call_ant_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port(host)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


HTTP_PORT = 47260
if len(sys.argv) > 1:
    HTTP_PORT = sys.argv[1]

if __name__ == '__main__':
    logging.info("-------grpc service start--------")
    serve(HTTP_PORT)