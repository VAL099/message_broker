
import os; os.system('cls')
import json
import time
import socket
import threading
import constant
import schedule
import handlers

_host = constant.broker_host
_port = constant.broker_port
_broker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_broker.bind((_host, _port))
_broker.listen()

t1 = handlers.topicData()
t2 = handlers.topicData()
t3 = handlers.topicData()
publishers = []

local_storage = {
    'topic1': {'subscribers': t1.s, 'queue':t1.q, 'history':t1.h}, 
    'topic2': {'subscribers': t2.s, 'queue':t2.q, 'history':t2.h}, 
    'topic3': {'subscribers': t3.s, 'queue':t3.q, 'history':t3.h} }


def restore_messages(): # now is a parser

    prim = ['topic1', 'topic2', 'topic3']
    sec = ['queue', 'history']
    
    with open('storage.json', 'r') as f:
        data = json.load(f)
        for pkey in prim:
            for skey in sec:
                local_storage[pkey][skey] = data[pkey][skey]
            break

def backUp_messages():

    data = {   
        'topic1': { 'queue':local_storage['topic1']['queue'], 'history':local_storage['topic1']['history'] }, 
        'topic2': { 'queue':local_storage['topic2']['queue'], 'history':local_storage['topic2']['history'] }, 
        'topic3': { 'queue':local_storage['topic3']['queue'], 'history':local_storage['topic3']['history'] } }

    payload = json.dumps(data, indent = 4)
    file = open('storage.json', 'w')
    file.write(payload)
    file.close()

def broadcast(topic):
    print('[{} broadcast module] AWAKE!'.format(topic))
    while True:
        try:
            if len( local_storage[topic]['queue'] ) > 0 and len( local_storage[topic]['subscribers'] ) > 0: # verifing if in queue are messages and if there is a listener on topic
                for subscriber in local_storage[topic]['subscribers']:
                    subscriber.send( local_storage[topic]['queue'][0].encode() ) # send first message from queue
                local_storage[topic]['history'].append( local_storage[topic]['queue'][0] ) # append to history
                local_storage[topic]['queue'].remove( local_storage[topic]['queue'][0] ) # delete from queue 
                backUp_messages() # upload to storage.json
                print('Message on [{}] SENT!'.format(topic))
            else: time.sleep(5) # wait for messages
        except ConnectionResetError: 
            local_storage[topic]['subscribers'].remove(subscriber)
            print('[LOG] CLIENT <{}:{} LEFT!'.format(str(subscriber).split(',')[-2], str(subscriber).split(',')[-1]))

def recv_post(client):
    print('[publications receiver module] AWAKE!')
    if client in publishers:
        while True:
            try:
                msg = client.recv(8000).decode()
                topic, content = msg.split('||')
                if topic in local_storage.keys():
                    local_storage[topic]['queue'].append(content) # append publishers post to queue
                    backUp_messages() # upload to storage.json
                else: print('[publisher] Some error occured!')
            except ConnectionResetError:
                publishers.remove(client)
                print('[LOG] PUBLISHER <{}:{} LEFT!'.format(str(client).split(',')[-2], str(client).split(',')[-1]))
                return

def handle_hystory(client, topic):
    print('[history module] AWAKE!')
    if client not in publishers:
        while True:
            try:
                msg = client.recv(1024).decode()
                print(msg)
                if msg.startswith('GET'):
                    topic = msg.split(':')[1]
                    for i in range(len(local_storage[topic]['history'])):
                        client.send( '|{}'.format(local_storage[topic]['history'][i]).encode() ) # send all messages at once
                else: continue
            except ConnectionResetError: return

def broker():
    
    restore_messages() # load from storage.json

    # th 4 each topic
    th_handle_topic1 = threading.Thread(target = broadcast, args = ('topic1', )) 
    th_handle_topic2 = threading.Thread(target = broadcast, args = ('topic2', ))
    th_handle_topic3 = threading.Thread(target = broadcast, args = ('topic3', ))

    while True:

        client, address = _broker.accept()
        th_handle_publisher = threading.Thread(target = recv_post, args = (client, )) # create th 4 publisher

        resp = client.recv(2048).decode().split('|')
        if resp[0] == 'publisher':
            th_handle_history = threading.Thread(target = handle_hystory, args = ( client, resp[1] )) # create th 4 history
            print('[LOG] PUBLISHER <{}:{} Joined!'.format(str(client).split(',')[-2], str(client).split(',')[-1]))
            publishers.append(client)
            client.send('ACCEPTED!'.encode())
        elif resp[0] == 'listener':
            th_handle_history = threading.Thread(target = handle_hystory, args = ( client, resp[1] )) # create th 4 history
            if resp[1] == 'topic1':
                local_storage['topic1']['subscribers'].append(client) # or local_storage[resp[1]]['subscribers']
                client.send('WELCOMEN!'.encode())
                print('[LOG] CLIENT: <{}:{} JOINED!'.format(str(client).split(',')[-2], str(client).split(',')[-1]))
            elif resp[1]  == 'topic2':
                local_storage['topic2']['subscribers'].append(client)
                client.send('WELCOMEN!'.encode())
                print('[LOG] CLIENT: <{}:{} JOINED!'.format(str(client).split(',')[-2], str(client).split(',')[-1]))
            elif resp[1]  == 'topic3':
                local_storage['topic3']['subscribers'].append(client)
                client.send('WELCOMEN!'.encode())
                print('[LOG] CLIENT: <{}:{} JOINED!'.format(str(client).split(',')[-2], str(client).split(',')[-1]))
        
        handlers.start_thread(th_handle_history)
        handlers.start_thread(th_handle_publisher)
        handlers.start_thread(th_handle_topic1)
        handlers.start_thread(th_handle_topic2)
        handlers.start_thread(th_handle_topic3) # check if we can start them all in the header of main()


if __name__ == '__main__':
    print('BROKER AWAKE!')
    broker()