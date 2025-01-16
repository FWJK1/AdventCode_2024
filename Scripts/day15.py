import numpy as np
from  itertools import chain


def import_data(filepath):
    with open(filepath, 'r') as file:
        data = file.readlines()

    grid = [line[:-1] for line in data if '#' in line or '.' in line] # strip the last char off the grid lines
    grid = np.array([np.array(list(line), dtype=str) for line in grid])

    commands = [line for line in data if '<' in line or '>' in line]
    commands = [[char for char in line if char != '\n'] for line in commands] # take out any new lines
    commands = list(chain.from_iterable(commands))
    return grid, commands

# grid, commands = import_data("Test_inputs/day15_test.txt")
# grid, commands = import_data("Test_inputs/mini_day15_test.txt")
grid, commands = import_data("Inputs/day15_input.txt")

MOVE_DICT ={
    '^' : (-1, 0),
    'v'  : (1, 0),
    '<' : (0, -1),
    '>' : (0, 1)
}

def move_pos(pos, d):
    return tuple(p + d for p,d in zip(pos, d))


## Part 1 ## 
"""
Pretty simple -- just need to recursively update the grid as we try to move.
"""

def make_move(object, pos, direction, grid):
    nu_pos = move_pos(pos, direction)
    nu_obj = grid[nu_pos]

    if nu_obj == '.' :
        grid[nu_pos] = object
        grid[pos] = '.'
        return "moved"
    
    elif nu_obj == 'O' : ## recurse through new positions
       if make_move('O', nu_pos, direction, grid) == "moved":
            grid[nu_pos] = object
            grid[pos] = '.'
            return "moved"
       else:
           return "not_moved"
    else:
        return "not moved"

def iterate_moves(grid, num_moves):
    # print(grid, '\n\n')
    for i in range(num_moves):
        move = commands[i]
        robot = np.where(grid == '@')
        phrase = make_move('@', robot, MOVE_DICT.get(move), grid)
        # print(f"{i+1}: {move} gives {phrase} \n {grid}") # debug
    return grid
              
def score_grid(grid):
    positions  = np.where(grid=='O') ## this returns a tuple of x_array and y_array indicies so we have to rejoin them
    positions = [tuple(arr[i] for arr in positions) for i in range(len(positions[0]))]
    return np.sum(pos[0]*100 + pos[1] for pos in positions)
    
iterate_moves(grid, len(commands))
naive_score = score_grid(grid)
print(f"naive score = {naive_score}")