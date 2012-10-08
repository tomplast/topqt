#!/usr/bin/env python

import socketserver
import pickle

class ComObject:
	command = None

bombay = pickle.dumps([{"Name": "Karl"}, {"Name": "Tomas"}])
		

class MyTCPHandler(socketserver.BaseRequestHandler):

	def handle(self):
		# self.rfile is a file-like object created by the handler;
		# we can now use e.g. readline() instead of raw recv() calls
		self.data = self.request.recv(1024).strip()
		print(("{} wrote:".format(self.client_address[0])))

		version = "1.0.1"

		try:
			pickle_object = pickle.loads(self.data)
		except Exception as e:
			return

		print(pickle_object)

		if (pickle_object["command"] == "PING"):
			#self.wfile.write(bytes("PONG " + version, "utf-8"))
			self.request.sendall(bytes("PONG " + version, "utf-8"))
		else:
			#self.wfile.write(bytes("Huh?", "utf-8"))
			self.request.sendall(bombay)
			#self.request.sendall(bytes("Huh?", "utf-8"))
			

		#print((self.data))
		# Likewise, self.wfile is a file-like object used to write back
		# to the client
		#self.wfile.write(bytes("Kalle", "utf-8"))


if __name__ == "__main__":
	HOST, PORT = "localhost", 9999

	# Create the server, binding to localhost on port 9999
	server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

	# Activate the server; this will keep running until you
	# interrupt the program with Ctrl-C
	server.serve_forever()
