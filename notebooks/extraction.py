import time
import logging
import os
import subprocess
import pandas as pd
import variables
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException,
    NoSuchWindowException,
    UnexpectedAlertPresentException,
    SessionNotCreatedException
)
from zipfile import ZipFile
from variables import Variables

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
df = pd.DataFrame(list(Variables.items()), columns=["Description", "Code"])
def scroll_down(driver, TimeWait):           #driver.execute_script("window.scrollBy(0,10);")
    time.sleep(1)
    next_element = WebDriverWait(driver, TimeWait).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="first"]/table/tbody/tr[1]/td[2]/span'))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", next_element)

def wait_for_download(path, TimeWait):
    download_wait_time = 0
    download_complete = False
    while not download_complete and download_wait_time < TimeWait:
        time.sleep(1)
        download_wait_time += 1
        for file_name in os.listdir(path):
            if file_name.endswith(".crdownload") or file_name.endswith(".part"):
                download_complete = False
                break
            download_complete = True
    if not download_complete:
        raise Exception("Download did not complete within the expected time.")

def handle_finder_dialog(path, file_name):
    # AppleScript to handle the Finder dialog
    script = f'''
    tell application "System Events"
        delay 1
        keystroke "G" using {{command down, shift down}}
        delay 1
        keystroke "{path}"
        delay 1
        keystroke return
        delay 1
        keystroke "{file_name}"
        delay 1
        keystroke return
        delay 1
        keystroke return
    end tell
    '''
    subprocess.run(['osascript', '-e', script])

def download_hydrometeorological_data(driver, path, variable, param, departamento, code, date_ini, date_fin, retries=3):
    TimeWait = 40

    for attempt in range(retries):
        try:
            logging.info("Starting hydrometeorological data download process.")
            # Variable selection
            try:
                logging.info("Selecting variable.")
                dropdown = WebDriverWait(driver, TimeWait).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "k-dropdown-wrap"))
                )
                dropdown.click()
                options_list = WebDriverWait(driver, TimeWait).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul[aria-hidden='false'] li"))
                )

                for option in options_list:
                    if variable in option.text:
                        option.click()
                        print(f"Selected variable: {variable}")
                        break
                
                scroll_down(driver, TimeWait)
            except TimeoutException:
                logging.error("TimeoutException: Failed to find the variable dropdown or options.")
                driver.quit()
                return
            except NoSuchElementException:
                logging.error("NoSuchElementException: Failed to find the variable dropdown or options.")
                driver.quit()
                return
            except ElementNotInteractableException:
                logging.error("ElementNotInteractableException: The variable dropdown or options are not interactable.")
                driver.quit()
                return
            except Exception as e:
                logging.error(f"Failed to select variable: {e}")
                driver.quit()
                return
            # Parameter selection
            logging.info("Step 3: Selecting parameter.") 
            WebDriverWait(driver, TimeWait).until(
                EC.presence_of_all_elements_located((By.XPATH, "//input[@name='variablelista[]']"))
            )
            scroll_down(driver, TimeWait) 
            driver.find_element(By.ID, "radio82").click() #radio82
            driver.find_element(By.XPATH, f"//td[contains(text(), '{param}')]/preceding-sibling::td/input").click()
            logging.info(f"Selected parameter: {param}")
            scroll_down(driver, TimeWait)
            # Department selection
            logging.info("Step 4: Selecting department.") 
            time.sleep(1)
            dept_dropdown = WebDriverWait(driver, TimeWait).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="first"]/table/tbody/tr[1]/td[2]/span'))
            )
            # dept_dropdown = WebDriverWait(driver, TimeWait).until(
            #     EC.element_to_be_clickable((By.XPATH, '//*[@id="first"]/table/tbody/tr[1]/td[2]/span/span/span[1]'))
            # )
            driver.execute_script("arguments[0].click();", dept_dropdown)
            time.sleep(1)
            dept_option = WebDriverWait(driver, TimeWait).until(
                EC.element_to_be_clickable((By.XPATH, f"//ul[@aria-hidden='false']//li[text()='{departamento}']"))
            )
            driver.execute_script("arguments[0].click();", dept_option)
            logging.info(f"Selected department: {departamento}")
            # Click the "Filtrar" button
            scroll_down(driver, TimeWait)
            logging.info("Clicking the 'Filtrar' button.") 
            filtrar_button = WebDriverWait(driver, TimeWait).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="first"]/div[3]/div'))  
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", filtrar_button)
            driver.execute_script("arguments[0].click()", filtrar_button)
            logging.info("Clicked the 'Filtrar' button.")

            time.sleep(2)
            try:
                # Enter the station code
                code_input = WebDriverWait(driver, TimeWait).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="search-codigo"]'))
                )
                code_input.send_keys(code)
                logging.info(f"Code wrote: {code}")

                # Scroll down to make sure the checkbox is visible
                scroll_down(driver, TimeWait)

                # Locate and select the checkbox with the station code
                checkbox = WebDriverWait(driver, TimeWait).until(
                    EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{code}')]/preceding-sibling::td/input"))
                )
                driver.execute_script("arguments[0].click();", checkbox)
                logging.info(f"Selected checkbox for station code: {code}")

                # Verify if the checkbox is selected
                if not checkbox.is_selected():
                    logging.warning(f"Checkbox for station code {code} not selected. Retrying...")
                    driver.execute_script("arguments[0].click();", checkbox)
                    if not checkbox.is_selected():
                        raise Exception(f"Failed to select checkbox for station code {code}")

            except Exception as e:
                logging.error(f"Failed to select station code {code}. Error: {e}")
                continue  # Continue with the next station code

            scroll_down(driver, TimeWait)
            #Set date range

            logging.info("Step 7: Setting the date")
            date_fields = [
                ('//*[@id="datepicker"]', date_ini),
                ('//*[@id="datepicker1"]', date_fin)
            ]
            for field_xpath, date_value in date_fields:
                date_box = WebDriverWait(driver, TimeWait).until(
                    EC.element_to_be_clickable((By.XPATH, field_xpath))
                )
                date_box.clear()
                date_box.send_keys(date_value)
            logging.info(f"Set date range: {date_ini} to {date_fin}")
            # Step 8: Select next 
            logging.info("Step 8: Agregar la consulta")
            time.sleep(2)
            button = WebDriverWait(driver, TimeWait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="first"]/div[6]/div[1]')))
            button.click()

            # Select the format to download the data/CSV
            logging.info("Step 9: Select CSV format.")

            WebDriverWait(driver, TimeWait).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="OptionCSV"]'))
            ).click()
            # Download button sequence
            WebDriverWait(driver, TimeWait).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="second"]/div/div[4]/div[1]'))
            ).click()
            download_button = WebDriverWait(driver, TimeWait).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="dijit_form_Button_2_label"]'))
            )
            download_button.click()
            logging.info("Download initiated.")
            time.sleep(TimeWait*0.5)
            handle_finder_dialog(path, "report.zip")
            wait_for_download(path, TimeWait)
             # Ensure the downloaded file is stored correctly
            logging.info("Ensuring the downloaded file is stored correctly.")
            zip_file_path = f"{path}report.zip"
            if os.path.exists(zip_file_path):
                logging.info(f"File stored at: {zip_file_path}")
            else:
                raise Exception("Downloaded file not found.")
            logging.info("Data download and processing completed successfully.")
        except Exception as e:
            if attempt < retries - 1:
                logging.warning(f"Attempt {attempt + 1} failed. Retrying... Error: {e}")
                time.sleep(2)
            else:
                logging.error(f"Max retries reached. Failed to complete the download process. Error: {e}")
                raise
        print("Data download and processing completed successfully.")
    driver.quit()


