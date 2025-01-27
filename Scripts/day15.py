import numpy as np
from  itertools import chain
np.set_printoptions(linewidth=200) ## lets us print wider to see the grid without wrapping lines

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
# grid, commands = import_data("Test_inputs/day15_part2_test.txt")

MOVE_DICT ={
    '^' : (-1, 0),
    'v'  : (1, 0),
    '<' : (0, -1),
    '>' : (0, 1)
}

def move_pos(pos, d):
    return tuple(p + d for p,d in zip(pos, d))

def print_grid(grid):
    for row in grid:
        print(''.join(row))

## Part 1 ## 
"""
Pretty simple -- just need to recursively update the grid as we try to move.
"""
def make_move(object, pos, direction, grid):
    nu_pos = move_pos(pos, direction)
    nu_obj = grid[nu_pos]
    nu_obj = nu_obj.item()

    if nu_obj == '.': 
        grid[nu_pos] = object
        grid[pos] = '.'
        return "moved"
    
    elif nu_obj in "O, [, ]":  ## recurse through new positions
       if make_move(nu_obj, nu_pos, direction, grid) == "moved":
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
        old_grid = np.copy(grid)
        robot = np.where(grid == '@')
        phrase = double_grid_move('@', robot, MOVE_DICT.get(move), grid)
        if phrase == 'not_moved':
            grid = old_grid
        # print(f"{i+1}: {move} gives {phrase} \n") 
        # print_grid(grid)# debug
    return grid
              
def score_grid(grid):
    positions = np.where((grid == 'O') | (grid == '[') )
    ## this returns a tuple of x_array and y_array indicies so we have to rejoin them
    positions = [tuple(arr[i] for arr in positions) for i in range(len(positions[0]))]
    return np.sum(np.fromiter((pos[0]*100 + pos[1] for pos in positions), dtype='int'))
    
## part 2 ## 
"""
Also pretty easy -- just need to keep track of the double position if 
we are going up and down
"""
# If the tile is #, the new map contains ## instead.
# If the tile is O, the new map contains [] instead.
# If the tile is ., the new map contains .. instead.
# If the tile is @, the new map contains @. instead.



## double the grid 
def grid_doubler(grid):
    rows, cols= grid.shape
    nu_grid = np.zeros((rows, cols*2), dtype='str')

    doubler_dict = {
    '#' :  ('#', '#'),
    'O' : ('[', ']'),
    '.' : ('.', '.'),
    '@' : ('@', '.')     
    }
    
    for row in range(rows):
        for col in range(cols):
            object = grid[row, col]
            val1, val2 = doubler_dict.get(object)
            nu_grid[row, (col*2)] = val1
            nu_grid[row, (col*2) + 1] = val2
    return nu_grid


def double_grid_move(object, pos, direction, grid):
    grid_copy = np.copy(grid)
    nu_pos = move_pos(pos, direction)
    nu_obj = grid[nu_pos]

    if direction == (-1, 0) or direction == (1, 0):
        ## we only need to worry about double boxes for up/down
        if nu_obj == '[':
            other_pos = move_pos(nu_pos, (0, 1))
            other_obj = grid[other_pos]
            if other_obj != ']':
                 raise Exception(f"Showing {other_obj} instead of ]")
            else:
                if double_grid_move(nu_obj, nu_pos, direction, grid) == 'moved' \
                    and double_grid_move(other_obj, other_pos, direction, grid) == 'moved':
                     grid[nu_pos] = object
                     grid[pos] = '.'
                     grid[other_pos] = '.'
                     return "moved"
                else:
                    grid = grid_copy
                    return 'not_moved'
        elif nu_obj == ']':
             other_pos = move_pos(nu_pos, (0, -1))
             other_obj = grid[other_pos]
             if other_obj != '[':
                 raise Exception(f"Showing {other_obj} instead of [")
             else:
                 if double_grid_move(nu_obj, nu_pos, direction, grid) == 'moved' \
                    and double_grid_move(other_obj, other_pos, direction, grid) == 'moved':
                     grid[nu_pos] = object
                     grid[pos] = '.'
                     grid[other_pos] = '.'
                     return 'moved'
                 else:
                     grid = grid_copy
                     return 'not_moved'
        else:
            return make_move(object, pos, direction, grid)
    else:
        return make_move(object, pos, direction, grid)

grid = grid_doubler(grid)
grid = iterate_moves(grid, len(commands))
naive_score = score_grid(grid)
print(f"naive score = {naive_score}")