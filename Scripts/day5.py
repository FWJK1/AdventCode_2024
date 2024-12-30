import re
import itertools
import pandas as pd

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

## check to see whether a given update follows the rules
def good_update(update):
    # reduce permutations to those that are actual orders
    possible_orders = list(itertools.permutations(update, 2))
    possible_orders = pd.DataFrame(possible_orders, columns = ['Start', 'End'])
    actual_orders = pd.merge(
        left=orders,
        right=possible_orders,
        on=['Start', 'End'],
        how='inner'
    )

    # create a position dictionary
    pos_dict = {}
    for i, num in enumerate(update):
        pos_dict[num] = i
    # print(update, pos_dict, possible_orders)

    # run the logic and return
    actual_orders['respected'] = actual_orders.apply(
        lambda row: is_respected(row, pos_dict), axis=1
    )
    # print(actual_orders)
    # print( actual_orders['respected'].all()) # returns bool if col has all true vals else false
    return actual_orders['respected'].all()

good_update(updates[0])

# run logic on all the updates, accumulating middle values of good updates
middles = []
for i, update in enumerate(updates):
    # print(f"starting update {i}")
    if good_update(update):
        # print("good update")
        index = (len(update) -1) / 2 # eg from 5 -> 4 -> 2 = the middle index of 0, 1, 2, 3, 4
        middles.append(update[int(index)])
    # print("completed update")
naive_sum = sum(middles)
print(f"naive_sum = {naive_sum}")



## part two
""""
For part two, we need to change the logic a little within the main "good_update" function

Intead of just returning if the update is good, we need to fix it. 

To do so, we could just iterate through and "swap" any incorrect numbers.

"""