import socket
import sys
import select
import random
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from datetime import datetime

# Create a UDP socket
serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 10000)

# Calculate the clients Secret
sharedPrime = 12973
sharedBase = 14479
clientSecret = str(sharedBase ** random.randint(1000,1100) % sharedPrime)
serverSock.sendto(clientSecret.encode('utf-8'), server_address)

# Receive the servers secret
serverSecret = serverSock.recv(2048).decode('utf-8')

# Calculate the common secret key
commonSecret = int(serverSecret) ** int(clientSecret) % sharedPrime
print("The shared key is ", commonSecret)

while True:
    # Create an advanced encrypted standard object using our shared key, to encrypt message
    iv = Random.new().read(AES.block_size)
    encodeSecret = str(commonSecret)
    bitKey = encodeSecret.encode('utf-8')
    key = encodeSecret.ljust(16)
    obj = AES.new(key, AES.MODE_CBC, iv)

    # Maintains a list of possible input streams
    sockets_list = [sys.stdin, serverSock]
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
    for socks in read_sockets:
        if socks == serverSock:
            message = socks.recv(2048)

            # Create an advanced encrypted standard object using our shared key, to decrypt message
            obj2 = AES.new(key, AES.MODE_CBC, ivTemp)
            decrypt = str(obj2.decrypt(message))
            startIndex = decrypt.find('2')
            print("\nDecrypted message received: ", decrypt[2:startIndex-2])
            recvTime = decrypt[startIndex:startIndex+19]

            # Compare timestamps
            if recvTime == sendTime:
                print("\nReceived timestamp matches sent timestamp. Replay protection confirmed!")
        else:
            print("\nWrite a message: ")
            sendTime = str(datetime.now())[0:19]
            timeMessage = sys.stdin.readline() + sendTime

            # Encrypt the combined message and time
            encryptMessage = obj.encrypt(timeMessage.ljust(64))
            print("\nEncrypted message to send: ", encryptMessage)

            # Hash the encrypted message with the shared key and SHA256
            sign = HMAC.new(bitKey, encryptMessage, digestmod=SHA256).digest()
            print("\nHash to send: ", sign)

            # Send message and hash to server
            serverSock.sendto(sign, server_address)
            serverSock.sendto(encryptMessage, server_address)
            ivTemp = iv

serverSock.close()
