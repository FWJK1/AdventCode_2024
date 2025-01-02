import re
import copy

def read_7file(filepath): 
    with open(filepath, "r") as f:
        eqs = f.readlines()
    for i, eq in enumerate(eqs):
        vals = [int(val) for val in re.findall(r'(\d+)', eq)]
        eq = (vals[0], vals[1:])
        # print(eq) #debug
        eqs[i] = eq
    return eqs

eqs = read_7file("Inputs/day7_input.txt")
test_eqs = read_7file("Test_inputs/day7_test.txt")

def check_eq(goal, val1, vals, ops):
    if val1 > goal:
        # print(f"Too high... goal: {goal}, val1: {val1}")
        return False
    if not vals and val1 == goal: # return true iff final entry
        return ops
    if vals: # recursively try diff operators
        val2, *vals = vals 

        mult = val1 * val2
        add = val1 + val2

        # print(f"goal: {goal}, val1: {val1}, vals: {vals}, val2: {val2}, mult: {mult}, add: {add}, concat: {concat}") # debug
        recursions = [
            check_eq(goal, add, vals, ops + ['+']),
            check_eq(goal, mult, vals, ops + ['*']),
        ]
        return next((result for result in recursions if result), False)
  
    
cum = 0
for eq in copy.deepcopy(eqs): ## need deep copy because lists within a copied list are not copied in python
    # print("--" * 50) # debug
    goal = eq[0]
    val, *vals = eq[1]
    ops = check_eq(goal, val, vals, ops=[])
    if ops:
        ## debug print block ##
        # print(val, end=" ")
        # for i, op in enumerate(ops):
        #     print(f"{op} {vals[i]}", end=" ")
        # print(f"= {goal}")

        cum += goal
print(f"With two operators the answer is {cum}")
#4998764814652



## part two we redefine with a few more lines ## 

## note we could make this one func with if/else for a 'concat' condition but seems unneeded

def check_eq(goal, val1, vals, ops=None):

    if val1 > goal:
        # print(f"Too high... goal: {goal}, val1: {val1}")
        return False
    if not vals and val1 == goal: # return true iff final entry
        return ops
    if vals: # recursively try diff operators
        val2, *vals = vals 

        mult = val1 * val2
        add = val1 + val2
        concat = int(str(val1) + str(val2))

        # print(f"goal: {goal}, val1: {val1}, vals: {vals}, val2: {val2}, mult: {mult}, add: {add}, concat: {concat}") # debug
        recursions = [
            check_eq(goal, add, vals, ops + ['+']),
            check_eq(goal, mult, vals, ops + ['*']),
            check_eq(goal, concat, vals, ops + ['||'])
        ]
        return next((result for result in recursions if result), False) 


cum = 0
for eq in eqs:
    # print("--" * 50) # debug
    goal = eq[0]
    val, *vals = eq[1]
    ops = check_eq(goal, val, vals, ops=[])
    if ops:
        ## debug print block ##
        # print(val, end=" ")
        # for i, op in enumerate(ops):
        #     print(f"{op} {vals[i]}", end=" ")
        # print(f"= {goal}")
        
        cum += goal
print(f"With three operators the answer is {cum}")
#37598910447546
