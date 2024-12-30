import re

## Part 1: find only parts of text like mul(11,8) ## 
with open("Inputs/day3_input.txt", "r") as f:
    buff = f.read()

def get_nums(string):
    #use regex to get all the strings with format "mul(digit, digit)"
    matches = re.findall(r'mul\(\d+,\d+\)', string)  

    # then get the digits from these matches and multiply them
    tuples = [re.search(r'(\d+),(\d+)', text).groups() for text in matches]
    multiplications = [int(x)*int(y) for x,y in tuples]
    return sum(multiplications)

naive_sum = get_nums(buff)
print(f"The naive total = {naive_sum}")

## Part 2: apply conditional logic of DO and DONT ## 
## idea: split on every 'do', then sum only those that have a 'do' in them ##
buff_split = re.split(r"(do)", buff)

# recombine so that "don't" appears in full
merged = [buff_split[0]] + [buff_split[i] + buff_split[i + 1] for i in range(1, len(buff_split), 2)]
cum = 0
for string in merged:
    if "don't" in string: pass
    else:
         cum += get_nums(string)

print(f"The actual total = {cum}")