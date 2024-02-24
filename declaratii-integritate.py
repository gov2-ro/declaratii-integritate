from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, ElementNotInteractableException, NoSuchElementException
import csv
from datetime import datetime, timedelta
import os
import sys

# Configuration
target_csv = "../../data/declaratii.integritate.eu/declaratii-ani.csv"
scrapping_log = "../../data/declaratii.integritate.eu/scrapping-log.csv"
days_delta =  2
timeout =  2
end_date = "01.01.2008"
csv_downloads_folder = "/Users/pax/devbox/gov2/data/declaratii.integritate.eu/csvs/"
csv_basename = 'declaraii-'
source_url = "https://declaratii.integritate.eu/index.html"
err_log = "../../data/declaratii.integritate.eu/error.log"
gecko_driver_path = 'geckodriver/geckodriver'

# Selenium WebDriver setup
def setup_webdriver():
    firefox_options = Options()
    firefox_options.add_argument("--headless=new")
    firefox_options.set_preference("browser.download.folderList",  2)
    firefox_options.set_preference("browser.download.dir", csv_downloads_folder)
    firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
    return webdriver.Firefox(service=FirefoxService(executable_path=gecko_driver_path), options=firefox_options)

# Logging activities
def log_activity(activity_details):
    with open(scrapping_log, 'a', newline='') as log_file:
        log_writer = csv.writer(log_file)
        log_writer.writerow(activity_details)

# Date calculations
def get_current_date():
    return datetime.now().strftime("%d.%m.%Y")

def get_previous_date(current_date):
    return (datetime.strptime(current_date, "%d.%m.%Y") - timedelta(days=1)).strftime("%d.%m.%Y")

# Scraping tasks
def perform_scraping(driver, current_date):
    # Navigate to the source URL
    driver.get(source_url)

    # Click 'Căutare avansată' button if it's already present; otherwise, wait for it
    try:
        advanced_search_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, "form:showAdvancedSearch"))
        )
        advanced_search_button.click()
    except TimeoutException:
        log_activity([datetime.now(), current_date, '--', 'err', 'pass  59'])
        return

    # Wait for the advanced search panel to load if it's already present; otherwise, wait for it
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "form:advanced-search-panel_content"))
        )
    except TimeoutException:
        log_activity([datetime.now(), current_date, '--', 'err', 'pass  75'])
        return

    # Input the current start date and end date
    start_date = (datetime.strptime(current_date, "%d.%m.%Y") - timedelta(days=days_delta)).strftime("%d.%m.%Y")
    driver.find_element(By.ID, "form:endDate_input").clear()
    driver.find_element(By.ID, "form:endDate_input").send_keys(current_date)
    driver.find_element(By.ID, "form:startDate_input").clear()
    driver.find_element(By.ID, "form:startDate_input").send_keys(start_date)

    # Click on the search button if it's already present; otherwise, wait for it
    try:
        search_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, "form:submitButtonAS"))
        )
        search_button.click()
    except TimeoutException:
        log_activity([datetime.now(), current_date, '--', 'err', 'pass  86'])
        return

    # Find and print the number of results
    try:
        results_count = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h5[contains(text(),'Rezultatele căutării:')]/span")
            )
        )
        print(f" -> {results_count.text} results for {start_date} to {current_date}")
    except TimeoutException:
        log_activity([datetime.now(), current_date, '-', 'err', 'pass  156'])
        return

    # Save csv file
    try:
        export_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, "form:dataExporter"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", export_button)
        export_button.click()
        log_activity([datetime.now(), current_date, 'real savecsv', 'ok', 'xx saved csv'])
    except Exception as e:
        print(e)
        log_activity([datetime.now(), current_date, '-  183', 'err', str(e)])
        return

    # Find the table and save data to CSV file
    try:
        results_table = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "form:resultsTable"))
        )
        rows = results_table.find_elements(By.TAG_NAME, "tr")
        header = [header.text for header in rows[0].find_elements(By.TAG_NAME, "th")[:-1]]  # Exclude the last 'Distribuie' header
        header.append("Vezi declaratie")   
        header.append("page")   
        header.append("rezultate")   
        header.append("start_date")   
        header.append("end_date")

        with open(target_csv, "a", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(header)

            for row in rows[1:]:
                cells = row.find_elements(By.TAG_NAME, "td")[:-1]  # Exclude the last 'Distribuie' column
                vezi_declaratie_link = row.find_element(By.XPATH, ".//a[contains(text(),'Vezi document')]").get_attribute("href")
                row_data = [cell.text for cell in cells]
                row_data.append(vezi_declaratie_link)   
                row_data.append(current_date)   
                row_data.append(start_date)   
                csvwriter.writerow(row_data)
    except TimeoutException:
        log_activity([datetime.now(), current_date, '-', 'err', 'pass  187'])
        return

    # Handle pagination
    try:
        pagination = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ui-paginator-pages"))
        )
        next_page_link = driver.find_elements(By.XPATH, "//a[@id='form:resultsTable_paginatorbottom_nextPageLink' and not(contains(@class, 'ui-state-disabled'))]")
        while next_page_link:
            driver.execute_script("arguments[0].scrollIntoView();", next_page_link[0])
            next_page_link[0].click()
            # Repeat the process of saving data to CSV for the next page
            # This part is simplified for brevity. You should implement the logic to save data from the next page.
    except (StaleElementReferenceException, NoSuchElementException, TimeoutException):
        pass

    log_activity([datetime.now(), current_date, 'tbscrp', '', ''])


# Main execution
def main():
    current_date = get_current_date()
    runs =  0
    while current_date > end_date:
        runs +=  1
        try:
            print(f"Run {runs} - {current_date}")
            driver = setup_webdriver()
            perform_scraping(driver, current_date)
            driver.quit()
            print("q1 done")
            current_date = get_previous_date(current_date)
        except Exception as e:
            print(f"Error occurred: {e}")
            log_activity([datetime.now(), current_date, 'broken loop', 'err end', str(e)])
            driver.quit()
            print("q2 done")
            continue

    print("done")
    log_activity([datetime.now(), current_date, 'done', 'ok', 'finished proper? run: ' + str(runs)])

if __name__ == "__main__":
    main()
