import socket
import select
import sys

MSG_LEN = 5

if len(sys.argv) != 3: 
    print("Correct method: script, host IP address, port number")
    exit() 

Host = str(sys.argv[1])
Port = int(sys.argv[2])

name = (input("Enter Name: "))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	server.connect((Host, Port))
except:
	print("CAN'T CONNECT TO SERVER!")
	sys.exit()

server.setblocking(False)

def send_name_to_server(socket, message):
	if message == "":
		print("Please choose a name and join again")
		print("DISCONNECTED")
		sys.exit()
	else:
		try:
			socket.send(bytes(message, 'utf-8'))
		except:
			socket.close()
			clients_list.remove(receiver)

def send_to_one(socket, message):
	try:
		socket.send(bytes(message, 'utf-8'))
	except:
		socket.close()
		clients_list.remove(receiver)

def receive_message(client_socket):
	try:
		msg_len = client_socket.recv(MSG_LEN)

		if not len(msg_len):
			return False

		message_length = int(msg_len.decode('utf-8').strip())
		return {'Length': msg_len, 'data': client_socket.recv(message_length)}

	except:
		return False

send_name_to_server(server, name)

while True:
	sockets_list = [sys.stdin, server]
	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
	for socket in read_sockets:
		if socket == server:
			encoded_message = receive_message(socket)
			if not encoded_message :
				print("DISCONNECTED")
				sys.exit()
			else:
				message = encoded_message['data'].decode('utf-8')
				print(message)

		else:
			message = sys.stdin.readline()
			send_to_one(server, message)
server.close()
sys.exit()
