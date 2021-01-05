
import grpc
from app.grpc import call_ant_pb2_grpc, call_ant_pb2


def run():
    channel = grpc.insecure_channel('localhost:9959')
    stub = call_ant_pb2_grpc.GreeterStub(channel)
    text = "你好啊"
    response = stub.SendData(call_ant_pb2.AntRequest(name=text))
    print(response.data)
    print(len(response.data))
    print(response.code)
    


if __name__ == '__main__':
    run()
