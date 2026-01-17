import os

def set_db_path():
    path = os.path.join(os.path.dirname(__file__), '..', 'Data', 'roulette_data.db')
    return os.path.abspath(path)