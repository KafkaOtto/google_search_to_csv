import pandas as pd
import matplotlib.pyplot as plt
import io
import base64


file_path = '..//data/data_extraction.xlsx'
sheets_to_analyze = ['google_scholar_result', 'snowballing', 'google_search_02']

overall_counts = {}

for sheet in sheets_to_analyze:
    df = pd.read_excel(file_path, sheet_name=sheet)
    df_keep = df[df['status'] == 'keep']

    # Identify the exact column name for "impacted part"
    col_name = None
    for col in df_keep.columns:
        if col.strip().lower() == 'impacted part':
            col_name = col
            break

    # If no "impacted part" column found, skip this sheet
    if col_name is None:
        continue

    # Split comma-separated values and aggregate
    for val in df_keep[col_name]:
        if pd.isna(val):
            continue
        parts = [p.strip() for p in str(val).split(',')]
        for part in parts:
            if part:
                overall_counts[part] = overall_counts.get(part, 0) + 1

# 3. Rename keys from "retriever" -> "retrieval" and "generator" -> "generation"
rename_map = {
    'retriever': 'retrieval',
    'generator': 'generation'
}

new_counts = {}
for old_key, count in overall_counts.items():
    new_key = rename_map.get(old_key, old_key)  # Use renamed key if in rename_map, otherwise keep old_key
    new_counts[new_key] = new_counts.get(new_key, 0) + count

# 4. Prepare final counts in the order: data, retrieval, generation, pipeline
final_order = ['data', 'retrieval', 'generation', 'pipeline']
final_counts = {}
for item in final_order:
    final_counts[item] = new_counts.get(item, 0)

# 5. Plot the bar chart
keys = list(final_counts.keys())
values = list(final_counts.values())

plt.figure(figsize=(6, 4))
plt.bar(keys, values, color='blue', edgecolor='black')
plt.xlabel('Impacted Part')
plt.ylabel('Count')
# No title, as requested
plt.tight_layout()

# 6. Encode the resulting chart as a base64 PNG and print
buf = io.BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)
img_base64 = base64.b64encode(buf.read()).decode('utf-8')

print(img_base64)
