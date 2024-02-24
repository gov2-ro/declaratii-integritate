""" 
## Prompt
Python script to read urls from a xlsx file and download them, following a folder structure.

script should load a xlsx file found in `data/decl csv url.xlsx` with the following columns: data,	tip,	url_decl,	downloaded

The script should read the date in `data` - format dd.mm.yyyy create a folder structure in the following way: <yyyy>/<mm>/<tip> and download the file from https://declaratii.integritate.eu/DownloadServlet?fileName=<url_decl> to the folder structure. Create required folders if they don't exist.
After file is downloaded, mark the `downloaded` column with `1` for the respective row. Or if the file is not found, mark the `downloaded` column with `0`. 

Use try / except to handle errors and log them in a file called `data/error.log` with the following format: `date - data - url_decl - error message`

stop a random number of seconds between 0.5 and 2 before downloading the next file.

script should not overwrite, skip files that are already downloaded - resume where it left from. At the beginning of the script read `data/decl csv url.xlsx` and only attempt downloading the files that are not downloaded yet, where the downloaded column is empty.

Sample `decl csv url.xlsx` data:

    data,tip,url_decl,downloaded
    31.01.2024,dI,16037936_2858993_a.pdf&uniqueIdentifier=NTNTARTLNE_16037936,
    19.01.2024,dI,16027942_2844314_a.pdf&uniqueIdentifier=NTNTARTLNE_16027942,
    19.01.2024,dI,16027935_2843964_a.pdf&uniqueIdentifier=NTNTARTLNE_16027935,
    26.05.2007,dI2,3410669_3672011_DI_2007-05-26_ALECU%20SANDRA-OANA_63369.pdf&uniqueIdentifier=NTNTARTLNE_3410669,
    26.05.2007,dA2,2350515_1562660_DA_2007-05-26_VLADU%20MINODORA_40304915.pdf&uniqueIdentifier=NTNTARTLNE_2350515,
    26.05.2007,dI2,1481808_594802_DI_2007-05-26_MACAU%20SALVINA_10096411.pdf&uniqueIdentifier=NTNTARTLNE_1481808,
    26.05.2007,dA2,1476464_600135_DA_2007-05-26_MAN%20NICOLAE_10100544.pdf&uniqueIdentifier=NTNTARTLNE_1476464,
    26.05.2007,dA2,1424389_628592_DA_2007-05-26_GHEORGHE%20SVETLANA%20EUGENIA_20101499.pdf&uniqueIdentifier=NTNTARTLNE_1424389,

 """
data_root = '/Users/pax/devbox/gov2/data/'
file_path = data_root + "decl csv url.xlsx"
base_url = "https://declaratii.integritate.eu/DownloadServlet?fileName="
err_log = data_root + "dlpdf_error.log"

import pandas as pd
import requests
import os
import time
import random
from datetime import datetime

def download_file(url, folder_path, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(folder_path, file_name), 'wb') as f:
            f.write(response.content)
        return True
    else:
        return False

def log_error(date, data, url_decl, message):
    with open(err_log, "a") as log_file:
        log_file.write(f"{date} - {data} - {url_decl} - {message}\n")

def create_folder_structure(date, tip):
    date_obj = datetime.strptime(date, "%d.%m.%Y")
    folder_path = os.path.join(str(date_obj.year), f"{date_obj.month:02}", tip)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def main():
    
    
    try:
        df = pd.read_excel(file_path, dtype=str)
        df['downloaded'] = df['downloaded'].fillna('')  # Fill NaN with empty strings

        for index, row in df.iterrows():
            if row['downloaded'] == '':
                folder_path = create_folder_structure(row['data'], row['tip'])
                file_name = row['url_decl'].split('&')[0]  # Assuming the file name is before '&'
                full_url = base_url + row['url_decl']

                try:
                    # Check if file already exists to avoid re-download
                    if not os.path.exists(os.path.join(folder_path, file_name)):
                        downloaded = download_file(full_url, folder_path, file_name)
                        df.at[index, 'downloaded'] = '1' if downloaded else '0'
                        time.sleep(random.uniform(0.5, 2))  # Wait for a random time before next download
                    else:
                        df.at[index, 'downloaded'] = '1'  # Mark as downloaded if file exists
                except Exception as e:
                    log_error(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), row['data'], row['url_decl'], str(e))
                    df.at[index, 'downloaded'] = '0'

        # Save the DataFrame back to Excel
        df.to_excel(file_path, index=False)
    except Exception as e:
        log_error(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "General", "N/A", str(e))

if __name__ == "__main__":
    main()
