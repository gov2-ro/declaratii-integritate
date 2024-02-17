import pandas as pd
import os
import shutil

data_folder = '/Users/pax/devbox/gov2/data/declaratii.integritate.eu/'
csv_downloads_folder = data_folder + "csvs/"
input_folder = csv_downloads_folder
output_file = data_folder + 'declaratii-ani-dl-csvs.csv'
archive_folder = csv_downloads_folder + 'parsed'

# Create the archive folder if it doesn't exist
os.makedirs(archive_folder, exist_ok=True)

# List all CSV files in the folder
csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

# Read and concatenate CSV files while removing duplicates
df_new_data = pd.concat([pd.read_csv(os.path.join(input_folder, f)) for f in csv_files]).drop_duplicates()

# If output_file exists, read it and concatenate with new data, else use new data
if os.path.exists(output_file):
    df_existing_data = pd.read_csv(output_file)
    df_combined = pd.concat([df_existing_data, df_new_data]).drop_duplicates()
else:
    df_combined = df_new_data

# Save the combined data to output_file
df_combined.to_csv(output_file, index=False)

# Move the input CSVs to 'data/parsed'
for f in csv_files:
    shutil.move(os.path.join(input_folder, f), os.path.join(archive_folder, f))

print("CSV files have been concatenated, duplicates removed, and original files moved to 'data/parsed'.")
