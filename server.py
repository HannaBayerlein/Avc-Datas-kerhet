import socket
import sys
import random
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from datetime import datetime

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the address
server_address = ('localhost', 10000)
sock.bind(server_address)

# Calculate the servers secret
sharedPrime = 12973
sharedBase = 14479
serverSecret = str((sharedBase ** random.randint(1000,1100)) % sharedPrime)

# Receive the clients secret
clientSecret, address = sock.recvfrom(4096)

sock.sendto(serverSecret.encode('utf-8'), address)

# Calculate the common secret key
commonSecret = int(serverSecret) ** int(clientSecret) % sharedPrime
print("The shared key is ", commonSecret)
bitKey = str(commonSecret).encode('utf-8')


while True:
    # Receive the hash from the client
    print('\nWaiting to receive message')
    hash, address = sock.recvfrom(4096)
    print("\nReceived hash from client: ",hash)

    # Receive the encrypted message from the client
    encrypt, address = sock.recvfrom(4096)
    print("\nReceived encrypted message from client: ",encrypt)

    # Calculate the hash with the common secret key, encrypted message and SHA256
    sign = HMAC.new(bitKey ,encrypt, digestmod=SHA256).digest()

    # Compare the calculated hash with the received hash
    if hash == sign:
        print("\nCalculated hash matches received hash. Message not tampered with.")

    if encrypt:
        # Echo the received encrypted message
        sock.sendto(encrypt, address)
