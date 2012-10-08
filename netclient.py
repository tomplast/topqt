#!/usr/bin/env python

import socket
import sys
import pickle

HOST, PORT = "localhost", 9999


com_object = {"command": "HAHAHA"}

data = pickle.dumps(com_object)

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	# Connect to server and send data
	sock.connect((HOST, PORT))
	sock.sendall(data)

	# Receive data from the server and shut down
	received = sock.recv(1024)
	kalle = pickle.loads(received)
	for i in kalle:
		print(i["Name"])
finally:
	sock.close()

print(("Sent:	 {}".format(data)))
