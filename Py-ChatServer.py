import socket
import threading

SIZE = 4
print 'Welcome to Py-Chat'
print 'This is Py-Chat server'
print 'Designed by : Ankush Bhatia\n My ID is asshatter'
port = 5432 # You can use any number greater than 1024

soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
soc.bind((socket.gethostname(),port)) # You can use '127.0.0.1' in first arguement for a local host
print 'My Chat server started on ' + socket.gethostname() +'\nport ' + str(port)
print 'Listening for new connections. . . .'
soc.listen(5)

class CThread(threading.Thread):
    def __init__(self,c):
        threading.Thread.__init__(self)
        self.conn = c
        self.stopIt=False

    def mrecv(self):
        data = self.conn.recv(SIZE)
        self.conn.send('OK')
        msg = self.conn.recv(int(data))
        return msg

    def run(self):
        while not self.stopIt:
            msg = self.mrecv()
            print 'Client :  ',msg

def setConn(con1,con2):
    dict={}
    state = con1.recv(9)
    con2.recv(9)
    if state =='WILL RECV':
        dict['send'] = con1 # server will send data to reciever
        dict['recv'] = con2
    else:
        dict['recv'] = con1 # server will recieve data from sender
        dict['send'] = con2
    return dict

def msend(conn,msg):
    if len(msg)<=999 and len(msg)>0:
        conn.send(str(len(msg)))
        if conn.recv(2) == 'OK':
            conn.send(msg)

(c1,a1) = soc.accept()
(c2,a2) = soc.accept()
print 'Got connectiion from address: ' + str(a1[0])
dict = setConn(c1,c2)
thr = CThread(dict['recv'])
thr.start()
try:
    while 1:
        msend(dict['send'],raw_input())
except:
    print 'closing'
thr.stopIt=True
msend(dict['send'],'Bye')# for stoping the thread
thr.conn.close()
soc.close()
