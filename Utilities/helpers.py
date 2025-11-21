import os

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
    return

def pause():
    input("Presione Enter para continuar...")
    return

def set_db_path():
    path = os.path.join(os.path.dirname(__file__), '..', 'Data', 'roulette_data.db')
    return os.path.abspath(path)