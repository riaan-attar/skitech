import pandas as pd

df = pd.read_csv('csv')
column_values = df['district'].values
printed_values = set()
output = ', '.join(['"' + value + '"' for value in column_values if value not in printed_values])
unique_values = list(set(output.split(', ')))
print(len(unique_values))
