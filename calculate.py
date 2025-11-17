import pickle
import os
from state import int2state, state2int, state_sum, contains_at_least
from tqdm import trange
from move import * 
import numpy as np
from config import *

class Expectations:
    def __init__(self, rate128, rate256, rate512, score, sum):
        self.rate128 = rate128
        self.rate256 = rate256
        self.rate512 = rate512
        self.score = score
        self.sum = sum

    def __add__(self, other):
        if isinstance(other, Expectations):
            return Expectations(self.rate128 + other.rate128, self.rate256 + other.rate256, self.rate512 + other.rate512, self.score + other.score, self.sum + other.sum)
        else:
            return NotImplemented
    
    def __mul__(self, other):
        return Expectations(self.rate128 * other, self.rate256 * other, self.rate512 * other, self.score * other, self.sum * other)
    
    def max(self, other):
        if isinstance(other, Expectations):
            return Expectations(max(self.rate128, other.rate128), max(self.rate256, other.rate256), max(self.rate512, other.rate512), max(self.score, other.score), max(self.sum, other.sum))
        else:
            return NotImplemented
        
    def to_tuple(self):
        return (self.rate128, self.rate256, self.rate512, self.score, self.sum)
        

def rnd_spawn_int(state, num):
    return [state | (num << (4*i)) for i in range(8) if (state >> (4*i)) & 15 == 0]

def contains(state, num):
    for i in range(8):
        if (state >> (4*i)) & 15 >= num:
            return 1
    return 0


        

def bfs(board_ind):
    num_states = 0
    current = set()
    current_p2 = set()
    current_p4 = set()
    current_dict = dict()

    # load move informations for a certain board
    with open(f"polynominoes/{board_ind}/move.pkl", 'rb') as f:
        move_info = pickle.load(f)


    move_funcs = [generate_move_function(chains) for chains in move_info]

    # start states
    start2 = rnd_spawn_int(0, 1)
    start4 = rnd_spawn_int(0, 2)
    for x in start2:
        current.update(rnd_spawn_int(x,1))
        current_p2.update(rnd_spawn_int(x,2))
    for x in start4:
        current_p4.update(rnd_spawn_int(x,2))

    for i in trange(2, 511):
        os.makedirs(f"{TEMP_FOLDER}", exist_ok=True)
        
        num_states += len(current)
        
        for state in current:
            children = []
            for move_func in move_funcs:
                moved_state, score , valid = move_func(state, chain_table)
                if valid:
                    next_state2= rnd_spawn_int(moved_state, 1)
                    current_p2.update(next_state2)
                    next_state4= rnd_spawn_int(moved_state, 2)
                    current_p4.update(next_state4)
                    children.append((next_state2, next_state4, score))
                else:
                    children.append(([],[],0))
            current_dict[state] = children
        
        with open(f"{TEMP_FOLDER}/{i}.pkl", 'wb') as f:
            pickle.dump(current_dict, f)
        
        current = set(current_p2)
        current_p2 = set(current_p4)
        current_p4 = set()
        current_dict = dict()

    return num_states

        


def calc_ev(board_ind):
    current = dict()
    current_p2 = dict()
    current_p4 = dict()

    for i in trange(510, 1, -1):
        with open(f"{TEMP_FOLDER}/{i}.pkl", 'rb') as f:
            current_states = pickle.load(f)
        for state, children in current_states.items():
            # suppose it is a dead state, if not, moving increases the statistics
            ev = Expectations(contains(state,7), contains(state,8), contains(state, 9), 0, 2 * i)
            # search for each direction
            for child_states2, child_states4, apd_score in children:
                l = len(child_states2)
                if l != 0:
                    contribution = 1.0 / l

                    # 2 spawn
                    ev2 = Expectations(0, 0, 0, apd_score, 0)
                    for next_state in child_states2:
                        ev2 = ev2 + current_p2[next_state] * contribution

                    # 4 spawn
                    ev4 = Expectations(0, 0, 0, apd_score, 0)
                    for next_state in child_states4:
                        ev4 = ev4 + current_p4[next_state] * contribution
                    
                    ev = ev.max(ev2 * (1-P) + ev4 * P)


            current[state] = ev

        if i in [2, 3, 4]:
            current_info = dict([(key, item.to_tuple()) for key, item in current.items()])
            # breakpoint()
            with open(f"polynominoes/{board_ind}/sum_{2*i}.pkl", 'wb') as f:
                pickle.dump(current_info, f)


        current_p4 = dict(current_p2)
        current_p2 = dict(current)
        current = dict()
        
        


import cProfile
import pstats

if __name__ == "__main__":
    init_tables()
    if USE_CPROFILE:
        with cProfile.Profile() as pr:
            for i in workflow:
                print(f"Calculating polynomino {i}")
                bfs(i)
                calc_ev(i)

        p = pstats.Stats(pr)
        p.strip_dirs().sort_stats('cumulative').print_stats(10)
    # breakpoint()

    else:
        for i in workflow:
            print(f"Calculating polynomino {i}")
            bfs(i)
            calc_ev(i)
            