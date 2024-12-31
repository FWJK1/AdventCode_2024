import re
import itertools
import pandas as pd
from functools import cmp_to_key

## read the file and parse into ordering rules and updates
ordering = []
updates = []
with open("Inputs/day5_input.txt", "r") as file:
    for line in file:
        if "|" in line:  # if an ordering rule, convert to digits and store as a tuple
            res = re.search(r'(\d+)\|(\d+)', line).groups()
            ordering.append((int(res[0]), int(res[1])))
        else: # else make a list of all the digits in the entry
            res = re.findall(r'(\d+)', line)
            res = [int(x) for x in res]
            updates.append(res)
updates = updates[1:] # the first update is the line between the orders and updates so we drop it

# convert orders to dataframe for easier cross-checking
orders = pd.DataFrame(ordering, columns = ['Start', 'End'])


## Main Idea
"""
One way to do this would be to conglomerate all the "after" and "before" rules for each number.
Then we would iterate across the update, checking that the before and after are good for every number.

But this is kind of a silly way to do that, as we have to iterate across the list twice for every entry.

Instead, we can iterate across the list once and record in a dictionary the position of each number.
Then we can check the rules by referring to that. So that to check "52 must be less than 71", 
we can quickly get 52->0 and 71->3; therefore it's good. Really we just need the subtraction (end - first > 0). 

Ideally, we don't check ALL the rules, but only those that apply. To do so, we build a list of all the permutations
of all the numbers and then take only the perms that are actual rules. To easily compare the two, merge w pandas.

Once we have this frame, we check that the (end - first > 0) orde listed in the frame r is valued in the position dict
We can store this in a new column of the dataframe to make calculating it vectorized.
"""

# helper func to check if the rule in a row is respected in the position dictionary. 
def is_respected(row, pos_dict):
    pos_start = pos_dict[row['Start']]
    pos_end = pos_dict[ row['End']]
    return pos_end - pos_start > 0



# Helper func to reduce permutations to those that are actual orders
def get_actual_orders(update):
    possible_orders = list(itertools.permutations(update, 2))
    possible_orders = pd.DataFrame(possible_orders, columns = ['Start', 'End'])
    actual_orders = pd.merge(
        left=orders,
        right=possible_orders,
        on=['Start', 'End'],
        how='inner'
    )
    return actual_orders



# checks if the update follows the constraints or not checks once for good updates and then
# every swap for bad
def is_valid_order(constraints, pos_dict):
    actual_orders = constraints.copy()
    # create a position dictionary
    
    # run the logic and return
    actual_orders['respected'] = actual_orders.apply(
       lambda row: is_respected(row, pos_dict), axis=1
    )
    return actual_orders['respected'].all()


## check to see whether a given update follows the rules
def good_update(update):
    actual_orders = get_actual_orders(update)
    pos_dict = {}
    for i, num in enumerate(update):
        pos_dict[num] = i
    return(is_valid_order(actual_orders, pos_dict))

good_update(updates[0])


""""
For part two, we need to change the logic a little within the main "good_update" function

Intead of just returning if the update is good, we need to fix it. 

To do so, we could just iterate through and "swap" any incorrect numbers.

It would be nice if we could just build an 'accurate' orders function, but seemingly there is no "objective final order," no matter how I tried to build it, it didnt work.

So instead if the start and stop are wrong we just swap them and then check the whole thing again. 

Ugly, but it works.
"""

def reorder_with_constraints(update, constraints, pos_dict):
    # Check the order validity using pos_dict and constraints
    while not is_valid_order(constraints, pos_dict):  # Check every position after each update
        for _, row in constraints.iterrows():
            start = row['Start']
            end = row['End']
            start_idx = update.index(row['Start'])
            end_idx = update.index(row['End'])
    
            if start_idx > end_idx:
                # Swap the elements in the update list and pos_dict
                update[start_idx], update[end_idx] = update[end_idx], update[start_idx]
                pos_dict[start], pos_dict[end] = pos_dict[end], pos_dict[start]
    
    return update


## fixes bad updates
def bad_update(update):
    actual_orders = get_actual_orders(update) # get the actual orders that apply to this update 
    pos_dict = {}
    for i, num in enumerate(update):
        pos_dict[num] = i
    sorted_update = reorder_with_constraints(update, actual_orders, pos_dict) # resort the update to make sure it follows those orders
    val = int((len(sorted_update) -1) / 2)
    return sorted_update[val]
 

# run logic on all the updates, accumulating middle values of good and bad updates separately
middles_naive= []
middles =[]
for i, update in enumerate(updates):
    # print(f"starting update {i}")
    if good_update(update):
        # print("good update")
        index = (len(update) -1) / 2 # eg from 5 -> 4 -> 2 = the middle index of 0, 1, 2, 3, 4
        middles_naive.append(update[int(index)])
    else:
        middles.append(bad_update(update))
    # print("completed update")
naive_sum = sum(middles_naive)
actual_sum = sum(middles)

print(f"naive_sum = {naive_sum}")
print(f"second_sum = {actual_sum}")