def DHIME_Download(path, variable, param, departamento, code, date_ini, date_fin):
    print("Initializing the Safari driver...")
    driver = webdriver.Safari()
    driver.get("http://dhime.ideam.gov.co/atencionciudadano/")

    TimeWait = 60  # Time to wait for elements to load

    # Step 1: Handle the checkbox for terms and conditions
    try:
        print("Waiting for the checkbox (Términos y condiciones) to be clickable...")

        checkbox = WebDriverWait(driver, TimeWait).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".checkbox"))
        )
        # Scroll into view and click using JavaScript
        try:
            print(f"Checkbox displayed: {checkbox.is_displayed()}, enabled: {checkbox.is_enabled()}")

            driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
            driver.execute_script("arguments[0].click();", checkbox)
            print("Checkbox clicked successfully using JavaScript.")
        except Exception as e:
            print(f"Failed to click checkbox using JavaScript: {e}")
    except Exception as e:
        print(f"Failed to handle the checkbox: {e}")
        driver.quit()
        return
    
    # Handle the "Aceptar" button
    try:
        # Wait for the "Aceptar" button to be clickable and click it
        accept_button = WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "enable-btn"))
        )
        print(f"'Aceptar' button displayed: {accept_button.is_displayed()}, enabled: {accept_button.is_enabled()}")
        driver.execute_script("arguments[0].scrollIntoView(true);", accept_button)
        driver.execute_script("arguments[0].click();", accept_button)
        print(f"'Aceptar' button clicked successfully using  JavaScript.")
    except TimeoutException:
        print(f"Failed to handle the 'Aceptar button: {e}")
        driver.quit()
        return
    print("Terms accepted successfully...")
    
    print("Starting to download the variables.")
    download_hydrometeorological_data(driver, path, variable, param, departamento, code, date_ini, date_fin, retries=1)
    driver.quit()

