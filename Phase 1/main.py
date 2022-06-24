from Hyperparameters import *
import multiprocessing as mp
from player_process import player_process
from manager import Manager
import time
import threading


if __name__ == '__main__':
    players = []
    connections = []
    for i in range(NUM_PLAYERS):
        parent_con, child_con = mp.Pipe()
        process = mp.Process(target = player_process, args = (child_con, i))
        players.append(process)
        connections.append(parent_con)

    for p in players:
        p.start()
        time.sleep(1)

    manager = Manager(connections)
    listen_thread = threading.Thread(target = manager.listen)
    listen_thread.start()
    listen_thread.join()