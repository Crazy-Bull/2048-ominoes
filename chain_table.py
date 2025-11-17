from math import floor
import os
import pickle
from state import int2state,state2int

def move_on_chain(chain_state, chain_len):
    score = 0
    prev = -1
    new_chain_state = []
    for i in range(chain_len):
        if chain_state[i] == 0:
            continue
        elif chain_state[i] == prev:
            new_chain_state.append(chain_state[i]+1)
            score += (1 << (chain_state[i]+1))
            prev = -1
        else:
            if prev != -1:
                new_chain_state.append(prev)
            prev = chain_state[i]
    if prev != -1:
        new_chain_state.append(prev)

    for _ in range(chain_len-len(new_chain_state)):
        new_chain_state.append(0)

    return new_chain_state, score, new_chain_state != chain_state

def main():
    os.makedirs("states", exist_ok=True)
    for chain_len in range(1,7):
        result = dict()
        for state_int in range(floor(pow(10,chain_len)+0.5)):
            state = int2state(state_int, mod = 10, n = chain_len)
            tmp = move_on_chain(state, chain_len)
            result[state2int(state)] = (state2int(tmp[0]), tmp[1], tmp[2])
    
        with open(f"chains/table{chain_len}_int.pkl", 'wb') as f:
            pickle.dump(result, f)

if __name__ == "__main__":
    # main()
    print(move_on_chain([7,4,1,1], 4))

