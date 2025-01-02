import numpy as np
import pandas as pd


## Read in file and parse to a 2d array
with open("Inputs/day6_input.txt", 'r') as f:
    map = f.readlines()

map = [line.replace('\n', '' ) for line in map]
# for i, line in enumerate(map): print(i, line)  ## dbug to see map if needed
map = [np.array(list(line), dtype=str) for line in map]
map = np.array(map)




## dictionary for turning
turn_dict = {
    (1, 0) : (0, -1), ##  down to left
    (0, -1) : (-1, 0), ## left to up
    (-1, 0) : (0, 1), ## up to right
    (0, 1) : (1, 0) ## right to down
}

## calculate the next move, turning right if you have to.
## if the move takes you out of bounds, return false
## for ease we return the row, col, and direction
def make_move(row, col, d, map):
    nu_row = row + d[0]
    nu_col = col + d[1]
    if nu_row < 0 or nu_row >= length or nu_col < 0 or nu_col >= length:
        return (False, False, False)
    else:
        next = map[nu_row, nu_col]
        if next == '#': 
            # print(f"HIT OBSTACLE AT {nu_row, nu_col}, TURNING from {d} to {right_turn(d)}")
            return make_move(row, col, turn_dict.get(d), map)
        else:
            return  (nu_row, nu_col, d)
        

## init global vars
length = map.shape[0]
row, col = np.where(map == '^')
row, col = row[0], col[0]
frow, fcol = row, col ## store this now for part 2
d = (-1, 0) ## initial direction is up

positions = set()
while row and col:
    positions.add((row, col))
    # print(f"Visited position: {(row, col)}")  # Debug
    row, col, d= make_move(row, col, d, map)
positions.add((row, col)) ## add the final position

print(f"Naive solution = {len(positions)}") ## answer: 5030



"""for part two, we need to find all the spots that can create a loop. 
we can just iterate through all the positions we calc'd naively.
if the guard ever hits the same run position/direction again,
then we know they are looping and can count that position as a candidate.

Note: if we were doing this for production level type code, we could improve performance by pre-checking
all the block positions to see if there is a turn somewhere in their future. If there isn't, then we dont
have to check them. We could even do two (more accurate check, slightly lower performance).
we could even make a pretty sophisticated algo to estimate how many turns we should check ahead.
but this way is fast enough for this (about 5 seconds).  """


def is_loop_pos(row, col, position):
    run_map = map.copy()
    run_map[position] = '#'
    run_pos = set()
    d = (-1, 0) ## initial direction is up
    while row and col:
        row, col, d = make_move(row, col, d, map=run_map)
        pos = (row, col, d)
        if pos in run_pos:
            return 1
        else:
            run_pos.add(pos)
    return 0


## simple loop solution
cum = 0
for position in positions:
    cum += is_loop_pos(frow, fcol, position)

print(f"The number of potential looping spots is {cum}") 
## answer: 1928


## checking to see if vectorizing this improves performance much
# cum = 0
# # start at same start 
# df = pd.DataFrame(positions, columns=['row', 'col'])

# df['loop'] = df.apply(lambda position: is_loop_pos(frow, fcol, (position['row'], position['col'])), axis=1)
# print(df['loop'].sum())

    
    