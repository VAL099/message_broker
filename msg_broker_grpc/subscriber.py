import os; os.system('cls')
import time
import grpc
import logging
import broker_pb2_grpc as pb2_grpc
import broker_pb2 as pb2

def run():
    print('Running...')
    prev = ''
    t = input('What topic do you wanna listen? -> ')
    hc = input('Do you want to read history?(Y/n) -> ')
    if hc == 'Y':
        try:
            with grpc.insecure_channel( 'localhost:4587' ) as channel:
                stub = pb2_grpc.handle_messagesStub(channel)
                response = stub.HistoryHandler(pb2.RequestHistory(topic = t))
                for fb in response:
                    print(f'[history] >> {fb.content}')
        except: pass
    while True:
        try:
            with grpc.insecure_channel( 'localhost:4587' ) as channel:
                stub = pb2_grpc.handle_messagesStub(channel)
                response = stub.BroadcastPublication(pb2.RequestUpdate(topic = t))
                msg = response.content
                if msg != prev:
                    print(f'>> {msg}')
                else: time.sleep(3)
                prev = response.content
                time.sleep(2)
        except: time.sleep(2)

if __name__ == '__main__':
    logging.basicConfig()
    run()