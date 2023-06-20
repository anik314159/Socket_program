import socket

#HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 9898        # The port used by the server
HOST = socket.gethostbyname('ipc_server_dns_name')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
	message = input("Client:");
	s.sendall(message.encode())
	data = s.recv(1024)

print('Received', repr(data))
