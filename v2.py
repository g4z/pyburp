#!/usr/local/bin/python

import sys
import socket
import time

if len(sys.argv) < 2:
    print("Invalid invocation. Byebye...")
    sys.exit(254)

# server = "irc.freenode.net"
server = "10.93.188.1"
port = 6667
channel = "#test"
botnick = sys.argv[1]

nodes = []

socket_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_recv.bind(('', 12345))
socket_recv.setblocking(0)

socket_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_send.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# irc.send(bytes("PASS %s\n" % (password)))
# irc.setblocking(False)

def connect():
    print("Connecting to [%s:%u]" % (server, port))
    irc.connect((server, port))
    print(irc.recv(1024).decode("UTF-8"))
    print(irc.recv(1024).decode("UTF-8"))

def authorise():
    print("Authorising as [%s]" % (botnick))
    irc.send(bytes("USER " + botnick + " " + botnick + " " + botnick + " :" + botnick + "\n", "UTF-8"))
    irc.send(bytes("NICK " + botnick + "\n", "UTF-8"))
    print(irc.recv(1024).decode("UTF-8"))
    print(irc.recv(1024).decode("UTF-8"))

def joinChannel():
    print("Joining channel [%s]" % (channel))
    buffer = ""
    irc.send(bytes("JOIN " + channel + "\n", "UTF-8"))
    while buffer.find("End of /NAMES list.") == -1:  
        buffer = irc.recv(1024).decode("UTF-8")
        buffer = buffer.strip('\n\r')
        print(buffer)

def ping(): # respond to server Pings.
    print("Sending PONG")
    irc.send(bytes("PONG :pingis\n", "UTF-8"))

def sendmsg(msg, target=channel): # sends messages to the target.
    message = "PRIVMSG " + target + " :" + msg + "\n"
    print("Sending: %s" % message)
    irc.send(bytes(message, "UTF-8"))

def main():

    connect()
    authorise()
    joinChannel()

    sendmsg("Hello everybody!")

    irc.setblocking(False)

    t_start =  time.time()

    while True:

        try:
            packet = socket_recv.recvfrom(2048)
            message = packet[0].decode('utf-8')
            remoteip = packet[1][0]
            remoteport = packet[1][1]
            if not remoteip in nodes:
                nodes.append(remoteip)
        except BlockingIOError:
            pass

        try:
            response = irc.recv(1024).decode()
            print("Received: %s" % response)

            # if response.find('PRIVMSG') != -1:
            #     sendmsg("...whatever...")

            if response.find('PING') != -1:
                pong()

        except Exception as e:
            pass

        if int((time.time() - t_start) % 10) == 0:

            nodelist = ','.join([str(node) for node in nodes])
            sendmsg("nodes(%s)" % nodelist)
            # print(nodelist)

            # print("Broadcast HELLO")
            socket_send.sendto(
                bytes("HELLO", "UTF-8"),
                ('127.0.0.255', 12345)
            )

        # print(".")

        time.sleep(1)

main()
