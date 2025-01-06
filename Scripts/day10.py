import numpy as np

## first parse data into 2d np array
def day8_data(file):
    data = np.loadtxt(file, dtype=str)
    data = [np.array(list(line), dtype=int) for line in data]
    data = np.array(data)

    length = data.shape[0]
    return data, length

# data, length = day8_data("Test_inputs/day10_test.txt")
data, length = day8_data("Inputs/day10_input.txt")



""""
Part 1: We can just do a recursive search starting from every point.

At first I tried a better optimized way -- to keep track of whether every position worked or not 
in a depth first search. But this can fail because some positions have MULTIPLE correct nines associated with them. I'm sure there's a way to make thatt work properly but the grids are small enough it runs instantly anyway.
"""

# helper func to ensure pos is in bounds
def check_bounds(pos):
    return 0 <= pos[0] < length and 0 <= pos[1] < length

## helper func to add a direction to a tuple
def new_pos(pos, d):
    return tuple(p + d for p,d in zip(pos, d))

direction_dict = {
    'up' : (-1, 0),
    'right' : (0, 1),
    'down' : (1, 0),
    'left' : (0, -1)
}

## we return a set of the ones that are in bounds so that we don't have to worry about duplicates ## 
def check_connected(pos, goal, direction_dict=direction_dict):
    if data[pos] == 9: ## we reached the goal and can return the position (as a set)
        return {pos}
    else:

        ## build and check a list of candidates
        candidates = []
        for _ , d in direction_dict.items():
            candidate = new_pos(pos, d)
            if check_bounds(candidate) and data[candidate] == goal:
                # print(f"Candidate {candidate} has val {data[candidate]}")
                candidates.append(candidate)

        ## if we have any candidates, recursively perform search on them, updating to a result set
        ## luckily, set.update puts the content in, not the second set itself, so it all hashes nicely
        if candidates:
            result_set = set()
            for candidate in candidates:
                result_set.update(check_connected(candidate, goal + 1, direction_dict))
            return result_set
        else:
            return set()

def build_tree(pos):
    # print("--" * 50)
    if  data[pos] != 0:
        # print(f"data{pos} = {data[pos]} != 0")
        return 0
    else:
        # print(f"data{pos} = {data[pos]} == 0: STARTING")
        # print(data)
        return len(set(check_connected(pos, 1)))
    
 ## switching to one liners for counting
count = sum(build_tree((i, j)) for i in range(length) for j in range(length))
print(f"The naive answer is {count}")



### Part  2 -- a very easy change as this was my original implementation ###
def check_connected(pos, goal, direction_dict=direction_dict):
    if data[pos] == 9: ## we reached the goal and can return the position
        return True
    else:
        candidates = []
        for _ , d in direction_dict.items():
            candidate = new_pos(pos, d)
            if check_bounds(candidate) and data[candidate] == goal:
                # print(f"Candidate {candidate} has val {data[candidate]}")
                candidates.append(candidate)
        return sum(
            [check_connected(candidate, goal+1) for candidate in candidates]
        )


def build_tree(pos):
    if  data[pos] != 0:
        return 0
    else:
        return check_connected(pos, 1)
    

 ## better way to do the counting
count = sum(
    build_tree((i, j)) for i in range(length) for j in range(length))
print(f"The final answer is {count}")



##### Posterity scratch work for a DFS I gave up on becuase not necessary and fiddly ###### 


# """"
# Part 1: DFS
# """
# def check_connected(pos, goal):
#     pass


# def DFS_check_connected(pos, no_go, yes_go, direction_dict=direction_dict, data=data):
#     print("--" * 50)
#     print(data)
#     print(f"Checking pos {pos}")
#     stack = [(0, pos)]
#     chain = []
#     visited_this_run = np.zeros_like(data, dtype=bool)
#     run_count = 0

#     while stack:
#         goal, pos = stack.pop()
#         print(goal, pos, data[pos])

#         if visited_this_run[pos]:
#             continue
#         visited_this_run[pos] = True

#         if no_go[pos]:
#             continue
#         if yes_go[pos]:
#             run_count += 1
#             continue



#         if goal == 9 and data[pos] == 9:
#             chain.append((pos, 9))
#             print(chain)
#             print("score!")
#             for (pos,_) in chain:
#                 yes_go[pos] = True
#             run_count += 1
        
#         elif data[pos] == goal:
#             candidates = []
#             for _, d in direction_dict.items():
#                 val = new_pos(pos, d)
#                 if check_bounds(val) and data[val] == goal+1:
#                     candidates.append(val)
#             if candidates:
#                 chain.append((pos, data[pos]))
#                 for candidate in candidates:
#                     stack.append((goal+1, candidate))
#             else:
#                 chain.pop()


#     print(f"run count for {pos} is {run_count}")
#     return run_count


# def DFS_main(file):
#     data, length = day8_data(file)

#     count = 0
#     length = data.shape[0]
#     no_go = np.zeros_like(data, dtype=bool)
#     yes_go = np.zeros_like(data, dtype=bool)

#     for i in range(length):
#         for j in range(length):
#             pos = (i, j)
#             if data[pos] == 0:
#                 count += DFS_check_connected(pos, no_go, yes_go)
#                 print(count)
#     print(count)


# DFS_main("Inputs/day10_input.txt")