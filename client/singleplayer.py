import random
from TTT import TTT

class TTTSinglePlayer(TTT):
    def get_ai_input(self):
        c_row = random.randint(0, 2)
        c_col = random.randint(0, 2)

        while self.board[c_row][c_col] != self.empty:
            c_row = random.randint(0, 2)
            c_col = random.randint(0, 2)

        self.circle_key_index = [c_row, c_col]

    def run(self):
        while True:
            self.print_board()

            self.add_input()
            self.update_memory(True)

            if self.detect_pattern():
                self.declare_winner()
                break

            self.get_ai_input()
            self.update_memory(False)

            if self.detect_pattern():
                self.declare_winner()
                break


if __name__ == '__main__':
    test = TTTSinglePlayer()
    test.run()
        