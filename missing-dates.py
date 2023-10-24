import pandas as pd
from datetime import datetime, timedelta

target_csv = "../../data/declaratii.integritate.eu/declaratii-ani.csv"
# Load the CSV file into a pandas DataFrame
df = pd.read_csv(target_csv)

# Convert the 'Data completare declaratie' column to datetime objects
df['Data completare declaratie'] = pd.to_datetime(df['Data completare declaratie '], format='%d.%m.%Y')

# Find the minimum and maximum dates
min_date = df['Data completare declaratie '].min()
max_date = df['Data completare declaratie '].max()

# Create a list of all dates between the min and max date (excluding weekends)
date_range = pd.date_range(start=min_date, end=max_date, freq='D')
weekdays = [date for date in date_range if date.weekday() < 5]  # Weekdays are 0-4 (Monday to Friday)

# Find the missing dates
missing_dates = [date for date in weekdays if date not in df['Data completare declaratie ']]

print(f"Minimum Date: {min_date}")
print(f"Maximum Date: {max_date}")
print(f"Missing Dates (excluding weekends):")
for date in missing_dates:
    print(date.strftime('%Y-%m-%d'))
