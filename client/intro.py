import os
import platform
import time

python = """
⠀⣰⡶⣶⣶⡶⠤⠶⢿⣿⣿⣷⣄
⠀⣿⣿⣿⢻⣧⣀⠀⠀⣿⣿⣿⣏⠷⣦⣀⡀⠀⠀⠀⣀⣀⣀⣄⣀⣀⣀⡀
⠀⢿⣿⠙⠻⣿⣿⢶⣄⠙⠻⠟⠋⠀⠀⠈⣙⣿⠛⠛⢻⣹⣥⣿⣫⠼⠋⠙⠛⣦⣄
⠀⠀⠉⠀⠀⠹⠏⠛⢿⣿⢦⣄⡀⠤⢤⣤⡀⠙⢠⡀⠈⠻⣦⣼⠇⠀⠀⠀⢸⡇⣿⠻⣦
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣇⠈⠉⢛⡟⠙⠃⠀⠘⣧⣀⣀⣈⣉⣀⠀⠀⠀⢠⡇⢸⣇⣈⢷⡀ 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⣠⣾⠃⠀⠀⠀⢰⡏⠁⠀⠀⠈⠙⢷⡄⠀⠈⠳⠞⠓⢮⡉⣧
⠀⠀⢀⣤⣴⣾⡿⠿⢿⣿⢿⣿⠟⠁⣀⣀⣠⡴⠋⠀⠀⠀⠀⠀⠀⠀⣷⠀⠀⠀⠀⠀⠀⠙⢻⡇
⠀⣰⣏⡿⠋⠁⢀⣠⢞⣡⠞⢁⣠⠞⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡟⠀⠀⠀⠀⠀⣀⠀⢸⡇
⠠⢿⣿⠁⠀⢰⡿⠛⠋⢁⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡟⠀⣀⣀⡀⠀⣾⠉⠉⢻⡇
⠀⠀⠀⠀⠀⠘⠿⠞⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠋⠀⠀⣯⠀⠉⣻⣯⡶⢲⡞
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣰⠞⠋⠀⠀⠀⠀⣸⠆⠠⣇⠀⠀⣾⠃
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠾⠋⠀⠀⠀⠀⠀⠀⠀⠈⠓⠢⣬⢻⣾⠃
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡴⠛⠁⠀⢀⣀⣀⢀⣀⠀⠀⠀⠀⠀⠀⣸⡿⠁
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠞⠉⠀⠀⠀⠀⠘⣇⠈⠉⠉⢳⡄⠀⠀⢀⡼⠋
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠟⠁⠀⠀⠀⠀⠀⠀⣠⠾⢀⡾⢳⡀⢳⣄⡴⠛⠁ 
⠀⠀⠀⠀⠀⠀⠀⠀⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠰⡏⠀⢿⡀⠈⣧⡾⠋ 
⠀⠀⠀⠀⠀⠀⠀⣾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⢦⣀⣿⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣶⠶⢶⣶⡶⠦⣄⣀⡀
⠀⠀⠀⠀⠀⠀⣼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⠶⠛⠉⠀⠙⠦⣄⠈⣹⡄⠀⠉⡽⠶⣄
⠀⠀⠀⠀⠀⢠⡟⠀⠀⠀⠀⠀⠀⢀⡖⠒⢦⣤⣰⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⠟⢳⣄⠀⠀⠀⠀⠀⣿⠀⠛⠛⠢⠞⠁⢀⣘⣦⡀
⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⢀⣼⡇⢸⡖⣾⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⢯⣀⣸⠃⠀⠀⠀⠀⠀⣿⣠⠴⢦⣄⣀⡼⠋⠀⠘⣧
⠀⠀⠀⠀⠀⢸⠃⠀⠀⠀⠀⢠⠟⢿⣿⣩⣴⢿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣁⠴⠟⠉⢳⡄⠀⠀⠀⣀⣈⠀⠀⠀⠈⠁⠀⠀⠀⠀⣿⠀⠀⠀⠀⠰⣶⣶⢤⣄⠀⠀⠀
⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠈⢧⣀⡭⠤⣿⢈⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣟⠉⢁⡴⠒⠒⠚⢁⣤⠞⠋⠉⠉⠛⠳⣄⠀⠀⠀⣤⠖⢒⣿⠀⠀⠀⠀⠀⠀⠈⢧⡈⢳⡄⠀
⠀⠀⠀⠀⠀⢹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠉⠙⣧⣄⠀⠀⠀⠀⢀⣠⡾⠋⠈⠉⠁⠀⠀⠀⣰⠟⠀⠀⠀⠀⠀⠀⠀⠈⢷⠀⠀⣸⣦⣿⡏⠀⠀⠀⠀⠀⠀⠀⠈⣷⠀⢿⡀
⠀⠀⠀⠀⠀⢸⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡦⢸⡇⢹⡙⠓⣶⠚⠋⣿⠀⠀⠀⠀⠀⠀⠀⣼⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⢤⠟⢁⣛⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⣼⢳⠈⣧
⠀⠀⠀⠀⠀⠀⢿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⢣⠀⣱⠀⣸⠀⣠⠟⠀⠀⠀⠀⠀⠀⣼⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠈⠉⠉⢹⡇⠀⠀⠀⠀⠀⠀⠀⠀⢠⣏⣘⣧⣿
⠀⠀⠀⠀⠀⠀⠈⢿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣞⠀⣿⣋⠁⣸⠃⠀⠀⠀⠀⠀⠀⣴⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⡄⠀⢀⠼⣧⡀⠀⠀⠀⠀⠀⠀⣠⠟⠁⠉⢀⡏
⠀⠀⠀⠀⠀⠀⠀⠀⠹⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⢀⣴⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣷⡀⠘⠒⠚⠻⣶⣤⣤⡤⠶⣿⠁⠀⠀⢀⡿⠁
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢶⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡞⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣄⠀⠀⠀⣧⡙⢻⡶⠚⠁⠀⢀⡴⠟
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠲⢤⣤⣤⣀⣀⣀⣀⣀⣤⣤⠴⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠶⢤⣤⣿⣾⣥⣤⠶⠛⠋
"""

