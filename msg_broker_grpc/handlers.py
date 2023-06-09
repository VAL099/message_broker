import json

class topicData:

    def __init__(self):
        self.q = [] # message queue
        self.h = [] # history


def restore_messages(storage): # now is a parser

    prim = ['topic1', 'topic2', 'topic3']
    sec = ['queue', 'history']
    
    with open('storage.json', 'r') as f:
        data = json.load(f)
        for pkey in prim:
            for skey in sec:
                storage[pkey][skey] = data[pkey][skey]
            break

def backUp_messages(storage):

    data = {   
        'topic1': { 'queue':storage['topic1']['queue'], 'history':storage['topic1']['history'] }, 
        'topic2': { 'queue':storage['topic2']['queue'], 'history':storage['topic2']['history'] }, 
        'topic3': { 'queue':storage['topic3']['queue'], 'history':storage['topic3']['history'] } }

    payload = json.dumps(data, indent = 4)
    file = open('storage.json', 'w')
    file.write(payload)
    file.close()
