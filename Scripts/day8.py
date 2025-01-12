import numpy as np
from itertools import combinations

def day8_data(file):
    data = np.loadtxt(file, dtype=str)
    data = [np.array(list(line), dtype=str) for line in data]
    data = np.array(data)
    # print(data) #debug
    length = data.shape[0]
    return data, length

# data, length = day8_data("Test_inputs/day8_text.txt")
data, length = day8_data("Inputs/day8_input.txt")


## first make a position directory for every node
def add_to_dict(d, key, value):
    d.setdefault(key, []).append(value)

node_dict = {}
for i in range(length):
    for j in range(length):
        element = data[i, j]
        if element != "." :
            add_to_dict(node_dict, element, (i, j))


## now iterate through the node dict and create an anti_node dict
# helper func to ensure pos is in bounds
def check_position(pos):
    return 0 <= pos[0] < length and 0 <= pos[1] < length

## return a list of the (up to 2) positions that two nodes can create
def get_antinode_positions(pos1, pos2):
    # calculate diff and then go back from initial and forward from second
    delta = (pos2[0] - pos1[0], pos2[1] - pos1[1])
    back_scale = tuple(p - d for p, d in zip(pos1, delta))
    up_scale = tuple(p + d for p, d in zip(pos2, delta))

    # print(f"pos1: {pos1}, pos2: {pos2}, delta: {delta}, back_scale: {back_scale}, up_scale: {up_scale}")
    return [val for val in [back_scale, up_scale] if check_position(val)] 

## for part two we all positions in line that fit
def get_all_antinode_positions(pos1, pos2):
        delta = (pos2[0] - pos1[0], pos2[1] - pos1[1])
        candidates = []

        # calc backward from pos1
        (x, y )= pos1
        while check_position((x,y)):
            candidates.append((x,y))
            (x, y) = tuple(p - d for p, d in zip((x, y), delta))

        # calc forward from pos2
        (x, y )= pos2
        while check_position((x,y)):
            candidates.append((x,y))
            (x, y) = tuple(p + d for p, d in zip((x, y), delta))
        return candidates
        


## run logic
anti_nodes, all_anti_nodes = set(), set()
for key, vals in node_dict.items():
    pairs = list(combinations(vals, 2)) ## get every combo (order does not matter) 
    for (pos1, pos2) in pairs:
       anti_nodes.update(get_antinode_positions(pos1, pos2))
       all_anti_nodes.update(get_all_antinode_positions(pos1, pos2))


# debug block to print the datamap again with antinode chars
for node in all_anti_nodes:
    row = node[0]
    col =  node[1]
    pos = data[row, col]
    if pos == '.' : 
        data[row, col] = '#'

for line in data:
    print(''.join(line))

print(f"There are {len(anti_nodes)} anti-node positions, naively.")
print(f"There are {len(all_anti_nodes)} anti-node positions in all.")        