import os; os.system('cls')
import socket
import constant
import tkinter as tk

who = 'publisher'

_host = constant.broker_host
_port = constant.broker_port

_broker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_broker.connect((_host, _port))

def SignIn():

    _broker.send('{}|'.format(who).encode())
    resp = _broker.recv(2048).decode()
    if resp == 'ACCEPTED!':
        print('Linked with {}'.format(constant.host_name))

def send(t, c):

    topic = t
    content = c
    _broker.send('{}||{}'.format(topic, content).encode())
    print('SENT!')

def main():
    
    mainWin = tk.Tk()
    w = 500; h = 600;
    sw = mainWin.winfo_screenwidth(); sh = mainWin.winfo_screenheight()
    xw = (sw//2) - (w//2); xh = (sh//2) - (h//2)
    mainWin.configure(background = 'lightgray')
    mainWin.geometry('{}x{}+{}+{}'.format(w, h, xw, xh)) #centring
    mainWin.resizable(False, False)
    mainWin.title('Publisher')

    uiTopic = tk.StringVar()
    uiContent = tk.StringVar()

    lb1 = tk.Label(mainWin, text = 'Topic:',  font = ('Cambria', 14), background = 'lightgray', foreground = 'black')
    lb1.place(relx = 0.05, rely = 0.1, anchor = 'w')
    entry1 = tk.Entry(mainWin, textvariable = uiTopic, font = ('Cambria', 14), width = 30)
    entry1.place(relx = 0.22, rely = 0.1, anchor = 'w')

    lb2 = tk.Label(mainWin, text = 'Content:',  font = ('Cambria', 14), background = 'lightgray', foreground = 'black')
    lb2.place(relx = 0.05, rely = 0.20, anchor = 'w')
    entry2 = tk.Text(mainWin, font = ('Cambria', 14), width = 30, height = 15)
    entry2.place(x = 110, y = 110)

    btn = tk.Button(mainWin, text = 'SEND!', command = lambda:[send(uiTopic.get(), entry2.get(1.0, 'end')), entry1.delete(0, tk.END), entry2.delete('1.0', tk.END)], font = ('Cambria', 13), width = 10)
    btn.place(relx = 0.5, rely = 0.9, anchor = 'center')

    mainWin.mainloop()

    """
    # testing
    for i in range(30):
        send('topic1', 'some text here!!!!!!')
        time.sleep(1)
        send('topic2', 'some text here!!!!!!')
        time.sleep(1)
        send('topic3', 'some text here!!!!!!')
        time.sleep(1)
    """

if __name__ == '__main__':
    SignIn()
    main()

    
