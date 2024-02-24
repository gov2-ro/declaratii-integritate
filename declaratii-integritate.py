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
import time


target_csv = "../../data/declaratii.integritate.eu/declaratii-ani.csv"
scrapping_log = "../../data/declaratii.integritate.eu/scrapping-log.csv"
days_delta =   6
timeout =   2
end_date = "01.01.2008"
csv_downloads_folder = "/Users/pax/devbox/gov2/data/declaratii.integritate.eu/csvs/"
csv_basename = 'declaraii-'
source_url = "https://declaratii.integritate.eu/index.html"
err_log = "../../data/declaratii.integritate.eu/error.log"
gecko_driver_path = 'geckodriver/geckodriver'
log_lvl = '' # 'silent', 'verbose', 'errors', 'default'

def setup_webdriver():
    firefox_options = Options()
    firefox_options.add_argument("--headless=new")
    firefox_options.set_preference("browser.download.folderList",   2)
    firefox_options.set_preference("browser.download.dir", csv_downloads_folder)
    firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
    return webdriver.Firefox(service=FirefoxService(executable_path=gecko_driver_path), options=firefox_options)

def log_activity(activity_details):
    # Assuming activity_details is a list where each element is a string
    # Convert all elements to strings if they are not already
    activity_details = [str(detail) for detail in activity_details]
    
    with open(scrapping_log, 'a', newline='') as log_file:
        log_writer = csv.writer(log_file)
        log_writer.writerow(activity_details)


def get_current_date():
    return datetime.now().strftime("%d.%m.%Y")

def get_previous_date(current_date):
    return (datetime.strptime(current_date, "%d.%m.%Y") - timedelta(days=1)).strftime("%d.%m.%Y")

def get_last_date_from_log():
    try:
        with open(scrapping_log, 'r') as log_file:
            log_reader = csv.reader(log_file)
            last_row = list(log_reader)[-1]
            return (datetime.strptime(last_row[1], "%d.%m.%Y") - timedelta(days=1)).strftime("%d.%m.%Y")
    except Exception as e:
        print(f"Error reading last date from log: {e}")
        return None

def check_for_error_message(driver):
    try:
        # driver.find_element_by_xpath("//*[contains(text(), 'utarea întoarce mai mult de 10')]")
        driver.find_element("xpath", "//*[contains(text(), 'utarea întoarce mai mult de 10')]")

        print("Error detected: too many results")
        log_activity([datetime.now(), '', 'Error detected: too many results', 'err', 'Too many results'])
        return True  # Return True to indicate an error was detected
        # # Wait for the error dialog title to be present in the DOM
        # error_dialog_title = WebDriverWait(driver, timeout).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, ".ui-dialog.ui-widget.ui-widget-content.ace-dialog .ui-dialog-title"))
        # )
        # if 'Eroare' in error_dialog_title.text:
        #     # Wait for the error message to be present in the DOM
        #     error_message = WebDriverWait(driver, timeout).until(
        #         EC.presence_of_element_located((By.CSS_SELECTOR, ".ui-dialog.ui-widget.ui-widget-content.ace-dialog .contPop h3 span"))
        #     )
        #     if any(error in error_message.text for error in ['întoarce mai mult de', 'rafinați termenii', 'de căutare']):
        #         print(f"Error detected: {error_message.text}")
        #         log_activity([datetime.now(), current_date, 'Error detected: too many results', 'err', error_message.text])
        #         return True  # Return True to indicate an error was detected
    except (TimeoutException, NoSuchElementException):
        pass  # No error message detected
    return False  # Return False if no error message was detected


