import pandas as pd

## Part 1: find total difference between two lists ## 
# read into dataframe and then resort the cols individually from min to max

df = pd.read_csv("Inputs/day1_input.txt", names=['loc_a', 'loc_b'], sep='  ', index_col=False, engine='python')
df['loc_a'] = df['loc_a'].sort_values(ascending=True).reset_index(drop=True) 
df['loc_b'] = df['loc_b'].sort_values(ascending=True).reset_index(drop=True)

 # find the difference between the two, take abs, then sum
df['diff'] = abs(df['loc_a'] - df['loc_b'])
difference = df['diff'].sum()
print("Answer one: ", difference)

## Part 2: Similarity Scores ##
# Calculate a total similarity score by adding up each number in the left list 
# after multiplying it by the number of times that number appears in the right list. 

# first get the count for each number in the right list
counts = df.copy()
counts = counts['loc_b'].value_counts().reset_index()
counts.columns = ['loc_a', 'count'] #rename for merging

# now merge with the original frame on the loc_a value
df = pd.merge(
    left=df,
    right=counts,
    on='loc_a',
    how='left'
)

# calc and report
df['sim_score'] = df['loc_a'] * df['count']
total_score = df['sim_score'].sum()
print("Answer two: ", total_score)