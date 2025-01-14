import numpy as np
import pandas as pd
from collections import defaultdict
from itertools import product


def day12_data(file):
    data = np.loadtxt(file, dtype=str)
    data = [np.array(list(line), dtype=str) for line in data]
    data = np.array(data)
    
    ## rather than make a fake 'fence' grid (my earlier solution), we can just pad the array
    #  with space for  perimeter.
    data = np.pad(data, pad_width=1, mode='constant', constant_values= '.')
    length = data.shape[0]
    print(data) # debug
    return data, length

data, length = day12_data("Inputs/day12_input.txt")
# data, length = day12_data("Test_inputs/day12_test.txt")

## Part 1 ##
"""
We do a depth-first search to build all our different sections.
"""
# helper func to ensure pos is in bounds
def check_bounds(pos, length):
    return 0 <= pos[0] < length and 0 <= pos[1] < length

## helper func to add a direction to a tuple
def move_pos(pos, d):
    return tuple(p + d for p,d in zip(pos, d))

direction_dict = {
    'up' : (-1, 0),
    'right' : (0, 1),
    'down' : (1, 0),
    'left' : (0, -1)
}
## Part 2 ## 
""""
This one is tricky until we see that 'sides' = corners, if we define corners properly.
"""

## find out how many corners=sides a list of positions (contiguous plant area) has 
######  eg ## 
#AAA#
#ABA#
#AAA#
###### has 8 corners and 8 sides.  four exterior (obvious) and four interior (the corners AROUND B)
## This is as far as I can figure always right and certainly gives the right answer
def count_corners(positions, plant):
    num_corners = 0
    for row, col in positions:
        for row_offset, col_offset in product([1, -1], repeat=2): ## this generates all the offsets: 1,1; 1-1; -1,1; -1,-1
            row_neighbor = (row + row_offset, col)
            col_neighbor = (row, col + col_offset)
            diagonal_neighbor = (row + row_offset, col + col_offset)

              # exterior corners have a row and cold neighbor that are both not in the area 
            if (
                data[row_neighbor] != plant  # right or left 
                and data[col_neighbor] != plant # top or bot
            ): 
                num_corners += 1

            # interior corners are weirder. its when there is a non-plant 'within' the area so to speak. 
            # the diagonal corner is off while the others must be on
            if (
                data[row_neighbor] == plant
                and data[col_neighbor] == plant
                and data[diagonal_neighbor] != plant
            ):
                num_corners += 1
    return num_corners

def dfs(data, visited, pos):
    stack = [pos]
    plant = data[pos]
    positions = []
    perim = 0

    while stack:
        pos = stack.pop()
        if data[pos] == '.':
            visited[pos] = True 
        if visited[pos]:
            continue
       
        visited[pos] = True
        positions.append(pos)

        # Check all four possible directions
        for d in direction_dict.values():
            new_pos = move_pos(pos, d)
            if check_bounds(new_pos, length):
                if data[new_pos] != plant:
                    perim += 1
                else: stack.append(new_pos)

    size = len(positions)
    count = size*perim
    edges = count_corners(positions, plant)
    edge_score = size*edges
    if size:
        ## debug print block ## 
        # print("--" * 50)
        # print(f"{plant} has {size} positions with perimeter {perim}. \n\tScore = {count}")
        # print(f"{plant} has {size} positions with edges {edges}. \n\tScore = {edge_score}")
        # print(positions)
        pass
    return positions, count, edge_score

visited = np.zeros_like(data)
perim_count = 0
edge_count = 0
for i in range(length):
    for j in range(length):
        positions, perimeter, edges = dfs(data, visited, (i,j))
        perim_count += perimeter
        edge_count += edges

print("\n\n")
print(f"The perimeter score = {perim_count}, the edge score = {edge_count}")
print(data)

#### bad code for posterity ###


## convert a position on the standard grid to a fence position, which is 2 * (length+1) sized
def convert_pos(pos):
    x, y = pos
    x = x*2 + 1
    y = y*2 + 1
    return (x,y)


## older way of calculating this 
## update all the fence positions. 
def update_fence_posts(pos, fence):
    val = data[pos]
    post = convert_pos(pos)
    fence[post] = val.lower()
    posts = []
    for direction in direction_dict.values():
        candidate = move_pos(post, direction)
        old = fence[candidate]
        if old == val:
            fence[candidate] = ''
        else:
            posts.append(candidate)
            fence[candidate] = val
    return post
