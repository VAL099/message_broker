
import os; os.system('cls')
import handlers
import constant

import grpc
import broker_pb2_grpc as pb2_grpc
import broker_pb2 as pb2
from concurrent import futures

t1 = handlers.topicData()
t2 = handlers.topicData()
t3 = handlers.topicData()

local_storage = {
    'topic1': { 'messages':t1.q }, 
    'topic2': { 'messages':t2.q }, 
    'topic3': { 'messages':t3.q } }

class Broker():
    
    def GetPublication(self, request, context):
        local_storage[request.topic]['messages'].append( request.content )
        print(f'\n{local_storage}')
        # handlers.backUp_messages(local_storage)
        return pb2.Reply1(message = constant.REPLY_TO_PUBLISHER)

    def BroadcastPublication(self, request, context):
        if len(local_storage[request.topic]['messages']) > 0:
            msg = local_storage[request.topic]['messages'][-1]
            # handlers.backUp_messages(local_storage)
            return pb2.Publication(content = msg)

    def HistoryHandler(self, request, context):
        print(f'[history] {request}')
        for message in local_storage[request.topic]['messages']:
            yield pb2.History(content = message) # pb2.History(content = message)
        
def run_broker():
    port = '4587'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    pb2_grpc.add_handle_messagesServicer_to_server(Broker(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print(f'Server started, working on {port} ...')
    server.wait_for_termination()


# python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. ./broker.proto

if __name__ == '__main__':

    run_broker()