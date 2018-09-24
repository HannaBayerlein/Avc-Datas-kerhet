import socket
import sys
import random
from Crypto.Cipher import AES

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
sock.bind(server_address)

sharedPrime = 12973
sharedBase = 14479
serverSec = random.randint(1000,1100)
print("server", serverSec)
serverSecret = str((sharedBase ** serverSec) % sharedPrime)
print("S", serverSecret)
clientSecret, address = sock.recvfrom(4096)
clientSecret.decode('utf-8')
int(clientSecret)
print("secC", clientSecret)
if clientSecret:
    sent = sock.sendto(serverSecret.encode('utf-8'), address)

commonSecret = int(serverSecret) ** int(clientSecret) % sharedPrime
print("Common", commonSecret)


while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(4096)

    print('received %s bytes from %s' % (len(data), address))
    #sent = sock.sendto(data, address)
    #print(data)

    if data:
        sent = sock.sendto(data, address)
        print(data)
        #print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)
