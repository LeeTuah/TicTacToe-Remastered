import socket
import threading
import random
from pynput.keyboard import Key, Listener
import os
import platform

key_pressed = ''

PORT = 6741
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'

JOIN_MSG = '!join'
HOST_MSG = '!host'
ABORT_MSG = '!abort'
START_MSG = '!start'
LEAVE_MSG = '!leave'

EMPTY = 0
CROSS = 1
CIRCLE = 2

ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

user_data = {} # username -> {"client": client, "addr": addr, "has_room": bool, "room_id": int/None, "opp_name": None, "ingame": False}
currently_online_rooms = {} # room_id -> [player1, player2]
currently_playing_rooms = []

def clear():
    if platform.system() == 'Windows':
        os.system('cls')

    else:
        os.system('clear')

def detect_keypress():
    def press(key):
        global key_pressed
        key_pressed = key
        return False
    
    with Listener(on_press=press) as listener:
        listener.join()

def program_controls():
    while True:
        detect_keypress()

        if key_pressed == Key.delete:
            os._exit(0)

def handle_connections(client: socket.socket, addr):
    connected = True
    get_username = True
    valid_username = True
    room_id = None
    other_client_name = ''
    username = ''

    while connected:
        try:
            message = client.recv(1024).decode(FORMAT)

            if not message:
                break

            elif get_username:
                get_username = False
                username = message

                if username in user_data.keys():
                    client.send('403|The username already exists, please try again!'.encode(FORMAT))
                    connected = False
                    valid_username = False
                    print(f'[DISCONNECT] {addr[0]}:{addr[1]} has disconnected.')
                    break

                user_data[username] = {"client": client, "addr": addr, "has_room": False, "room_id": None, "opp_name": None, "ingame": False}
                client.send('200|Successfully joined the server'.encode(FORMAT))
                print(f'[CONNECT] {username} has connected to the server.')

                continue

            elif user_data[username]['ingame']:
                    opp_name = user_data[username]['opp_name']

                    if message == ABORT_MSG:
                        print(f'[GAME] Match ended in Room {room_id}')
                        user_data[username]['ingame'] = False
                        user_data[opp_name]['ingame'] = False

                        user_data[username]['opp_name'] = None
                        user_data[opp_name]['opp_name'] = None

                        user_data[username]['has_room'] = False
                        user_data[opp_name]['has_room'] = False

                        user_data[username]['room_id'] = None
                        user_data[opp_name]['room_id'] = None

                    else:
                        user_data[opp_name]['client'].send(message.encode(FORMAT))

                    continue

            elif message == HOST_MSG:
                if user_data[username]['has_room']:
                    client.send('403|00000000|You already have a room created. Please exit it beforehand.'.encode(FORMAT))
                    print(f'[HOST] {username} attempted to host a room, but failed.')
                    continue

                user_data[username]['has_room'] = True
                
                room_id = str(random.randint(11111111, 99999999))
                user_data[username]['room_id'] = room_id
                currently_online_rooms[room_id] = [username]

                print(f'[HOST] {username} created a room with ID {room_id}.')
                client.send(f'200|{room_id}|Your room has been hosted successfully.'.encode(FORMAT))
                # 200|11111111|Your room has been hosted successfully.

            elif message == START_MSG:
                if not room_id or not room_id in currently_online_rooms:
                    continue

                players = currently_online_rooms[room_id]

                if len(players) < 2:
                    client.send('400|Not enough players.'.encode(FORMAT))
                    continue

                p1 = players[0]
                p2 = players[1]

                user_data[p1]['opp_name'] = p2
                user_data[p2]['opp_name'] = p1
                user_data[p1]['ingame'] = True
                user_data[p2]['ingame'] = True

                user_data[p2]['client'].send('200|Match Started...'.encode(FORMAT))
                print(f'[GAME] Room {room_id}: {p1} vs {p2}')
            
            elif message[0:len(JOIN_MSG)] == JOIN_MSG:
                try:
                    split = message.split(' ')
                    room_id = split[1]

                    if (not room_id in list(currently_online_rooms.keys())) or (room_id in currently_playing_rooms):
                        print(f'[JOIN] {username} attempted to join a room, but failed. (Try-block)')
                        client.send('404|This Room does not exist or busy. Please try again.'.encode(FORMAT))
                        room_id = None
                        continue
                    
                    user_data[username]['has_room'] = True
                    user_data[username]['room_id'] = room_id

                    currently_online_rooms[room_id].append(username)
                    currently_playing_rooms.append(room_id)
                    print(f'[JOIN] {username} has successfully joined the room with ID {room_id}.')
                    client.send('200|Successfully joined the room.'.encode(FORMAT))
                    
                    other_client_name = currently_online_rooms[room_id][0]
                    user_data[other_client_name]['client'].send(f'200|{username} has joined your room.'.encode(FORMAT))

                except IndexError:
                    print(f'[DEBUG] {username} sent an invalid Join Command.')
                    client.send('402|Invalid Command Sent.'.encode(FORMAT))
                    continue

                except KeyError:
                    print(f'[JOIN] {username} attempted to join a room, but failed. (KeyError)')
                    client.send('404|Invalid Room ID was provided. Please try again.'.encode(FORMAT))
                    continue

            elif message == LEAVE_MSG:
                if user_data[username]['has_room']:
                    cache_list = currently_online_rooms[room_id]

                    if username == cache_list[0]:
                        if len(cache_list) > 1:
                            user_data[cache_list[1]]['client'].send('404|The Room was closed.'.encode(FORMAT))
                            user_data[cache_list[1]]['has_room'] = False
                            user_data[cache_list[1]]['room_id'] = None

                        print(f'[LEAVE] {username} closed a room with ID {room_id}')
                        user_data[username]['has_room'] = False
                        user_data[username]['room_id'] = None
                        client.send('201|The Room was closed.'.encode(FORMAT))
                        room_id = None
                    
                    elif username == cache_list[1]:
                        user_data[cache_list[0]]['client'].send(f'400|{username} has left the room.'.encode(FORMAT))

                        user_data[username]['has_room'] = False
                        user_data[username]['room_id'] = None

                        currently_playing_rooms.remove(room_id)
                        currently_online_rooms[room_id].pop()

                        print(f'[LEAVE] {username} left the room with ID {room_id}.')
                        client.send('201|You have left the room.'.encode(FORMAT))
                        room_id = None

        except ConnectionRefusedError:
            connected = False

        except ConnectionResetError:
            connected = False

    if valid_username:
        client.close()
        if user_data[username]['has_room']:
            room_id = user_data[username]['room_id']
            currently_online_rooms.pop(user_data[username]['room_id'])

            if room_id in currently_playing_rooms:
                currently_playing_rooms.remove(room_id)

        user_data.pop(username)
        print(f'[LEAVE] {username} has disconnected.')

    else:
        client.close()
        print(f'[LEAVE] ({addr[0]}:{addr[1]}) has disconnected.')

def start():
    clear()

    server.listen()
    print('[DEBUG] Server is listening...')
    print('[DEBUG] Press Delete Key to close the server.')

    program_control_thread = threading.Thread(target=program_controls)
    program_control_thread.start()

    while True:
        client, addr = server.accept()
        print(f'[CONNECT] {addr[0]}:{addr[1]} attempting to connect.')

        handle_thread = threading.Thread(target=handle_connections, args=(client, addr))
        handle_thread.start()

if __name__ == '__main__':
    start()