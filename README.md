# SocketQuiz
This is a socket based multiplayer quiz based on Python 3.

# Project overview:
There are up to four players in the game. The host (server) has a long list questions and correct answers with him. A random question is sent to all the players. The players press the buzzer by pressing ‘Enter’ key on the keyboard. The first one to press the buzzer within 10 seconds is given chance to answer the question. Otherwise, the host moves to the next question. The answer is to be given within 10 seconds. If the answer given by the player is correct, he is awarded a point. If the player fails to provide an answer in 10 seconds or gives any other answer except the option number or gives wrong answer, 0.5 points are deducted. The host then proceeds with the next question. The game stops when any player gets 5 points or above and then he is declared the winner.

# Features:
1. Up to four players can play.
2. One can choose any player name.
3. A random question is asked each time.
4. For any session, a question is asked only once.
5. For a question, the options will never be displayed in a particular order (options are randomized).
6. Scores of all the players and status of the buzzer is displayed after every question.

# Instructions to run:
1. Start the server with the following command:
                  python3 server.py <IP_address> <Port_Number>
2. Start the client with the following command:
                  python3 client.py <IP_address> <Port_Number>

# Contribute:
Contributions, issues and feature requests are welcome!

# Show your support:
Give a ⭐️ if you find this repo useful!
