import socket

HOST = socket.gethostbyname('control_server');
#HOST = "127.0.0.1"
PORT = 9898

control_server_socket = socket.socket();
control_server_socket.bind((HOST,PORT))

while True:
	control_server_socket.listen(1)
	conn,addr = control_server_socket.accept()

	print("Connected to Client")

	req = conn.recv(1024).decode()

	print(req)
	message = input("Enter Y to allow connection")
	conn.send(message.encode())
	if message == 'end':
		break
control_server_socket.close()

#control_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
