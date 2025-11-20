from TTT import TTT, detect_keypress
import socket
from intro import clear
import time
import threading

PORT = 6741
SERVER = '192.168.1.4'
FORMAT = 'utf-8'

JOIN_MSG = '!join'
HOST_MSG = '!host'
ABORT_MSG = '!abort'
START_MSG = '!start'
LEAVE_MSG = '!leave'

ADDR = (SERVER, PORT)

class TTTMultiPlayer(TTT):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    message_history = []
    username = ''
    terminate = False
    close_terminate_thread = False

    def terminate_room(self):
        while not self.close_terminate_thread:
            key_pressed = detect_keypress()

            if key_pressed == '\'s\'':
                self.terminate = True
                self.client.send(LEAVE_MSG.encode(FORMAT))

    def get_other_input(self):
        message = self.client.recv(1024).decode(FORMAT)
        splitted_msg = message.split()

        # self.board[int(splitted_msg[0])][int(splitted_msg[1])] = self.circle if self.other_symbol == self.circle else self.cross
        if self.other_symbol == self.cross:
            self.cross_key_index = [int(splitted_msg[0]), int(splitted_msg[1])]

        elif self.other_symbol == self.circle:
            self.circle_key_index = [int(splitted_msg[0]), int(splitted_msg[1])]

    def run_game(self):
        while True:
            self.print_board()

            if self.client_symbol == self.cross:
                self.add_input()
                self.client.send((' '.join(map(str, self.cross_key_index))).encode(FORMAT))

            else:
                self.get_other_input()

            self.update_memory(True)

            if self.detect_pattern():
                self.client.send(ABORT_MSG.encode(FORMAT))
                self.declare_winner()
                break

            self.print_board()

            if self.client_symbol == self.circle:
                self.add_input()
                self.client.send((' '.join(map(str, self.circle_key_index))).encode(FORMAT))

            else:
                self.get_other_input()

            self.update_memory(False)

            if self.detect_pattern():
                self.client.send(ABORT_MSG.encode(FORMAT))
                self.declare_winner()
                break

    def run(self):
        clear()

        username = input('Enter your username: ')
        self.username = username
        self.client.connect(ADDR)
        self.client.send(username.encode(FORMAT))

        msg = self.client.recv(1024).decode(FORMAT)
        print(msg[4:])

        if msg[0:3] != '200':
            return -1
        
        looping = True
        while looping:
            self.terminate = False
            clear()
            print('Choose any one of the following: ')
            print('1. Host a Room')
            print('2. Join a Room')
            print('3. Go Back')
            print('\n>> ', end='')
            key_pressed = detect_keypress()

            match key_pressed:
                case '\'1\'':
                    self.client.send(HOST_MSG.encode(FORMAT))

                    message = self.client.recv(1024).decode(FORMAT)
                    status_code = message[0:3]
                    room_id = message[4:12]
                    message = message[13:]

                    clear()
                    print(message)
                    time.sleep(3)

                    if status_code != '200':
                        continue

                    while not self.terminate:
                        self.close_terminate_thread = False
                        termination_thread = threading.Thread(target=self.terminate_room)
                        termination_thread.start()

                        clear()
                        print(f'Your Room ID is {room_id}')
                        print('Sharing this to others will let them join your room.')
                        print('Press \'S\' to close the room.')

                        for i in self.message_history:
                            print(i)

                        msg = self.client.recv(1024).decode(FORMAT)
                        self.message_history.append(msg[4:])
                        print(f'\n\n{msg[4:]}')
                        status_code = msg[0:3]
                        time.sleep(2)

                        self.close_terminate_thread = True

                        if status_code == '400':
                            continue

                        if status_code == '201':
                            self.terminate = True

                        if self.terminate or status_code != '200':
                            continue

                        print('Press \'W\' to start the match.')
                        key_pressed = detect_keypress()

                        if key_pressed == '\'w\'':
                            print('\nStarting Match...')
                            time.sleep(5)

                            self.client.send(START_MSG.encode(FORMAT))
                            self.update_symbols(self.cross)
                            self.run_game()
                            return -1

                case '\'2\'':
                    clear()
                    room_id = input('Enter Room ID: ')
                    self.client.send(f'{JOIN_MSG} {room_id}'.encode(FORMAT))

                    message = self.client.recv(1024).decode(FORMAT)
                    status_code = message[0:3]
                    message = message[4:]

                    print(message)
                    time.sleep(3)

                    if status_code != '200':
                        continue

                    while not self.terminate:
                        self.close_terminate_thread = False
                        termination_thread = threading.Thread(target=self.terminate_room)
                        termination_thread.start()

                        clear()
                        print(f'The Room ID is {room_id}')
                        print('Sharing this to others will let them join the room.')
                        print('Press \'S\' to exit the room.')
                        print('\nWaiting for host to start the match...')

                        for i in self.message_history:
                            print(i)

                        msg = self.client.recv(1024).decode()
                        self.message_history.append(msg[4:])
                        print(f'\n\n{msg[4:]}')
                        time.sleep(2)
                        status_code = msg[0:3]

                        self.close_terminate_thread = True

                        if status_code == '201':
                            continue

                        if status_code == '404':
                            self.terminate = True

                        if status_code != '200' or self.terminate:
                            continue
                        
                        self.update_symbols(self.circle)
                        self.run_game()
                        return -1

                case '\'3\'':
                    looping = False

        self.client.close()