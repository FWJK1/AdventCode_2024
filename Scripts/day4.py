import numpy as np

## load in the data as a array of strings
data = np.loadtxt("Inputs/day4_input.txt", dtype=str)
nu_data = []
chars = {
    'X' : 0,
    'M' : 1,
    'A' : 2,
    'S' : 3
}

## test readable data
# rows, cols = 10, 10
# data = np.random.choice(list(chars.keys()), size=(rows, cols))
# print(data)

## convert to array of arrays of numbers for easier sequencing
for string in data:
    string = np.array(list(string), dtype=str)
    transformed_arr = []
    for char in string:
        transformed_arr.append(chars.get(char, char)) 
    nu_data.append(transformed_arr)
nu_data = np.array(nu_data)

## check along a direction to see if the xmas sequence is filled
def check_xmas(x, y, d, val, length):
    # check we're in valid bounds
    nu_x = x + d[0]
    nu_y = y + d[1]
    if nu_x < 0 or nu_x >= length or nu_y < 0 or nu_y >= length:
        return False
    
    # see if sequence is being fulfilled
    check_val = nu_data[nu_y, nu_x] 
    if check_val == val + 1: 
        if check_val == 3:
            return True
        else:
            return check_xmas(nu_x, nu_y, d, check_val, length)
    else:
        return False

## Wrapper to check in all 8 possible directions:
def eight_search(x, y, length):
    results = []
    directions =  [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),  (0, 1),
        (1, -1), (1, 0), (1, 1) 
        ]
    # run checks if initial val is good
    val = nu_data[y, x]
    if val == 0:
        for direction in directions:
            if check_xmas(x, y, direction, 0, length):
                results.append(direction) # accum this way for easier debugging
        return len(results)
    else:
        return 0

## function to check for MAS cross sequence (for second solution)
def check_mas(x, y, length):
        if x-1 < 0 or x+1 >= length or y-1 < 0 or y+1 >= length:
            return False
        elif nu_data[y, x]  != 2:
            return False
        else:        
            mas_counter = 0

            topleft = nu_data[y-1, x-1]
            botleft = nu_data[y+1, x-1]
            topright = nu_data[y-1, x+1]
            botright = nu_data[y+1, x+1]
 
            if (topleft == 1 and botright == 3) or (topleft == 3 and botright == 1):
                mas_counter += 1
            if (botleft ==1 and topright == 3) or (botleft == 3 and topright ==1):
                mas_counter +=1
            return True if mas_counter == 2 else False

## loop, calc, report
real_sol, naive_sol = 0, 0 
for y in range(len(nu_data)): 
    for x in range(len(nu_data[y])): 
        naive_sol += eight_search(x, y, nu_data.shape[0])
        real_sol += check_mas(x, y, nu_data.shape[0])

print(f"The naive solution is {naive_sol}")
print(f"The actual solution is {real_sol}")
