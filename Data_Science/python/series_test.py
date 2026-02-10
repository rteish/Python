import pandas as pd

# Correct way to create a Series
character = ['a', 'b', 'c', 'd']
# Use pd.Series (Capital 'S')
c = pd.Series(character)

print(c)
