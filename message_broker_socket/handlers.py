
class topicData:

    def __init__(self):
        self.s = [] # subscriber
        self.q = [] # message queue
        self.h = [] # history
        

def start_thread(th):
    if th.is_alive() == False:
        th.start()