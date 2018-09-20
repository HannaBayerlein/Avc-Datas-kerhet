import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

while True:
    print >>sys.stderr, '\nwaiting to receive message'
    data, address = sock.recvfrom(4096)

    print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
    print >>sys.stderr, data

    if data:
        sent = sock.sendto(data, address)
        print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)



# use Python 3 print function
# this allows this code to run on python 2.x and 3.x
#from __future__ import print_function

# Variables Used
#sharedPrime = 23    # p
#sharedBase = 5      # g

#aliceSecret = 6     # a
#bobSecret = 15      # b

# Begin
#print( "    Publicly Shared Prime: " , sharedPrime )
#print( "    Publicly Shared Base:  " , sharedBase )

# Alice Sends Bob A = g^a mod p
#A = (sharedBase**aliceSecret) % sharedPrime
#print( "\n  Alice Sends Over Public Chanel: " , A )

# Bob Sends Alice B = g^b mod p
#B = (sharedBase ** bobSecret) % sharedPrime
#print( &amp;amp;amp;amp;amp;amp;quot;   Bob Sends Over Public Chanel: ", B )

#print( "\n------------\n" )
#print( "Privately Calculated Shared Secret:" )
# Alice Computes Shared Secret: s = B^a mod p
#aliceSharedSecret = (B ** aliceSecret) % sharedPrime
#print( "    Alice Shared Secret: ", aliceSharedSecret )

# Bob Computes Shared Secret: s = A^b mod p
#bobSharedSecret = (A**bobSecret) % sharedPrime
#print( "    Bob Shared Secret: ", bobSharedSecret )
