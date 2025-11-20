from pynput.keyboard import Listener
from intro import clear, game_over_text, gg_text, slow_print
import time
from copy import deepcopy
import pygetwindow as gw

key_pressed = ''
TARGET_WINDOW = ''

def initialize_targeted_window():
    global TARGET_WINDOW
    TARGET_WINDOW = gw.getActiveWindow()

def detect_keypress():
    global key_pressed
    def press(key):
        global key_pressed
        try:
            active_window = gw.getActiveWindow()
            if active_window and active_window == TARGET_WINDOW:
                key_pressed = str(key)

            else:
                key_pressed = ''
        
        except AttributeError:
            key_pressed = ''

        return False
    
    with Listener(on_press=press) as listener:
        listener.join()

    return key_pressed

class TTT:
    empty = 0
    cross = 1
    circle = 2

    client_symbol = empty
    other_symbol = empty

    board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    cross_key_index = [0, 0]
    circle_key_index = [0, 0]
    wins = [False, False] # (Cross Wins, Circle Wins)

    cross_memory = []
    circle_memory = []

    def __init__(self):
        self.update_symbols(self.cross)

    def print_board(self):
        clear()
        print('+======+======+======+')

        for i in range(3):
            for j in range(2):
                print(end='|')

                for k in range(3):
                    print(end='  ' + ('  ' if self.board[i][k] == self.empty else 'XX' if self.board[i][k] == self.cross else 'OO') + '  |', flush=True)

                if j == 0:
                    print()

            if i != 2:
                print(end='\n+------+------+------+', flush=True)

            print()     

        print('+======+======+======+')

    def add_input(self):
        global key_pressed
        detect_keypress()

        while True:
            if not (key_pressed in [f'\'{i}\'' for i in range(1, 10)]):
                detect_keypress()
                continue

            key_int = int(key_pressed[1])
            k_index = [0, key_int - 1] if key_int in range(1, 4) else [1, key_int - 4] if key_int in range(4, 7) else [2, key_int - 7]
            c_index = self.board[k_index[0]][k_index[1]]

            if c_index != self.empty:
                detect_keypress()
                continue

            if self.client_symbol == self.cross:
                self.cross_key_index = k_index

            elif self.client_symbol == self.circle:
                self.circle_key_index = k_index
            
            break

    def update_symbols(self, client_symbol):
        self.client_symbol = client_symbol
        self.other_symbol = self.circle if client_symbol == self.cross else self.cross

    def update_memory(self, cross: bool):
        if cross:
            if len(self.cross_memory) == 3:
                removed = self.cross_memory.pop(0)
                self.board[removed[0]][removed[1]] = self.empty

            self.cross_memory.append(self.cross_key_index)
            self.board[self.cross_key_index[0]][self.cross_key_index[1]] = self.cross
    
        else:
            if len(self.circle_memory) == 3:
                removed = self.circle_memory.pop(0)
                self.board[removed[0]][removed[1]] = self.empty

            self.circle_memory.append(self.circle_key_index)
            self.board[self.circle_key_index[0]][self.circle_key_index[1]] = self.circle

    def detect_pattern(self):
        temp_board = deepcopy(self.board)

        for i in range(3):
            # Horizontal
            if (temp_board[i][1] != self.empty) and (temp_board[i][0] == temp_board[i][1] and temp_board[i][1] == temp_board[i][2]):
                self.wins[0 if temp_board[i][1] == self.cross else 1] = True
                return True
            
            # Vertical
            if (temp_board[1][i] != self.empty) and (temp_board[0][i] == temp_board[1][i] and temp_board[1][i] == temp_board[2][i]):
                self.wins[0 if temp_board[1][i] == self.cross else 1] = True
                return True
            
        # Both Diagonals
        if (temp_board[1][1] != self.empty) and ((temp_board[0][0] == temp_board[1][1] and temp_board[1][1] == temp_board[2][2]) or (temp_board[0][2] == temp_board[1][1] and temp_board[1][1] == temp_board[2][0])):
            self.wins[0 if temp_board[1][1] == self.cross else 1] = True
            return True
            
        return False
    
    def declare_winner(self):
        self.print_board()
        sleep_amount = 1
        time.sleep(sleep_amount)

        clear()
        if self.wins[0]:
            if self.client_symbol == self.cross:
                slow_print(gg_text, 5)
                print('\nYou Won.')
                time.sleep(sleep_amount)

            else:
                slow_print(game_over_text, 1)
                print('\nYou Lost.')
                time.sleep(sleep_amount)

        elif self.wins[1]:
            if self.client_symbol == self.circle:
                slow_print(gg_text, 5)
                print('\nYou Won.')
                time.sleep(sleep_amount)

            else:
                slow_print(game_over_text, 1)
                print('\nYou Lost.')
                time.sleep(sleep_amount)
