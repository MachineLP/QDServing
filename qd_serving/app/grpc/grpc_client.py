
import time
import grpc
from app.config.config import *
from app.exts.common import *
from app.utils.logging import logging
from app.grpc import call_ant_pb2_grpc, call_ant_pb2



# 获取图片特征值，通过grpc远程调用
def get_res_by_grpc(grpc_host, text):

    logger.info("start_call_grpc, grpc_host: {}, url: {}".format( grpc_host, url ) )

    start = time.time()
    channel = grpc.insecure_channel(grpc_host)
    stub = call_ant_pb2_grpc.GreeterStub(channel)
    response = stub.SendData(call_ant_pb2.AntRequest(name=text))
    end = time.time()

    if response.code == 200:
        logging.info("success_data_by_grpc, time: {}s, size: {}, url: {}".format( (end-start), len(response.data), url) )
    else:
        logging.error("fail_call_grpc, time: {}s, data_size: {}, url: {}".format( (end-start), len(response.data), url) )

    return response.data



# 获取排序top n，通过grpc远程调用
def get_sort_by_grpc(grpc_host, resp_data, list_url):

    logger.info("start_call_grpc, grpc_host: {}, url: {}".format( grpc_host, url ) )
    start = time.time()
    channel = grpc.insecure_channel(grpc_host)
    stub = call_ant_pb2_grpc.GreeterStub(channel)
    response = stub.SendData(call_ant_pb2.AntRequest(name=resp_data))
    end = time.time()
    list_result = str_2_list_by_json(response.data)

    if response.code == 200:
        logging.info("success_call_grpc, time: {}s, data_size: {}, url: {}".format( (end-start), len(response.data), list_url) )
    else:
        logging.error("fail_call_grpc, time: {}s, data_size: {}, url: {}".format( (end-start), len(response.data), list_url) )

    return list_result


    # 异步获取排序top n，通过grpc远程调用
def get_sort_by_grpc_async(grpc_host, resp_data, list_url, results = [], tags=[]):

    def process_response(call_future):
        try:
            list_result = str_2_list_by_json(call_future.result().data)
            results.extend(list_result)
            tags.append(1)
            logging.info("--------------end_call_grpc-------------")
        except:
            logging.error("--------------fail_call_grpc-------------")

    ret = True
    try:
        logging.info("start_call_grpc, grpc_host: {}s, url: {}".format( grpc_host, list_url) )
        channel = grpc.insecure_channel(grpc_host)
        stub = call_ant_pb2_grpc.GreeterStub(channel)
        call_future = stub.SendData.future(call_ant_pb2.AntRequest(name=resp_data))
        call_future.add_done_callback(process_response)
    except:
        tags.append(1)
        logging.error("-----fail_get_sort_by_grpc, host: {}".format( grpc_host ) )
        ret = False

    return ret


