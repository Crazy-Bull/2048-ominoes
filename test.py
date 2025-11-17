import pickle
from state import int2state, state_sum
import os
from calculate import Expectations, rnd_spawn_int

def unprocessed():
    unprocessed_list = []
    processed_list = []
    for i in range(369):
        path = f"polynominoes/{i}/sum_4.pkl"
        if not os.path.exists(path):
            unprocessed_list.append(i)
            continue
        with open(path, 'rb') as f:
            sum_4 = pickle.load(f)
            for key, val in sum_4.items():
                if len(list(val)) != 5:
                    unprocessed_list.append(i)
                else:
                    processed_list.append(i)

                break

    return unprocessed_list,  processed_list

def start_ev(board_ind):
    # start states
    start22 = set()
    start24 = set()
    start44 = set()
    start2 = rnd_spawn_int(0, 1)
    start4 = rnd_spawn_int(0, 2)
    for x in start2:
        start22.update(rnd_spawn_int(x,1))
        start24.update(rnd_spawn_int(x,2))
    for x in start4:
        start44.update(rnd_spawn_int(x,2))

    with open(f"polynominoes/{board_ind}/sum_4.pkl", 'rb') as f:
        sum_4 = pickle.load(f)
    with open(f"polynominoes/{board_ind}/sum_6.pkl", 'rb') as f:
        sum_6 = pickle.load(f)
    with open(f"polynominoes/{board_ind}/sum_8.pkl", 'rb') as f:
        sum_8 = pickle.load(f)


    contribution22 = 1 / 28 * 0.81
    contribution24 = 1 / 56 * 0.18
    contribution44 = 1 / 28 * 0.01


    ev = Expectations(0,0,0,0,0)
    for state_int in start22:
        ev += Expectations(sum_4[state_int][0], sum_4[state_int][1], sum_4[state_int][2], sum_4[state_int][3], sum_4[state_int][4]) * contribution22
    for state_int in start24:
        ev += Expectations(sum_6[state_int][0], sum_6[state_int][1], sum_6[state_int][2], sum_6[state_int][3], sum_6[state_int][4]) * contribution24
    for state_int in start44:
        ev += Expectations(sum_8[state_int][0], sum_8[state_int][1], sum_8[state_int][2], sum_8[state_int][3], sum_8[state_int][4]) * contribution44
    return ev

if __name__ == "__main__":
    unpprocessed_list, processed_list = unprocessed()
    print("Unprocessed polynominoes:", unpprocessed_list)
    with open('output.csv', 'w', encoding='utf-8') as file:
        file.write('ID,128 rate,256 rate,512 rate, E[score], E[sum]\n')
        for i in processed_list:
            ev_tuple = start_ev(i).to_tuple()
            print(f"Expected value for polynomino {i}:", ev_tuple)
            file.write(f"{i},{ev_tuple[0]},{ev_tuple[1]},{ev_tuple[2]},{ev_tuple[3]},{ev_tuple[4]}\n")
            