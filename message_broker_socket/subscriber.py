import os
import time; os.system('cls')
import socket
import constant
import tkinter as tk

who = 'listener'

_host = constant.broker_host
_port = constant.broker_port
_broker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

topic = {'value' : ''}

def atr_val(var):
    topic['value'] = var

def initialize():
    welcomeWin = tk.Tk()
    w = 350; h = 150;
    sw = welcomeWin.winfo_screenwidth(); sh = welcomeWin.winfo_screenheight()
    xw = (sw//2) - (w//2); xh = (sh//2) - (h//2)
    welcomeWin.configure(background = 'lightgray')
    welcomeWin.geometry('{}x{}+{}+{}'.format(w, h, xw, xh)) #centring
    welcomeWin.resizable(False, False)
    welcomeWin.title('Subscriber')

    uiTopic = tk.StringVar()
    
    lb1 = tk.Label(welcomeWin, text = 'Topic:',  font = ('Cambria', 14), background = 'lightgray', foreground = 'black')
    lb1.place(relx = 0.07, rely = 0.2, anchor = 'w')
    entry1 = tk.Entry(welcomeWin, textvariable = uiTopic, font = ('Cambria', 14), width = 20)
    entry1.place(relx = 0.25, rely = 0.2, anchor = 'w')
    btn = tk.Button(welcomeWin, text = 'CONNECT!', command = lambda:[atr_val(uiTopic.get()), helpWin(welcomeWin)], font = ('Cambria', 13), width = 10)
    btn.place(relx = 0.5, rely = 0.7, anchor = 'center')

    welcomeWin.mainloop()

def helpWin(root):
    win1 = tk.Toplevel(root)
    w = 400; h = 150;
    sw = win1.winfo_screenwidth(); sh = win1.winfo_screenheight()
    xw = (sw//2) - (w//2); xh = (sh//2) - (h//2)
    win1.configure(background = 'lightgray')
    win1.geometry('{}x{}+{}+{}'.format(w, h, xw, xh))
    win1.resizable(False, False)
    win1.title('History')

    lb1 = tk.Label(win1, text = 'Would you like to see the history of post?',  font = ('Cambria', 14, 'bold'), background = 'lightgray', foreground = 'black')
    lb1.place(relx = 0.5, rely = 0.2, anchor = 'center')
    btn1 = tk.Button(win1, text = 'NO!', command = lambda:[SignIn(topic['value'], 'n'), win1.destroy(), root.destroy(), receive()], font = ('Cambria', 13), width = 10)
    btn1.place(relx = 0.7, rely = 0.7, anchor = 'center')
    btn2 = tk.Button(win1, text = 'YES!', command = lambda:[SignIn(topic['value'], 'Y'), win1.destroy(), root.destroy(), receive()], font = ('Cambria', 13), width = 10)
    btn2.place(relx = 0.3, rely = 0.7, anchor = 'center')

    win1.mainloop()

def SignIn(topic, decision):

    _broker.connect((_host, _port))
    _broker.send('{}|{}'.format(who, topic).encode())
    resp = _broker.recv(2048).decode()
    if resp == 'WELCOMEN!':
        print('Connected and ready!')
    if decision == 'Y':
        _broker.send('GET:{}'.format(topic).encode())


def receive():
    
    while True:
        print('-...-')
        msg = _broker.recv(1024).decode()
        if msg.startswith('|'):
            payload = msg.split('|')
            for m in payload:
                print('[History] >> {}'.format(m.rstrip()))
                time.sleep(0.2)
        else: 
            print('>> {}'.format(msg.rstrip()))
            

if __name__ == '__main__':
    print('CLIENT LAUNCHED!')

    initialize()
    receive()

