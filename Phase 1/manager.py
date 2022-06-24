from Hyperparameters import *
import numpy as np
from copy import deepcopy


class Manager:
    def __init__(self, connections):
        self.connections = connections

        self.trajectories = [[0]]
        self.min_cell_steps = [999]
        self.cell_visits = [0]
        self.num_games = 0

    def update_memory(self, data):
        actions, cells, game_data = data
        trajectory = []
        for i in range(len(cells)):
            c = cells[i]
            trajectory.append(actions[i])

            if c >= len(self.min_cell_steps):
                for j in range(c - len(self.min_cell_steps) + 1):
                    self.min_cell_steps.append(i)
                    self.cell_visits.append(0)
                    self.trajectories.append(deepcopy(trajectory))
            elif self.min_cell_steps[c] > i:
                self.min_cell_steps[c] = i
                self.cell_visits[c] = 0
                self.trajectories[c] = deepcopy(trajectory)
        self.num_games += 1
        if PRINT_DATA:
            player_num, steps, t_idx, max_cell, num_games, max_x = game_data
            print('--------------------------')
            print('Player ' + str(player_num))
            print('Total Games Played: ' + str(self.num_games))
            print('Max Cell: ' + str(len(self.min_cell_steps) - 1))
            print('Max X: ' + str(max_x))
            print('Local Games Played: ' + str(num_games))
            print('Start Index: ' + str(t_idx))
            print('Total Steps: ' + str(steps))
            print('Local Max Cell: ' + str(max_cell))

    def get_trajectory(self):
        v_arrary = np.array(self.cell_visits)
        exp = (MAX_EXP - np.arange(len(self.cell_visits))) / MAX_EXP
        num = SCORE_A ** exp
        # num = 1.
        den = np.sqrt(v_arrary + SCORE_E1)
        p = num / den + SCORE_E2
        p = p / np.sum(p)
        idx = np.random.choice(len(self.cell_visits), 1, p = p)[0]
        self.cell_visits[idx] += 1
        return self.trajectories[idx]

    def listen(self):
        i = 0
        while True:
            if self.connections[i].poll():
                cmd, data = self.connections[i].recv()
                if cmd == 'batch':
                    self.update_memory(data)
                elif cmd == 'trajectory':
                    trajectory = self.get_trajectory()
                    self.connections[i].send(trajectory)
            i = (i + 1) % NUM_PLAYERS