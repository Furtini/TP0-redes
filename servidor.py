import sys
import socket
import struct
import threading

class ServidorThread(object):
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.tcp.bind((self.host, self.port))

    def listen(self):
        
        self.tcp.listen(1)        
        con, cliente = self.tcp.accept()
        # Timeout
        timeval = struct.pack('ll', 15, 0)
        self.tcp.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeval)
        
        threading.Thread(target=self.listen_client, args = (con,cliente)).start()
       
    def listen_client(self, con, cliente):
        
         #Funcao para decifrar
        def ceaser_desipher(msg, cipher):

            decifrada = ''
            for ch in msg:
                new_ch = (ord(ch) - cipher) % 123
                decifrada += chr(new_ch)

            return decifrada

        while True:

            size = con.recv(32)
            if not size:
                break
            con.send('>' + size + '<')

            # Tamanho da mensagem em bits
            size = int(size) * 8
            msg = con.recv(size)
            if not msg:
                break
            con.send('>' + msg + '<')

            cipher = con.recv(32)
            if not cipher:
                break
            con.send(cipher)

            decifrada = ceaser_desipher(msg, int(cipher))
            print decifrada
            con.send(decifrada)

        con.close()

if __name__ == '__main__':
    
    while True:
        try:
            porta = int(sys.argv[1])
            break
        except ValueError:
            pass

    ServidorThread('', porta).listen()