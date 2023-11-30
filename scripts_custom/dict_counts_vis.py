import json
import pandas as pd
import plotly.express as px

# Read the JSON data from the file
with open('results/counts.json', 'r') as json_file:
    dict_counts = json.load(json_file)

# Convert dictionary to a DataFrame
df = pd.DataFrame(list(dict_counts.items()), columns=['Name', 'Value'])

value_describe = df['Value'].describe()
print(value_describe)
# Count the occurrences of each value
value_counts = df['Value'].value_counts().reset_index()
value_counts.columns = ['Value', 'Frequency']

# Calculate cumulative frequency
value_counts['Cumulative Frequency'] = value_counts['Frequency'].cumsum()

# Calculate normalized percentages
total_samples = value_counts['Frequency'].sum()
value_counts['Normalized Percentage'] = (value_counts['Cumulative Frequency'] / total_samples) * 100

# Create the cumulative frequency step plot
fig = px.line(value_counts, x='Value', y='Normalized Percentage', title='Cumulative Frequency Histogram (Normalized)')
fig.update_xaxes(title_text='Value')
fig.update_yaxes(title_text='Normalized Percentage')
fig.show()

