import csv
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def setup_driver(download_folder, gecko_driver_path):
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    firefox_options.set_preference("browser.download.folderList", 2)
    firefox_options.set_preference("browser.download.dir", download_folder)
    firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
    driver = webdriver.Firefox(service=FirefoxService(executable_path=gecko_driver_path), options=firefox_options)
    return driver

def navigate_to_advanced_search(driver, url):
    driver.get(url)
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.ID, "form:showAdvancedSearch"))).click()
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, "form:advanced-search-panel_content")))

def perform_search(driver, start_date, end_date):
    driver.find_element(By.ID, "form:endDate_input").clear()
    driver.find_element(By.ID, "form:endDate_input").send_keys(end_date)
    driver.find_element(By.ID, "form:startDate_input").clear()
    driver.find_element(By.ID, "form:startDate_input").send_keys(start_date)
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.ID, "form:submitButtonAS"))).click()

def parse_and_save_results(driver, csvfile, current_date, start_date, rez_count):
    csvwriter = csv.writer(csvfile)
    results_table = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, "form:resultsTable")))
    rows = results_table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip header row
    
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")[:-1]  # Exclude last 'Distribuie' column
        vezi_declaratie_link = row.find_element(By.XPATH, ".//a[contains(text(),'Vezi document')]").get_attribute("href")
        row_data = [cell.text for cell in cells] + [vezi_declaratie_link, rez_count, start_date, current_date]
        csvwriter.writerow(row_data)

def main():
    driver = setup_driver(csv_downloads_folder, gecko_driver_path)
    try:
        navigate_to_advanced_search(driver, source_url)
        with open(target_csv, "a", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            # Write CSV header
            csvwriter.writerow(["Data", "Nume", "Functie", "Institutie", "Tip declaratie", "An", "Vezi declaratie", "Rezultate", "Data inceput", "Data sfarsit"])
            current_date = "14.10.2023"  # Example start date

            while current_date > end_date:
                start_date = (datetime.strptime(current_date, "%d.%m.%Y") - timedelta(days=days_delta)).strftime("%d.%m.%Y")
                perform_search(driver, start_date, current_date)

                # Example for handling result count; implement your logic as needed
                rez_count = "Example"  # Placeholder for actual result count retrieval logic

                parse_and_save_results(driver, csvfile, current_date, start_date, rez_count)

                # Update `current_date` for the next iteration
                current_date = (datetime.strptime(start_date, "%d.%m.%Y") - timedelta(days=days_delta)).strftime("%d.%m.%Y")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    # Configuration
    target_csv = "../../data/declaratii.integritate.eu/declaratii-ani.csv"
    days_delta = 2
    timeout = 2
    end_date = "01.01.2008"
    csv_downloads_folder = "/Users/pax/devbox/gov2/data/declaratii.integritate.eu/csvs/"
    gecko_driver_path = 'geckodriver/geckodriver'
    source_url = "https://declaratii.integritate.eu/index.html"

    main()
