import pandas as pd
import re


## first get the data into a dataframe
levels = []
with open("Inputs/day2_input.txt", 'r') as f:
    for line in f:
        level = re.findall(r'\d+', line) ## regex to select all the digits
        level = [int(n) for n in level]
        levels.append(level)

df = pd.DataFrame(levels)
df = df.apply(pd.to_numeric, errors='coerce').astype('Int64')


## combined part 1 and part 2 ## 
# build an iterative function to check reports and remove levels to try other options
# note that this operates on lists, not pd.series. 
def row_check(row, score):
    sign = 0
    if score > 1:
        return score

    # iterate through list and check if good
    for i in range(len(row)-1):
        val1, val2 = row[i], row[i+1]
        if pd.isna(val2):
            break
        if not sign:
            sign = (val2 > val1) - (val2 < val1)
            # print(val1, val2, sign)

        if val2 in [val for val in range(val1-3, val1+4) if (sign == 0 and val != val1) or (sign < 0 and val < val1) or (sign > 0 and val > val1)]:
            pass
        else: ## if bad, bump up score and then check if removing a number would help
        
            # print(row)
            # print(f'score going up because {val1}, {val2}')
            # print("--" * 50)
            score += 1
            list_removed_i = row[:i] + row[i+1:]
            list_removed_ip1 = row[:i+1] + row[i+2:]
            
            return min(
                row_check(list_removed_i, score), 
                row_check(list_removed_ip1, score), 
                row_check(row[1:], score)
                        )
    return score

# vectorize row_check
def row_checker(row):
    return row_check(row.tolist(), 0)

df['safety_score'] = df.apply(row_checker, axis=1)
df['naive_safe'] = df['safety_score'] == 0
df['actual_safe'] = df['safety_score'] < 2
# print(df[df['safety_score'] == 2].head(20))
# print (df)


#sum and report 
naive_safe = df['naive_safe'].sum()
actual_safe = df['actual_safe'].sum()
print(f"There are {naive_safe} reports that are safe without the dampener, and {actual_safe} with the dampener.")