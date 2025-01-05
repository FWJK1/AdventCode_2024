def day9_read_data(file):
    with open(file, 'r') as f:
        data =  f.read()
    nums = [int(num) for num in data if num != '\n']
    return nums

## choose which to run ##
# data = day9_read_data("Test_inputs/day9_test.txt")
data = day9_read_data("Inputs/day9_input.txt")


## first convert to the 1..2 type of format from the question
block_style = []
empty_spots = []
count, pos = 0, 0
for i, num in enumerate(data):
    if not i % 2: # eg 0,2 -- the storage bits
        pos += num
        for j in range(num):
            block_style.append(count)
        count += 1
    else:
        for j in range(num):
            block_style.append('.')
            empty_spots.append(pos)
            pos += 1

## debug print ## 
# print(block_style)
# print(empty_spots)

## nno move the bits around
#  i = eend pointer, j = last point
i = 0
j = len(block_style) -1 
while i < j:
    val1 = block_style[i] ## eg at the beginning
    val2 = block_style[j] ## eg at the end
    if val1 == '.' and val2 != '.' :
        block_style[i] = val2
        block_style[j] = val1
        i += 1
        j -= 1
    elif val1 == '.' and val2 == '.' :
        j-=1
    else:
        i += 1
    

# print(block_style)

nums = [int(num) for num in block_style if num != '.']
val =  0 
for i, num in enumerate(nums):
    val += (i * num)

print(f"The naive answer is {val}")




## part 2 ## 
## create a list of tuples (is_storage, size, ID) where ID for storage sections is always -1
counter = -1
positions = [(False, val, -1) if i % 2 else (True, val, (counter := counter + 1)) for i, val in enumerate(data)]
# print(positions)
i = 0
j = len(positions) - 1


## calcualte through the postions. again, with j counting back and and i counting up to j #
# but for each 
for j in range(len(positions)-1, 0, -1):
    ## debug print block ## 
    # results = [position[2] if position[0] else '.' for position in positions for _ in range(position[1])]
    # print(''.join(str(result) for result in results))

    to_empty = positions[j]
    for i in range(0, j):
        to_fill = positions[i]
        diff = to_fill[1] - to_empty[1]
        if to_fill[0]: ## eg already full
            pass
        elif not to_empty[0]: ## eg what we want to move is storage so we skip it
            break
        elif diff == 0: ## eg they are the same size
            positions[i] = to_empty
            positions[j] = to_fill
            break
        elif diff > 0: ## eg the one to fill is larger than the smaller one; we have to leave some empty
            positions[i] = to_empty
            positions[j] = (False, to_empty[1], -1)
            positions.insert(i+1,(False, diff, 1))
            break

# print(positions) #

results = [position[2] if position[0] else '.' for position in positions for _ in range(position[1])]
nums = [int(num) if num != '.' else 0 for num in results]
val =  0 
for i, num in enumerate(nums):
    val += (i * num)

print(f"The better answer is {val}")    