def perform_scraping(driver, current_date):
    # Navigate to the source URL
    driver.get(source_url)
    log_activity([datetime.now(), current_date, 'Navigated to source URL', 'ok', ''])

    # Click 'Căutare avansată' button if it's already present; otherwise, wait for it
    try:
        advanced_search_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, "form:showAdvancedSearch"))
        )
        advanced_search_button.click()
        if log_lvl == 'verbose':
            log_activity([datetime.now(), current_date, 'Clicked advanced search button', 'ok', ''])
    except TimeoutException:
        log_activity([datetime.now(), current_date, 'Failed to click advanced search button', 'err L69', 'Timeout'])
        return

    # Wait for the advanced search panel to load if it's already present; otherwise, wait for it
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "form:advanced-search-panel_content"))
        )
        if log_lvl == 'verbose':
            log_activity([datetime.now(), current_date, 'Advanced search panel loaded', 'ok', ''])
    except TimeoutException:
        log_activity([datetime.now(), current_date, 'Failed to load advanced search panel', 'err', 'Timeout'])
        return

    # Input the current start date and end date
    start_date = (datetime.strptime(current_date, "%d.%m.%Y") - timedelta(days=days_delta)).strftime("%d.%m.%Y")
    driver.find_element(By.ID, "form:endDate_input").clear()
    driver.find_element(By.ID, "form:endDate_input").send_keys(current_date)
    driver.find_element(By.ID, "form:startDate_input").clear()
    driver.find_element(By.ID, "form:startDate_input").send_keys(start_date)
    if log_lvl == 'verbose':
        log_activity([datetime.now(), current_date, 'Input start and end dates', 'ok', ''])

    # Click on the search button if it's already present; otherwise, wait for it
    try:
        search_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, "form:submitButtonAS"))
        )
        search_button.click()
        if log_lvl == 'verbose':
            log_activity([datetime.now(), current_date, 'Clicked search button', 'ok', ''])
    except TimeoutException:
        log_activity([datetime.now(), current_date, 'Failed to click search button', 'err L102', 'Timeout'])
        return

    # Check for 'too many results' error message
    if check_for_error_message(driver):
        print("Too many results error detected. Skipping to the next day.")
        log_activity([datetime.now(), current_date, 'Too many results detected: ' + current_date, 'err', '10k+'])
        return  # Skip the rest of the scraping process for the current date
    
 


    # Find and print the number of results
    try:
        results_count = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h5[contains(text(),'Rezultatele căutării:')]/span")
            )
        )
        print(f" -> {results_count.text} results for {start_date} to {current_date}")
        log_activity([datetime.now(), current_date, f'Found {results_count.text} results from {start_date} to {current_date}', 'ok', f'{results_count.text} results'])
    except TimeoutException:
        log_activity([datetime.now(), current_date, 'No results found ' + current_date + ' - ' + start_date +  'err l115', 'Timeout?'])
        if check_for_error_message(driver):
            print("Too many results error detected. Skipping to the next day 2.")
            # return  # Skip the rest of the scraping process for the current date
        return

    # Save csv file
    try:
        export_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, "form:dataExporter"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", export_button)
        export_button.click()
        log_activity([datetime.now(), current_date, 'CSV export', 'ok', 'csv'])
    except Exception as e:
        print(e)
        log_activity([datetime.now(), current_date, 'CSV export failed', 'err l129', str(e)])
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
    
        log_activity([datetime.now(), current_date, 'Table -> CSV', 'ok', str(len(rows)) + ' rows'])
    except TimeoutException:
        log_activity([datetime.now(), current_date, 'Failed to find data or save rows', 'err L158', 'Timeout'])
        return

    # Handle pagination
    count_pages = 0
    all_rows = int(results_count.text)
    crows = 0
    try:
        while True:
            # Wait for the next page link to be clickable
            next_page_link = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@id='form:resultsTable_paginatorbottom_nextPageLink' and not(contains(@class, 'ui-state-disabled'))]")))
            # Click the next page link
            next_page_link.click()
            if log_lvl == 'verbose':
                log_activity([datetime.now(), current_date, 'Navigated to next page', 'ok', ''])
            count_pages += 1
            # Wait for the results table to load on the next page
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.ID, "form:resultsTable")))
            
            # Repeat the process of saving data to CSV for the next page
            results_table = driver.find_element(By.ID, "form:resultsTable")
            rows = results_table.find_elements(By.TAG_NAME, "tr")
            for row in rows[1:]:
                cells = row.find_elements(By.TAG_NAME, "td")[:-1]  # Exclude the last 'Distribuie' column
                vezi_declaratie_link = row.find_element(By.XPATH, ".//a[contains(text(),'Vezi document')]").get_attribute("href")
                row_data = [cell.text for cell in cells]
                row_data.append(vezi_declaratie_link)   
                row_data.append(current_date)   
                row_data.append(start_date)   
                with open(target_csv, "a", newline="") as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(row_data)
                
            crows += len(rows)
            # Check if there is a next page link available
            next_page_link = driver.find_elements(By.XPATH, "//a[@id='form:resultsTable_paginatorbottom_nextPageLink' and not(contains(@class, 'ui-state-disabled'))]")
            if not next_page_link:
                break  # Exit the loop if there are no more pages
    except (StaleElementReferenceException, NoSuchElementException, TimeoutException):
        log_activity([datetime.now(), current_date, 'Pagination handling failed', 'err l198', 'Timeout or Element Not Found'])
        pass


    # log_activity([datetime.now(), current_date, 'Scraping completed for the day ' + str(current_date), 'ok', count_pages + ' pages  ' + crows + ' rows / ' + all_rows])
    log_activity([datetime.now(), current_date, 'Scraping completed for the day ' + str(current_date), 'ok', str(count_pages) + ' pages  ' + str(crows) + ' rows / ' + str(all_rows)])



def main():
    current_date = get_last_date_from_log()
    if current_date is None:
        current_date = get_current_date()

    runs =   0
    while current_date > end_date:
        runs +=   1
        try:
            # print(f"Run {runs} - {current_date}")
            print(runs, ' runs for', current_date)
            driver = setup_webdriver()
            perform_scraping(driver, current_date)
            driver.quit()
            print("q1 done")
            current_date = get_previous_date(current_date)
        except Exception as e:
            error_message = str(e) if e else "Unknown error"
            print(f"Error occurred: {error_message}")
            log_activity([str(datetime.now()), str(current_date), 'Scraping loop broken', 'err L224', error_message])
            
            driver.quit()
            print("q2 err")
            continue


    print("done")
    log_activity([datetime.now(), current_date, 'Scraping process completed', 'ok', ''])

if __name__ == "__main__":
    main()
