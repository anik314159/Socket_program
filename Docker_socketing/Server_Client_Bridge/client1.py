import socket

def call_client(client_name,message):
	self_socket = socket.socket();
	HOST = socket.gethostbyname(client_name);
	PORT = 8085
	self_socket.connect((HOST,PORT))
	self_socket.send(message.encode())


	

HOST = socket.gethostbyname('control_server');
PORT = 9898

client_control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

client_control_socket.connect((HOST,PORT))

client_control_socket.send(b"REQ:2");

Ack_message = client_control_socket.recv(1024).decode();

if Ack_message == "Y":
	call_client("client2","Hi Bro from CLient1");


server_socket = socket.socket()
HOST = socket.gethostbyname('client1');
PORT = 8086

server_socket.bind((HOST,PORT))

server_socket.listen(1)
conn,addr = server_socket.accept()
message = conn.recv(1024).decode()
print(message);



	
	
