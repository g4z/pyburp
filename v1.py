import time
import syslog
from socket import *

payload = b'hello world'

socket_recv = socket(AF_INET, SOCK_DGRAM)
socket_recv.bind(('', 12345))
socket_recv.setblocking(0)

socket_send = socket(AF_INET, SOCK_DGRAM)
socket_send.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)



while True:
    try:
        packet = socket_recv.recvfrom(1024)
        message = packet[0].decode('utf-8')
        remoteip = packet[1][0]
        remoteport = packet[1][1]
        syslog.syslog("SRC: %s:%s MSG: %s" %
            (remoteip, remoteport, message))

    except BlockingIOError:
        pass

    socket_send.sendto(payload, ('127.0.0.255', 12345))

    time.sleep(1)
