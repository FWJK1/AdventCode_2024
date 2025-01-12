import re
import numpy as np
import datetime
from collections import defaultdict, Counter


test_data = ["125", "17"]

with open("Inputs/day11_input.txt", "r") as f:
    data = f.read()

data = [str(val) for val in re.findall(r'(\d+)', data)]


## Part 1 ##
# Pretty simple; just create and apply rules

## quick helper func to split digit
def digit_splitter(num, length):
    split = int (length / 2)
    first = num[:split]
    last = num[split:]
    if last.count('0') == split:
        last = '0'
    last = str(int(last))
    return np.array([first, last])

## run one 'blink,' basically just some if/else
def blink(nums):
    nu_nums = []
    for num in nums:
        length = len(num)
        if num == '0':
            nu_nums.append('1')
        elif not (length % 2): ## if even num digits
            nu_nums.extend(digit_splitter(num, length))
        else:
            next = str(int(num) * 2024)
            nu_nums.append(next)
    
    return nu_nums # get rid of any leading 0s


def iterate_blinks(data, itt_count):
    # print(f"To start, the stones are: \n\t{data}. \n\t\tA total of {len(data)} stones.\n")
    for i in range(itt_count):
        print(i+1)
        data = blink(data)
        # print(f"After {i+1} iterations the stones are: \n\t{data}. \n\t\tA total of {len(data)} stones.\n")
        # print(f"After {i+1} iterations we have a total of {len(data)} stones.\n")

    
    print(f"\n\nIn the end there are {len(data)} total stones.")
    lengths = [len(stone) for stone in data]
    print(f"\nThe largest stone is  {max(lengths)} chars long")

    
# iterate_blinks(test_data, 25)


## Part 2 ##
"""
Okay, now we need to optimize ... 

for a while we try stuff that might improve processing speed... 
      ##  transition the digit maker to be log based 
      ##  precalculate a dictionary (largely foolish -- we could *add* to a dictionary if we really wanted
                and then use a function for anything NOT in it... but that's not needed)

but this isnt fast enough, so we look again and notice that really 
order DOESNT matter. just frequency! so we can work with a dict instead of a list ....
but it has to be a default dict because we need to add right into it.

This works very fast.
"""

## reworked helper func to convert a number into the first and second halves.
## uses log functions to avoid messing with strings
def digit_splitter(num, length):
    divisor = 10 ** (length // 2)
    num1 = int(num // divisor)
    num2  = int(num % divisor)
    return num1, num2

##  operate on one number at a time (because we are only going to work on one number at a time)
# need to always return an iterable, tho
def blink_num(num):
    length = np.floor(np.log10(num)) + 1 if num > 0 else 1
    if num == 0:
        return [1]
    elif not length % 2:
        return digit_splitter(num, length)
    else:
        return [num*2024]


def iterate_blinks(data, itt_count):
    # print(f"To start, the stones are: \n\t{data}. \n\t\tA total of {len(data)} stones.\n")
    data = [int(num) for num in data] #because splitter now just works with nums
    data = dict(Counter(data)) # the Counter object actually behaves like a dict already but this makes it clearer imo
    full_start = datetime.datetime.now()
    for i in range(itt_count):
        start_time = datetime.datetime.now()
        res = defaultdict(int) # default dict lets you add right in (the int gives default of 0 to add to)
        for num, freq in data.items():
            vals = blink_num(num)
            for val in vals:
                res[val] += freq
        data = res
        end_time = datetime.datetime.now()
        elapsed_time = end_time - start_time

        length = sum(data.values())
        elapsed_time = end_time - start_time 

        ## debug print block ## 
        # print(f"\nProcessed stone_line {i+1} in:", elapsed_time)
        # print(f"After {i+1} iterations the stones are: \n\t{data}. \n\t\tA total of {length} stones.")
        # print(f"After {i+1} iterations we have a total of {length} stones.")
        # print("--" * 50)

    full_end = datetime.datetime.now()
    elapsed_time = full_end - full_start

    print(f"\n\nIn the end (after {elapsed_time}) there are {length} total stones.")
iterate_blinks(data, 75)




### Posterity scratchwork ### 


# ## we can make a dict for every single number under some huge amount,
# ## that way we don't have to calculate in the moment...
# ## this is silly because it s just extra work  if we;re just going to only operate on each number once anyway
# dlimit = 7
# even_digit_nums = []
# for num in range(0, 10**dlimit):
#     if not len(str(num)) % 2:
#         even_digit_nums.append(num)
         

# operation_dict = {
#     0 : [1]
# }
# start_time = datetime.datetime.now()
# for num in even_digit_nums:
#     operation_dict[num] = digit_splitter_maker(num)

# end_time = datetime.datetime.now()
# elapsed_time = end_time - start_time
# print("Made dict in:", elapsed_time)