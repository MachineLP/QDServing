
import grpc
from app.grpc import call_ant_pb2_grpc, call_ant_pb2
from app.config.config import *
from app.exts.common import *
import time



# 获取图片特征值，通过grpc远程调用
def get_feat_by_grpc(grpc_host, url):

    logger.info("start_call_grpc, grpc_host: %s, url: %s", grpc_host, url)

    start = time.time()
    channel = grpc.insecure_channel(grpc_host)
    stub = call_ant_pb2_grpc.GreeterStub(channel)
    response = stub.SendData(call_ant_pb2.AntRequest(name=url))
    end = time.time()

    if response.code == 0:
        logger.info("success_get_feat_by_grpc, time: %fs, size: %d, url: %s", (end-start), len(response.data), url)
    else:
        logger.error("fail_call_grpc, time: %fs, data_size: %d, url: %s", (end-start), len(response.data), url)

    return response.data


# 获取排序top n，通过grpc远程调用
def get_sort_by_grpc(grpc_host, resp_data, list_url):

    logger.info("start_call_grpc, grpc_host: %s, url: %s", grpc_host, list_url)
    start = time.time()
    channel = grpc.insecure_channel(grpc_host)
    stub = call_ant_pb2_grpc.GreeterStub(channel)
    response = stub.SendData(call_ant_pb2.AntRequest(name=resp_data))
    end = time.time()
    list_result = str_2_list_by_json(response.data)

    if response.code == 0:
        logger.info("success_call_grpc, time: %fs, data_size: %d, url: %s", (end-start), len(response.data), list_url)
    else:
        logger.error("fail_call_grpc, time: %fs, data_size: %d, url: %s", (end-start), len(response.data), list_url)

    return list_result


    # 异步获取排序top n，通过grpc远程调用
def get_sort_by_grpc_async(grpc_host, resp_data, list_url, results = [], tags=[]):

    def process_response(call_future):
        try:
            list_result = str_2_list_by_json(call_future.result().data)
            results.extend(list_result)
            tags.append(1)
            logger.info("--------------end_call_grpc-------------")
        except:
            logger.error("--------------fail_call_grpc-------------")

    ret = True
    try:
        logger.info("start_call_grpc, grpc_host: %s, url: %s", grpc_host, list_url)
        channel = grpc.insecure_channel(grpc_host)
        stub = call_ant_pb2_grpc.GreeterStub(channel)
        call_future = stub.SendData.future(call_ant_pb2.AntRequest(name=resp_data))
        call_future.add_done_callback(process_response)
    except:
        tags.append(1)
        logger.error("-----fail_get_sort_by_grpc, host: %s", grpc_host)
        ret = False

    return ret


