
import time
from socket import *

payload = b'hello world'

socket_recv = socket(AF_INET, SOCK_DGRAM)
socket_recv.bind(('', 12345))
socket_recv.setblocking(0)

socket_send = socket(AF_INET, SOCK_DGRAM)
socket_send.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

while True:
	try:
		message = socket_recv.recvfrom(1024)
		syslog.syslog("Received: " + message)

	except BlockingIOError:
		pass

	socket_send.sendto(payload, ('127.0.0.255', 12345))

	time.sleep(1)
