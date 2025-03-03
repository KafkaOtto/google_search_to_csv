import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Read the Excel file
file_path = "../data/data_extraction.xlsx"  # Update with actual file path
xls = pd.ExcelFile(file_path)

# Get the relevant sheets
dfs = {sheet: xls.parse(sheet) for sheet in xls.sheet_names[:3]}

def split_lowercase_and_count(values):
    counter = Counter()
    for value in values.dropna():  # Drop NaN values before processing
        for sub_value in map(str.strip, str(value).lower().split(',')):  # Split by comma, strip spaces, and lowercase
            counter[sub_value] += 1
    return counter

# Filter rows where status is 'keep'
filtered_dfs = {sheet: df[df['status'] == 'keep'] for sheet, df in dfs.items()}

lowercase_challenge_group_analysis = {
    sheet: split_lowercase_and_count(filtered_df['challenge group'])
    for sheet, filtered_df in filtered_dfs.items() if 'challenge group' in filtered_df.columns
}

# Aggregate all challenge group counts
aggregated_counts = Counter()
for analysis in lowercase_challenge_group_analysis.values():
    aggregated_counts.update(analysis)

# Convert to DataFrame for plotting
df_aggregated = pd.DataFrame(aggregated_counts.items(), columns=['Challenges', 'Count'])
df_aggregated = df_aggregated.sort_values(by='Count', ascending=False)

# Calculate total count for x-axis label
total_count = df_aggregated['Count'].sum()

# Plot histogram
plt.figure(figsize=(12, 6))
plt.bar(df_aggregated['Challenges'], df_aggregated['Count'])
plt.xticks(rotation=45, ha='right')
plt.xlabel(f'Challenges ({total_count})')
plt.ylabel('Count')
plt.title('Challenge Categories')
plt.show()
