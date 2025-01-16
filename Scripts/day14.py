import numpy as np
import re

def import_data(filepath):
    with open(filepath, 'r') as file:
        data = file.readlines()

    def build_robit(line):
        px, py, vx, vy = map(int, re.findall(r'(-?\d+)', line))
        return px, py, vx, vy
    
    data  = [build_robit(line) for line in data]
    return data
    
##  test setup 
# data = import_data("Test_inputs/day14_test.txt")
# WIDTH = 11
# HEIGHT = 7 

# full setup
data = import_data("Inputs/day14_input.txt")
WIDTH = 101
HEIGHT = 103
NUM_ROBITS = len(data)


## Part 1 ## 
"""
Pretty straightforward. Just need to modulus the movements.

Splitting the grid is a little finicky; need to look at some np documentation I guess

Not necessary, but brainblast, I don't think we actually need to iterate these.

TODO: construct a formula that solves this
"""

def grid_rep(data):
    grid = np.zeros(shape=[HEIGHT, WIDTH])
    for px, py, _, _ in data:
        grid[py, px] += 1
    return grid

## move all the robots according to their velocity.
def move_robits(data):
    def move_robit(robit):
        # print(robit)
        px, py, vx, vy= robit
        px = (px + vx) % WIDTH
        py = (py + vy) % HEIGHT
        robit = px, py, vx, vy
        # print(robit)
        return robit
    return [move_robit(robit) for robit in data]

## perform as many moves as we need to
def iterate_moves(data, itt_count):
    # print(grid_rep(data))
    for i in range(itt_count):
        # print(f"\n\niteration {i+1}")
        data = move_robits(data)
        # print(grid_rep(data))
    return data

def score_data(data):
    grid = grid_rep(data)
    split_y, split_x = HEIGHT // 2, WIDTH // 2

    # remove the middles row/col
    grid = np.delete(grid, split_y, axis=0)
    grid = np.delete(grid, split_x, axis=1)

    grids = [
        grid[:split_y, :split_x],  # Top-left
        grid[:split_y, split_x:],  # Top-right
        grid[split_y:, :split_x],  # Bottom-left
        grid[split_y:, split_x:]   # Bottom-right
    ]
    score = np.prod([np.sum(grid) for grid in grids])
    return score

data_100 = iterate_moves(data, 100)
naive_score = score_data(data_100)
print(naive_score)


## Part 2 ## 
"""
Fewest number of seconds before we "make a picture of a christmas tree"

Uhh. I'm probably just going to use my eyes for this one
 (using the grid shower I built for HOT models in POCS)

 I tried this for 1000 frames but it didn't work.

 So instead I'll try looking at frames where a good amount of the robots
 are sharing a space (hoping this implies stucture).
 
 We can do this by checking if a frame has less than say 95% of robots present
 (becuase hte ohters ones are on the same sqaures...?)
 
 I see some stuff but nothing leaps out to me. 
 We do notice it repeats every 11000 frames or so

 We also notice that there are 'colasecing' frames... we
 want only to look at these --where most of the pixels
 are in one general spot... we can look at this by looking 
 for lines that have far more than the avg amount of pixels

"""
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


## animate frames (parsing only potential)
def show_robits(data, num):
    fig, ax = plt.subplots()
    grid = grid_rep(data)
    img = ax.imshow(grid, cmap='gray', vmin=0, vmax=1)
    title = ax.set_title(f"Grid at tree placement 0")
    i = 0

    ## draw a new frame
    def update(frame):
        nonlocal data, i
        data = move_robits(data) 
        grid = grid_rep(data)
        while not potential_frame(grid):
            i += 1
            data = move_robits(data) 
            grid = grid_rep(data)
        else:
            i += 1
            print(i)
            img.set_data(grid)  # update the image by changing its grid data
            title.set_text(f"Grid at tree placement {i}")  
        return img, title

    _ = FuncAnimation(fig, update, frames=num, blit=False, repeat=False)
    plt.show()

## this gives us only 'coalescing' frames.
def check_line(grid):
    counts = [np.count_nonzero(row) for row in grid]
    if max(counts) - 20 > np.mean(counts):
        return True
    else:
        return False

## check conditions to see if a frame meets it. 
def potential_frame(grid):
    grid = np.pad(grid, pad_width=1)
    return check_line(grid)


show_robits(data, 12000)

## go frame by frame to see where it is exactly
# def show_robits(data, num):
#     for i in range(num):
#         print(i)
#         grid = grid_rep(data)
#         if potential_frame(grid):
#             plt.imshow(grid, cmap='gray', vmin=0, vmax=1)
#             plt.title(f"Grid at tree placement {i}")
#             plt.show()
#         data = move_robits(data)