import socket
import sys
import select
import ssl
import random
from Crypto import Random
from Crypto.Cipher import AES
import hmac
import hashlib
import base64
from Crypto.Hash import HMAC

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)

sharedPrime = 12973
sharedBase = 14479
clientSec = random.randint(1000,1100)
print("client sec", clientSec)
clientSecret = str(sharedBase ** clientSec % sharedPrime)
print("C", clientSecret)
sock.sendto(clientSecret.encode('utf-8'), server_address)
serverSecret = sock.recv(2048)
serverSecret.decode('utf-8')
if serverSecret:
    print("S", serverSecret)
    commonSecret = int(serverSecret) ** int(clientSecret) % sharedPrime
    print("Common", commonSecret)

#iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])


while True:
    iv = Random.new().read(AES.block_size)
    encodeSecret = str(commonSecret)
    bitKey = encodeSecret.encode('utf-8')
    key = encodeSecret.ljust(16)
    obj = AES.new(key, AES.MODE_CBC, iv)
    # maintains a list of possible input streams
    sockets_list = [sys.stdin, sock]
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

    for socks in read_sockets:
        if socks == sock:
            message = socks.recv(2048)
            print("rec",message)
            #decryptMessage = str(message)
            obj2 = AES.new(key, AES.MODE_CBC, ivTemp)
            print("Riktigt mes", obj2.decrypt(message))
        else:
            message = sys.stdin.readline()
            encryptMessage = obj.encrypt(message.ljust(16))
            #sign = base64.b64encode(hmac.new(bitKey, encryptMessage, digestmod=hashlib.sha256).digest())
            #print("Sign",sign)
            sign = HMAC.new(encryptMessage).digest()
            print("Sign", sign)
        #    print("digest", sign.hexdigest())
            sock.sendto(sign, server_address)
            ivTemp = iv
            #sys.stdout.write(message)
            #sys.stdout.flush()
sock.close()
