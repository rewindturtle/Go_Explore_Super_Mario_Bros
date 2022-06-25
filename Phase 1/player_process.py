from Hyperparameters import *
import numpy as np
import super_mario_bros_env
import os


def get_cell(x):
    return int(max(x, 0.) // CELL_SIZE)


def player_process(child_con, player_num):
    np.random.seed(int.from_bytes(os.urandom(4), byteorder='little'))
    env = super_mario_bros_env.make(3)
    num_games = 0
    while True:
        child_con.send(('trajectory', None))
        trajectory = child_con.recv()
        a = 0
        t_idx = 0
        steps = 0
        max_cell = 0
        max_x = 0
        actions = []
        cells = []
        _ = env.reset()
        if RENDER:
            env.render()
        while True:
            if t_idx == len(trajectory):
                if np.random.random() < 0.5:
                    a = np.random.randint(NUM_ACTIONS)
            else:
                a = trajectory[t_idx]
                t_idx += 1
            _, x, done, _ = env.step(a)
            if RENDER:
                env.render()
            actions.append(a)
            cell = get_cell(x)
            max_x = max(x, max_x)
            max_cell = max(cell, max_cell)
            cells.append(cell)
            if done:
                break
            steps += 1
        num_games += 1
        data = [player_num, steps, t_idx, max_cell, num_games, max_x]
        batch = [actions, cells, data]
        child_con.send(('batch', batch))