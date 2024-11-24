import os

def clean():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
