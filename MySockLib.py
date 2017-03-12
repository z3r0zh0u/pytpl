"""
My Socket Library
"""

import time
import socket
import threading


def show_output(sock, lock):
    """Show output from a socket"""

    while True:
        lock.acquire()
        sock.setblocking(0)
        try:
            data = sock.recv(1024)
            if len(data) == 0:
                sock.setblocking(1)
                lock.release()
                break
            print data.strip()
        except Exception as e:
            pass
        sock.setblocking(1)
        lock.release()
        time.sleep(0.1)


class MySock:

    def __init__(self, host, port, debug = False):

        self.debug = debug
        self.host = host
        self.port = port

        self.__debug_print('[*] Host: ' + self.host)
        self.__debug_print('[*] Port: ' + str(self.port))

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))


    def send(self, data):
        """Send data"""

        self.__debug_print('[*] Send: ' + data)
        self.sock.send(data)
    

    def recv_until(self, stopper):
        """Receive data untill found the stopper"""

        data = ''
        while True:
            data += self.sock.recv(1)
            if data.find(stopper) != -1:
                break

        self.__debug_print('[*] Recv: ' + data)
        return data
    

    def recvn(self, size):
        """Receive data in specified size"""

        data = ''
        for i in range(0, size):
            data += self.sock.recv(1)
        
        self.__debug_print('[*] Recv: ' + data)
        return data


    def recv(self, size):
        """Recv data"""

        data = self.sock.recv(size)
        self.__debug_print('[*] Recv: ' + data)
        return data
    

    def interactive(self):
        """Interactive with the socket"""

        self.__debug_print('[*] Interactive Begin')

        self.lock = threading.Lock()
        output_thread = threading.Thread(target=show_output, args=(self.sock, self.lock))
        output_thread.daemon = True
        output_thread.start()
        
        while True:
            try:
                input = raw_input()
                self.lock.acquire()
                self.sock.send(input + '\n')
                self.lock.release()
                time.sleep(0.1)
            except Exception as e:
                print '[*] Error: ' + str(e)
                break
    

    def __debug_print(self, message):
        """Print debug info"""

        if self.debug:
            print message
    

def socket_conn():
    """Scoket Connection"""
    
    ip = '192.168.157.129'
    port = 1337

    sock = MySock(ip, port, debug = True)
    sock.send('Hello World!')
    sock.recvn(10)
    sock.recv_until('exit\n')
    

if __name__ == '__main__':

    socket_conn()
    