from __future__ import print_function

import grpc

# from app.services.grpc import callocr_pb2_grpc, callocr_pb2
from app.grpc import call_ant_pb2_grpc, call_ant_pb2


def run():
    channel = grpc.insecure_channel('localhost:47260')
    stub = call_ant_pb2_grpc.GreeterStub(channel)
    text = "你好啊"
    print("3333333333333")
    response = stub.SendData(call_ant_pb2.AntRequest(name=text))
    print("4444444444444")
    print(response.data)
    print(len(response.data))
    print(response.code)
    


if __name__ == '__main__':
    run()
