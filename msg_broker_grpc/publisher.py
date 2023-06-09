import os; os.system('cls')
import grpc
import logging
import broker_pb2_grpc as pb2_grpc
import broker_pb2 as pb2

def run():
    print('Running...')
    while True:
        t = input('Enter the topic: ')
        msg = input('Enter the message: ')
        with grpc.insecure_channel('localhost:4587') as channel:
            stub = pb2_grpc.handle_messagesStub(channel)
            response = stub.GetPublication(pb2.MessageWithContent( topic = t, content = msg ))
            print(f'Sent! {response}')


if __name__ == '__main__':
    logging.basicConfig()
    run()