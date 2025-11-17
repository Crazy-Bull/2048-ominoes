from tqdm import trange
import os
import pickle

def state2int(state, mod = 16):
    hash = 0
    mult = 1
    for i in range(len(state)):
        hash += state[i] * mult
        mult *= mod
    return hash

def int2state(hash, n = 8, mod = 16):
    state = []
    for _ in range(n):
        state.append(hash % mod)
        hash //= mod
    return state

def state_sum(state):
    sum = 0
    for i in state:
        if i != 0:
            sum += (1 << i)
    return sum


def is_valid_state(state):
    sorted_state = sorted(state)
    has_2_or_4 = False
    for i in range(len(sorted_state)):
        if sorted_state[i] > i + 2:
            return False
        if sorted_state[i] in [1, 2]:
            has_2_or_4 = True
    return has_2_or_4

def contains_at_least(state, k):
    sorted_state = sorted(state)
    return sorted_state[-1] >= k


def main():
    # generate all states and categorize them according to their sum
    valid_states = [[] for _ in range(511)]
    
    print("Calculating")
    for i in trange(100000000):
        state = int2state(i, mod=10)
        if is_valid_state(state):
            valid_states[state_sum(state)//2].append(state2int(state))

    print("Saving")
    os.makedirs("states", exist_ok=True)
    for i in trange(len(valid_states)):
        with open(f"states/{i}.pkl", 'wb') as f:
            pickle.dump(valid_states[i], f)
    
if __name__ == "__main__":
    main()
