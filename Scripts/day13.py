
import re

def find_x_y(line):
    X = int(re.search(r'X.(\d+)', line).groups()[0])
    Y = int(re.search(r'Y.(\d+)', line).groups()[0])
    return (X, Y)

def day13_data(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    data_map = {'A': [], 'B': [], 'Prize': []}

    for line in lines:
        for key in data_map:
            if key in line:
                data_map[key].append(find_x_y(line))
                break

    data = [{ 'A': data_map['A'][i], 'B': data_map['B'][i], 'P': data_map['Prize'][i] } for i in range(len(data_map['Prize']))]
    
    # print(data)
    return data
            
# data = day13_data("Test_inputs/day13_test.txt")
data = day13_data("Inputs/day13_input.txt")


## part 1 -- left for posterity but part 2 code does it better ##
"""
Pretty simple, we can just brute force through the whole thing easily by testing them 
all.
"""
def brute_force(machine):
    Ax, Ay = machine['A']
    Bx, By = machine['B']
    Px, Py = machine['P']
    best = 1000
    print("--" * 50)
    print(f"Testing {machine}")
    for i in range(101):
        for j in range(101):
            val_x = Ax*i + Bx*j
            val_y = Ay*i + By*j
            if (val_x, val_y) == (Px, Py):
                score = 3*i + j
                best = min(best, score)
                print(f"Score at {i, j}: valx={val_x}, valy={val_x}, so new best = {best}")
    if best == 1000:
        print("no prize")
        return False
    else:
        print(f"final answer: {best}")
        return best

## part 2: add 10000000000000 to px and py for every prize  # 
"""
Not sure yet... thinking it'll be something to do with % or //  ?

No! It's just a system of equations, duh. So we can solve it with linear algebra. 

Ax = b    =>     x = inv(A)*b
And we can get the inverse of A by multiplying 1/det(A) * the 'flipped' matrix
"""

## helper function to make sure we don't miss values with floats
def is_almost_int(value, tolerance=1e-3):
    return abs(value - round(value)) < tolerance

def get_thresholds(machine, plus_val=0):
    # print("--" * 50)
    # print(f"Testing {machine}")
    ax, ay = machine['A']
    bx, by = machine['B']
    px, py = machine['P']
    px, py = px + plus_val, py + plus_val

    # print(f"ax: {ax}, ay: {ay}, bx: {bx}, by: {by}, px: {px}, py: {py}")

    determinant = ax*by - bx*ay
    if not determinant: ## there is no inverse
        return False
    else:
        scaler = 1/determinant
        # print(f"determinant: {determinant}, scaler: {scaler}")
        button_one =  scaler * (by*px - bx*py)
        button_two = scaler * (-ay*px + ax*py)
        # print(button_one, button_two) 
        
    ## this is good but occasionally the floats aren't precise enough so we round up for things that are almost ints
    if is_almost_int(button_one) and is_almost_int(button_two):
                # print('score')
                return round(button_one)*3 + round(button_two)
    else:
        # print("False")
        return False
                                                                   
naive_score, score = 0, 0                                                                 
for machine in data:
    naive_score += get_thresholds(machine)
    score += get_thresholds(machine, 10000000000000)

print(f"The naive score is {naive_score}")
print(f"The actual score is {score}")