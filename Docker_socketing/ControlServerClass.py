import threading
import time
import socket
import re
import select
class ControlServer:
	def __init__ (self,my_hostname, port_no,port_mapping):
		self.my_hostname = my_hostname
		self.port_no = port_no
		self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
		self.MessageList = [[] for _ in range(len(port_mapping))]
		self.client_socket_list = []
		self.client_port_mapping = port_mapping
		self.client_access_check = [ False,False,False ,False]
	def sort_Clients():
		clients = self.client_port_mapping.keys()
		
		

	def get_hostname(self):
		return self.my_hostname
	def get_portName(self):
		return self.port_no

	#for putting the controller in connection ready state 
	def port_bind(self,num_clients):	
		self.control_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.control_socket.bind((self.my_hostname,self.port_no))
		self.control_socket.listen(num_clients)
		#self.conn,addr = self.control_socket.accept()


	def accept_connection(self):
		while True:
			for socket in self.client_socket_list:
				client_thread = threading.Thread(target=self.client_handler,args=(socket,))
				client_thread.start()
	#for handling clients to recieve connections from them 
	def recieve_connection(self):
		conn,addr = self.control_socket.accept()
		while True:
			self.client_socket_list.append(conn)
			print("Connection is successfull")
			return conn

	def client_handler(self,conn):
		conn.setblocking(0)
		while True:
			#print("debug1")
			ready_sock, _, _ = select.select([conn],[],[],1)
			
			if not ready_sock:
				break
				#timeout occured
			#if not ready_sock
			message = conn.recv(2048)
			#print(message)
			if len(message) == 0:
				return
			message = message.decode()

			#if message == "None":
				#print("debug2\n")
			#	break
			#print(message)
			pattern = r"Reciever:\s(.*?)\s*Message:\s(.*?)(?=\$|$)"
			matches = re.findall(pattern,message)
			if matches:
				for match in matches:
					message_dict = { "Reciever": match[0],"Message": match[1]}
					message = match[1]
					#print(match[1])
					self.MessageList[self.client_port_mapping[match[0]]].append(message_dict)
			#if message == "None" or message == "":
			#	break;
				
		self.printMessageList()
		print("...")

	
	def send_to_client(self,clientname):
		for message in self.MessageList[self.client_port_mapping[clientname]]:
			print(len(self.MessageList[self.client_port_mapping[clientname]]))
			client_socket = self.client_socket_list[self.client_port_mapping[clientname]]
			client_socket.send(message["Message"].encode())
			print("br")
			self.printMessageList(clientname)
			self.MessageList[self.client_port_mapping[clientname]].remove(message)
			

	#for sending the data 
	'''def send(self,clientname):
		c = 0
		#self.printMessageList()
		for message in self.MessageList:
			if clientname != message["Reciever"]:
				continue
			c += 1
			socket_1 = socket.socket();
			recv_host_name = message["Reciever"]
			recv_port_no = self.client_port_mapping[recv_host_name]

			socket_1.connect((recv_host_name,recv_port_no))
			socket_1.send(message["Message"].encode())
			print("Connected to ", recv_host_name,"On Port:",recv_port_no)
			print(c,end = "\n")
			socket_1.close();'''
	
	def printMessageList(self,clientname = 'all'):
		if len(self.MessageList) == 0:
			print("List is empty");
		if clientname == 'all':
			all_index = self.client_port_mapping.values()
			all_index = list(all_index)
			for i in all_index:
				for message in self.MessageList[i]:
					print(message['Reciever'],message['Message'],'\n')

		else:
			index = self.client_port_mapping[clientname]
			for message in self.MessageList[index]:
				print(message['Reciever'],message['Message'],'\n')
	def returnMessageList(self,clientname = 'all'):
		
		if len(self.MessageList) == 0:
			print("List is empty");
		if clientname == 'all':
			all_index = self.client_port_mapping.values()
			all_index = list(all_index)
			return self.MessageList[i]
		else:
			index = self.client_port_mapping[clientname]
			return self.MessageList[index]
				
	def printSockets(self):
		for socket in self.client_socket_list:
			print(socket)
	def getSocketList(self):
		return client_socket_list;
	
	def open_channel(self,client1,client2,time_limit):
	
		index_arr = [self.client_port_mapping[client1] , self.client_port_mapping[client2]]
		#for index in index_arr:
		#	print(index,end="")

		for index in index_arr:
			self.client_access_check[index] = True
		else:
			self.client_access_check[index] = False

		start_time = time.time()
		while True:
			self.client_handler(self.client_socket_list[index_arr[0]])
			if len( self.MessageList[self.client_port_mapping[client2]]) > 0:
				self.send_to_client(client2)
			self.client_handler(self.client_socket_list[index_arr[1]])
			if len( self.MessageList[self.client_port_mapping[client1]]) > 0:
				self.send_to_client(client1)
			elapsed_time = time.time() - start_time
			if elapsed_time >= time_limit:
				#self.client_socket_list[index_arr[1]].close()
				
				#self.client_socket_list[index_arr[0]].close()
				break
		print(client1)
		self.printMessageList(clientname = client1)
		print(client2)
		self.printMessageList(clientname = client2)
	def time_elapsed(time_now):
		return (time.time() - time_now)
	def open_channel_interval(self,client1,client2,time_intervals):
		
		time_period = []
		time_start = []
		for time_tuples in time_intervals:
			time_period.append(time_tuples[1] - time_tuples[0])

		#print(time_period)
		#print(time_start)
		time_now = time.time()
		for i in range(len(time_intervals)):
			print(client1,client2)
			while True:
			
				#time_elapsed = time.time() - time_now
				if (time.time() - time_now)  >= time_intervals[i][0] and (time.time() - time_now) < time_intervals[i][1]:
					print("conn:",client1,client2,"start:",time.time() - time_now)
					self.open_channel(client1,client2,time_period[i])

				if (time.time()-time_now)  >= time_intervals[i][1]:
					print("conn:",client1,client2,"end:",time.time()-time_now)
					break
		
		
		
	def start_controller(self):
		Controller = ControlServerClass.ControlServer(my_hostname,controller_port,port_mapping)
		Controller.port_bind(3)
		print('Server has started and is waiting for connections')
		
		connection_list = []
		for i in range(3):
			current_conn = Controller.recieve_connection()
			connection_list.append(current_conn)
	
		while True:
			for current_conn in connection_list:
				Controller.client_handler(current_conn)
	
			ch = input("")
			if ch == "exit":
				break
			#print("Hi  Hi")
			#client_thread = threading.Thread(target=Controller.client_handler,args=(current_conn,))
			#client_thread.start()
			
		#Controller.send_to_client("127.0.0.2")
		#Controller.send_to_client("127.0.0.3")
			
		Controller.printMessageList();

			






			


		
