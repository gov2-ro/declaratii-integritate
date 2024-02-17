""" 

 """

 


import pandas as pd

# Define file paths
data_folder = '/Users/pax/devbox/gov2/data/declaratii.integritate.eu/'
csv1_path = data_folder + 'declaratii-ani-dl-csvs.csv'
csv2_path = data_folder + 'declaratii-ani.csv'
output_path = data_folder + 'declaratii-ani-consolidated.csv'

# Load CSVs into DataFrames
df_csv1 = pd.read_csv(csv1_path)
df_csv2 = pd.read_csv(csv2_path)

# Standardize column names (remove trailing spaces)
df_csv1.columns = df_csv1.columns.str.strip()
df_csv2.columns = df_csv2.columns.str.strip()

# Define the columns to join on
join_columns = ['Nume Prenume', 'Institutie', 'Data completare declaratie', 'Tip declaratie']

# Merge the two DataFrames horizontally
merged_df = pd.merge(df_csv1, df_csv2, on=join_columns, how='outer', indicator=True)

# Add 'merged_status' column based on the '_merge' indicator
merged_df['merged_status'] = merged_df['_merge'].replace({'left_only': 'csv1_csvz', 'right_only': 'csv2_tables', 'both': 'both'})

# Drop the '_merge' column as it's no longer needed
merged_df.drop(columns=['_merge'], inplace=True)

# Save the merged DataFrame to CSV
merged_df.to_csv(output_path, index=False)

print(f"Merged CSV saved to {output_path}")