lee = """
    lee lee lee                            lee lee lee lee lee lee lee lee lee      lee lee lee lee lee lee lee lee lee
    lee lee lee                            lee lee lee lee lee lee lee lee lee      lee lee lee lee lee lee lee lee lee
    lee lee lee                            lee lee lee lee lee lee lee lee lee      lee lee lee lee lee lee lee lee lee
    lee lee lee                            lee lee lee                              lee lee lee
    lee lee lee                            lee lee lee                              lee lee lee
    lee lee lee                            lee lee lee lee lee lee lee lee lee      lee lee lee lee lee lee lee lee lee
    lee lee lee                            lee lee lee lee lee lee lee lee lee      lee lee lee lee lee lee lee lee lee
    lee lee lee                            lee lee lee                              lee lee lee
    lee lee lee lee lee lee lee lee lee    lee lee lee                              lee lee lee
    lee lee lee lee lee lee lee lee lee    lee lee lee lee lee lee lee lee lee      lee lee lee lee lee lee lee lee lee 
    lee lee lee lee lee lee lee lee lee    lee lee lee lee lee lee lee lee lee      lee lee lee lee lee lee lee lee lee
    lee lee lee lee lee lee lee lee lee    lee lee lee lee lee lee lee lee lee      lee lee lee lee lee lee lee lee lee
"""

