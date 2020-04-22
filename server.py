import socket
import select
import random
import sys
import time
from Questions import Q_and_A
from _thread import *

MSG_LEN = 5
random.shuffle(Q_and_A)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
	print("Correct method: script, IP address, port number")
	exit()

number_of_participants = int(input("Please enter the number of participants(max allowed is 4): "))  
number_joined = 0

if number_of_participants > 4 or number_of_participants < 1:
	while number_of_participants > 4 or number_of_participants < 1:
		number_of_participants = int(input("Please input valid number: "))


IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.bind((IP_address, Port))
server.listen(10)
print("Server started!")

print(f"Waiting for connection on IP address and Port number: {IP_address}, {Port}")

clients_list = []
participants = {}
marks = {}
mapping = {}
Person = [server]
answer = [-1]

def receive_message(client_socket):
	message = client_socket.recv(1024).decode('utf-8')
	return message

def send_to_one(receiver, message):
	message = f"{len(message):<{MSG_LEN}}" + message 
	try:
		receiver.send(bytes(message, 'utf-8'))
	except:
		receiver.close()
		clients_list.remove(receiver)

def send_to_all(sender, message):
	message = f"{len(message):<{MSG_LEN}}" + message
	for socket in clients_list:
		if (socket != server and socket != sender):
			try:
				socket.send(bytes(message, 'utf-8'))
			except:
				socket.close()
				clients_list.remove(socket)

def update_marks(player, number):
	print(participants[mapping[player]])
	marks[participants[mapping[player]]] += number
	print(marks)
	send_to_all(server, "\nScore: ")
	for j in marks:
		send_to_all(server, ">> " + str(j) + ": " + str(marks[j]))

def end_quiz():
	send_to_all(server, "GAME OVER\n")
	print("GAME OVER\n")
	for i in marks:
		if marks[i] >= 5:
			send_to_all(server, "WINNER: " + str(i))
	send_to_all(server, "Scoreboard:")
	print("Scoreboard: ")
	for i in marks:
		send_to_all(server, ">> " + str(i) + ": " + str(marks[i]))
		print(">> " + str(i) + ": " + str(marks[i]))
	sys.exit()

def ask_question():
	if len(Q_and_A) != 0:
		question_and_answer = Q_and_A[0]
		question = question_and_answer[0]
		options = question_and_answer[1]
		Answer = question_and_answer[2]

		random.shuffle(options)
		option_number = 1

		send_to_all(server, "\nQ. " + str(question))
		print("\nQ. " + str(question))
		for j in range(len(options)):
			send_to_all(server, "   " + str(option_number) + ") " + str(options[j]))
			print("   " + str(option_number) + ") " + str(options[j]))
			if options[j] == Answer: 
				answer.pop(0)
				answer.append(int(option_number))
			option_number += 1
		send_to_all(server, "\nHit Enter to answer")
		print("answer: option number " + str(answer))
	else:
		send_to_all(server, "All questions asked!")
		end_quiz()
		sys.exit()

def quiz():
		Person[0] = server
		random.shuffle(Q_and_A)
		ask_question()
		keypress = select.select(clients_list, [], [], 10)
		if len(keypress[0]) > 0:
			who_buzzed = keypress[0][0]
			send_to_one(who_buzzed, "YOU PRESSED THE BUZZER")
			send_to_one(who_buzzed, "ENTER YOUR ANSWER: ")
			send_to_all(who_buzzed, "BUZZER PRESSED")
			print("BUZZER PRESSED")
			time.sleep(0.01)
			Person.pop(0)
			Person.append(who_buzzed)
			t0 = time.time()
			Q_and_A.pop(0)

			answering = select.select(Person, [], [], 10)
			if len(answering) > 0:
				if time.time() - t0 >= 10:
					send_to_one(who_buzzed, "NOT ANSWERED!")
					send_to_all(server, str(participants[mapping[who_buzzed]]) + " -0.5")
					print(str(participants[mapping[who_buzzed]]) + " -0.5")
					update_marks(who_buzzed, -0.5)
					time.sleep(3)
					quiz()
				else:
					time.sleep(3)
					quiz()
			else:
				print("NOTHING!")						
		else:
			send_to_all(server, "BUZZER NOT PRESSED")
			print("BUZZER NOT PRESSED")
			time.sleep(3)
			Q_and_A.pop(0)
			quiz()

clients_list.append(server)

while True:
	rList, wList, error_sockets = select.select(clients_list, [], [])
	for socket in rList:
		if socket == server:
			client_socket, client_address = server.accept()
			if number_joined == number_of_participants:
				send_to_one(client_socket, "Maximum number of players joined!")
				client_socket.close()
			else:
				name = receive_message(client_socket)
				if name:
					if name in participants.values():
						send_to_one(client_socket, "Name already taken. Please choose a different one and join again!")
						client_socket.close()
					else:
						participants[client_address] = name
						marks[name] = 0
						number_joined += 1
						mapping[client_socket] = client_address
						clients_list.append(client_socket)
						print("Participant connected: " + str(client_address) +" [ " + participants[client_address] + " ]" )
						if number_joined < number_of_participants:
							send_to_one(client_socket, "Welcome to the quiz " + name + "!\nPlease wait for other participants to join...")
	
						if number_joined == number_of_participants:
							send_to_all(server, "\nParticipant(s) joined:")
							for i in participants:
								send_to_all(server,">> " + participants[i])
							send_to_all(server, "\nThe quiz will begin in 30 seconds. Quickly go through the instructions\n")
							send_to_all(server, "INSTRUCTIONS:\n> For each question you will be provided 10 seconds to press the buzzer.\n> To press the buzzer, hit Enter.\n> After pressing the buzzer you will be provided 10 seconds to answer the question.\n\n> You will be awarded 1 point in the following case:\n  > If you enter the correct option number after pressing the buzzer first\n\n> 0.5 points will be deducted in the following cases:\n  > If you press the buzzer first and give wrong answer\n  > If you press the buzzer first but don't give the answer\n  > If you provide any other answer other than the option numbers(1 to 4)\n\n> First person to score 5 points and above is the winner\n\nALL THE BEST!")
							print("\n" + str(number_of_participants) + " participant(s) connected! The quiz will begin in 30 seconds")
							time.sleep(30)
							start_new_thread(quiz, ())
		else:
			msg = receive_message(socket)
			print(msg)
			if socket == Person[0]:
				try:
					ans = int(msg)
					if ans == answer[0]:
						send_to_one(socket, "CORRECT ANSWER")
						send_to_all(server, str(participants[mapping[socket]]) + " +1")
						print(str(participants[mapping[socket]]) + " +1")
						update_marks(socket, 1)
						Person[0] = server
						if marks[participants[mapping[socket]]] >= 5:
							end_quiz()
										
					else:
						send_to_one(socket, "WRONG ANSWER")
						send_to_all(server, str(participants[mapping[socket]]) + " -0.5")
						print(str(participants[mapping[socket]]) + " -0.5")
						update_marks(socket, -0.5)
						Person[0] = server
				except ValueError:
					send_to_one(socket, "INVALID OPTION")
					send_to_all(server, str(participants[mapping[socket]]) + " -0.5")
					print(str(participants[mapping[socket]]) + " -0.5")
					update_marks(socket, -0.5)
					Person[0] = server		

			elif Person[0] != server:
				send_to_one(socket, "TOO LATE!")

			
client_socket.close()
server.close()
