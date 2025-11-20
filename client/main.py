import singleplayer
import multiplayer
from intro import intro_screen, clear
from TTT import detect_keypress, initialize_targeted_window

s_player = singleplayer.TTTSinglePlayer()
m_player = multiplayer.TTTMultiPlayer()

if __name__ == '__main__':
    initialize_targeted_window()
    intro_screen()
    detect_keypress()

    looping = True
    while looping:
        clear()
        print('Choose any one of the following: ')
        print('1. Singleplayer')
        print('2. Multiplayer')
        print('3. Controls')
        print('4. Quit Game')
        print('\n>> ', end='')
        key_pressed = detect_keypress()

        match key_pressed:
            case '\'1\'':
                s_player.run()

            case '\'2\'':
                m_player.run()

            case '\'3\'':
                clear()
                string = '''
+======+======+======+
|  11  |  22  |  33  |
|  11  |  22  |  33  |
+------+------+------+
|  44  |  55  |  66  |
|  44  |  55  |  66  |
+------+------+------+
|  77  |  88  |  99  |
|  77  |  88  |  99  |
+======+======+======+

Press the respective number keys for the given squares.
Press any key to continue...
'''
                print(string)
                detect_keypress()

            case '\'4\'':
                looping = False