game_over_text = """
        g g g g g               a a a a a a           m m m m           m m m m    e e e e e e e e e e 
      g g g   g g g            a a a a a a a          m m m m m       m m m m m    e e e e e e e e e e 
    g g g       g g g         a a a     a a a         m m m   m m   m m   m m m    e e e 
    g g g                    a a a       a a a        m m m     m m m     m m m    e e e 
    g g g                   a a a a a a a a a a       m m m       m       m m m    e e e e e e e e e e 
    g g g     g g g g      a a a a a a a a a a a      m m m               m m m    e e e 
      g g g g g   g g     a a a             a a a     m m m               m m m    e e e 
        g g g g   g g    a a a               a a a    m m m               m m m    e e e e e e e e e e 
          g g     g g   a a a                 a a a   m m m               m m m    e e e e e e e e e e 


        o o o o o       v v v               v v v    e e e e e e e e e e    r r r r r 
      o o o   o o o      v v v             v v v     e e e e e e e e e e    r r r   r r 
    o o o       o o o     v v v           v v v      e e e                  r r r     r r 
    o o           o o      v v v         v v v       e e e                  r r r   r r 
    o               o       v v v       v v v        e e e e e e e e e e    r r r r r 
    o o           o o        v v v     v v v         e e e                  r r r r r r   
    o o o       o o o         v v v   v v v          e e e                  r r r   r r r 
      o o o   o o o            v v v v v v           e e e e e e e e e e    r r r     r r r 
        o o o o o               v v v v v            e e e e e e e e e e    r r r       r r r 
"""

gg_text = """
        g g g g g             g g g g g 
      g g g   g g g         g g g   g g g 
    g g g       g g g     g g g       g g g 
    g g g                 g g g 
    g g g                 g g g 
    g g g     g g g g     g g g     g g g g  
      g g g g g   g g       g g g g g   g g 
        g g g g   g g         g g g g   g g 
          g g     g g           g g     g g s
"""

tttremastered = """

    T T T T T T T T T T T T T T T T T T T T                i i i i                    
    T T T T T T T T T T T T T T T T T T T T              i i i i i i    
    T T T T T T T T T T T T T T T T T T T T                i i i i                  c c c c c
                T T T T T T T                                                    c c c c c
                T T T T T T T                              i i i i             c c c c
                T T T T T T T                              i i i i            c c c c
                T T T T T T T                              i i i i            c c c
                T T T T T T T                              i i i i            c c c c
                T T T T T T T                              i i i i             c c c c
                T T T T T T T                              i i i i               c c c c c
                T T T T T T T                              i i i i                  c c c c c    
                T T T T T T T
                T T T T T T T                             a a a a a                c c c c c
                T T T T T T T                          a a a     a a            c c c c c
                T T T T T T T                                    a a          c c c c
                T T T T T T T                            a a a a a a         c c c c          
                T T T T T T T                          a a a     a a         c c c
                T T T T T T T                         a a        a a         c c c c
                T T T T T T T                         a a        a a          c c c c
                T T T T T T T                         a a a      a a            c c c c c
                T T T T T T T                            a a a a a a               c c c c c  
                T T T T T T T
                T T T T T T T
                T T T T T T T                             o o o o o              e e e e e 
                T T T T T T T                           o o o   o o o          e e e e e e e e
                T T T T T T T                         o o o       o o o      e e e          e e e 
                T T T T T T T                         o o           o o      e e e           e e e 
                T T T T T T T                         o               o      e e e e e e e e e e e
                T T T T T T T                         o o           o o      e e e e e e e e e e   
                T T T T T T T                         o o o       o o o      e e e                
                T T T T T T T                           o o o   o o o          e e e e e e e e 
                T T T T T T T                             o o o o o              e e e e e e e e

"""

def slow_print(text: str, delay=50):
    for i in text:
        print(end=i, flush=True)
        time.sleep(delay/1000)

def clear():
    if platform.system() == 'Windows':
        os.system('cls')

    else:
        os.system('clear')

def intro_screen(speed_multiplier=1):
    clear()
    slow_print('Made in...', 170 / speed_multiplier)
    slow_print(python, 1 / speed_multiplier)
    time.sleep(2.5 / speed_multiplier)

    clear()
    slow_print('An Original Product Of...', 100 / speed_multiplier)
    print('\n')
    slow_print(lee, 2 / speed_multiplier)
    time.sleep(1 / speed_multiplier)

    clear()
    slow_print(tttremastered, 0.8 / speed_multiplier)
    print('\n\n\n                               ', end='')
    slow_print('<-- R E M A S T E R E D      E D I T I O N -->', 45 / speed_multiplier)
    time.sleep(0.2 / speed_multiplier)
    print(end='\n\n\n\n\nPress any key to start the game...')


if __name__ == '__main__':
    intro_screen()

    