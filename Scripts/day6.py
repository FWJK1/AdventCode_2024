import numpy as np


## Read in file and parse to numbers
with open("Inputs/day6_input.txt", 'r') as f:
    map = f.readlines()

map = [line.replace('\n', '' ) for line in map]
for i, line in enumerate(map): print(i, line)

chars = {
    '.' : 0,
    '#' : 1,
    '^' : 5
}

for i, string in enumerate(map):
    string = np.array(list(string), dtype=str)
    transformed_arr = [chars.get(char) for char in string]
    map[i] = transformed_arr
map = np.array(map)




## dictionary for turning
turn_dict = {
    (1, 0) : (0, -1), ##  down to left
    (0, -1) : (-1, 0), ## left to up
    (-1, 0) : (0, 1), ## up to right
    (0, 1) : (1, 0) ## right to down
}
def right_turn(direction):
    return turn_dict.get(direction)


## calculate the next move, turning right if you have to.
## if the move takes you out of bounds, return false
def make_move(row, col, d):
    nu_row = row + d[0]
    nu_col = col + d[1]
    if nu_row < 0 or nu_row > length or nu_col < 0 or nu_col > length:
        return (False, False)
    else:
        path = map[nu_row, nu_col]
        if path == 1: 
            # print(f"HIT OBSTACLE AT {nu_row, nu_col}, TURNING from {d} to {right_turn(d)}")
            return make_move(row, col, right_turn(d))
        else:
            return  (nu_row, nu_col, d)
        

## init global vars
length = map.shape[0]
row, col = np.where(map == 5)
row, col = row[0], col[0]
d = (-1, 0) ## initial direction is up

positions = set()
while row and col:
    positions.add((row, col))
    # print(f"Visited position: {(row, col)}")  # Debug
    row, col, d= make_move(row, col, d)
positions.add((row, col)) ## add the final position

print(f"Naive solution = {len(positions)}") ## 5030





