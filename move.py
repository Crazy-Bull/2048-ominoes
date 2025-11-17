import pickle
from state import state2int, int2state
from chain_table import move_on_chain
max_table_len = 6
chain_table = [None for i in range(1+max_table_len)]

def init_tables():
    for l in range(1, 1+max_table_len):
        with open(f"chains/table{l}_int.pkl", 'rb') as f:
            chain_table[l] = pickle.load(f)

def move(state, chains):
    new_state = list(state)
    score = 0
    for chain in chains:
        l = len(chain)
        chain_state = [state[i] for i in chain]
        if l > max_table_len:
            new_chain_state, apd_score, _ = move_on_chain(chain_state, chain)

        else:
            new_chain_state, apd_score, _ = chain_table[l][tuple(chain_state)]
        for i in range(l):
            new_state[chain[i]] = new_chain_state[i]
        score += apd_score

    return new_state, score, new_state != state

def generate_move_function(chains):
    str = 'def move(x, table):\n ret=0 \n sum_score=0 \n total_moved=False\n '
    for chain in chains:
        str += "y="
        counter = 0
        for i in chain:
            str += f"(((x>>{4*i})&15)<<{4*counter})|"
            counter += 1
        str += "0\n "
        str += f"z, score, moved = table[{len(chain)}][y]\n ret |= ("
        counter = 0
        for i in chain:
            str += f"(((z>>{4*counter})&15)<<{4*i})|"
            counter += 1
        str += "0)\n sum_score += score \n total_moved = total_moved or moved \n "
    str += "return ret, sum_score, total_moved"
    compiled_code = compile(str, '<string>', 'exec')

    global_namespace = {}
    exec(compiled_code, global_namespace)

    func = global_namespace['move']
    # print(str)
    return func


def rnd_spawn(state, num):
    zero_ind = [i for i, value in enumerate(state) if value == 0]
    return [state[:i] + [num] + state[i+1:] for i in zero_ind]

def step(state, move_info):
    ret = []
    for chains in move_info:
        new_state, score, valid = move(state, chains)
        if valid:
            ret.append((new_state, score))

    return ret

def test():
    #test
    init_tables()
    state = [1,0,1,2,2,1,2,3,0,4,4,4,6,7,8,9]
    chain = [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]]
    #print(move(state,chain))
    # print(rnd_spawn(state,2))
    move_L = generate_move_function(chain)
    int_state = state2int(state)
    print(int2state(move_L(int_state, chain_table)[0], n=16))


if __name__ == "__main__":
    test()