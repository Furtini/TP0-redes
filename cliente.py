import sys
import socket
import struct

# Funcao para Cifrar a mensagem usando Ceaser Cipher
def ceaser_cipher(msg, cipher):
    
    cifrada = ''
    for ch in msg:
        new_ch = (ord(ch) + cipher) % 123
        cifrada += chr(new_ch)

    return cifrada

def main():     
    # Criando socket
    try:
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print 'Falha ao criar socket'
        sys.exit()

    HOST = sys.argv[1]          # Host: primeiro argumento
    PORT = int(sys.argv[2])     # Port: segundo argumento
    dest = (HOST, PORT)

    # Estabelecendo conexao.
    tcp.connect(dest)

    msg = sys.argv[3]           # Mensagem a ser enviada
    cipher = int(sys.argv[4])   # Valor do cipher
    size = len(msg) * 8

    # Convertendo mensagem para ascii
    msg.encode('ascii')

    # Cifrando mensagem
    cifrada = ceaser_cipher(msg, cipher)

    # Enviando tamanho
    p_size = struct.pack('!i', size)
    tcp.send(p_size)
    tcp.recv(32)
    
    # Enviando mensagem cifrada
    tcp.send(cifrada)
    tcp.recv(size)
  
    # Enviando cipher
    p_cipher = struct.pack('!i', cipher)
    tcp.send(p_cipher)
    tcp.recv(32)
  
    decifrada = tcp.recv(size)
    decifrada.decode('ascii', 'strict')
    print decifrada

    tcp.close()

if __name__ == '__main__':
    main()
