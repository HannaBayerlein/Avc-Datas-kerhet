import socket
import sys
import select

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)
message = 'This is the message.  It will be repeated.'


while True:

    # maintains a list of possible input streams
    sockets_list = [sys.stdin, sock]

    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

    for socks in read_sockets:
        if socks == sock:
            message = socks.recv(2048)
            print message
        else:
            message = sys.stdin.readline()
            sock.sendto(message, server_address)
            #sys.stdout.write(message)
            sys.stdout.flush()
sock.close()




#try:

    # Send data
#    print >>sys.stderr, 'sending "%s"' % message
#    sent = sock.sendto(message, server_address)

    # Receive response
#    print >>sys.stderr, 'waiting to receive'
#    data, server = sock.recvfrom(4096)
#    print >>sys.stderr, 'received "%s"' % data

#finally:
#    print >>sys.stderr, 'closing socket'
#    sock.close()
