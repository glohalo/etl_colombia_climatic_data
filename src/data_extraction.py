import time
import logging
import os
import subprocess
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from zipfile import ZipFile
import sys
sys.path.append(os.path.abspath(os.path.join('..')))

from src.variables import Variables
from src.chromedriver_config import *

#driver = webdriver.Chrome()

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

import logging
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def variable_deparment_and_date_set_up(driver, path, variable, param, departamento, code, date_ini, date_fin, retries=3):
    TimeWait = 40

    for attempt in range(retries):
        try:
            logging.info(f"Attempt {attempt + 1}: Starting hydrometeorological data download process.")
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
                logging.info(f"Varible {variable} written perfectly!") 
            except TimeoutException:
                logging.error("TimeoutException: Failed to find the variable dropdown or options.")
                continue
            except NoSuchElementException:
                logging.error("NoSuchElementException: Failed to find the variable dropdown or options.")
                continue
            except ElementNotInteractableException:
                logging.error("ElementNotInteractableException: The variable dropdown or options are not interactable.")
                continue
            except Exception as e:
                logging.error(f"Failed to select variable: {e}")
                continue
                logging.info(f"Starting to filter: {param}")

            try:
                # Enter the parameter name
                time.sleep(10)
                code_input = WebDriverWait(driver, TimeWait).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="search"]'))
                )
                code_input.send_keys(param)
                logging.info(f"Parameter wrote: {param}")
                                # Scroll down to make sure the checkbox is visible
                scroll_down(driver, TimeWait)

                # Locate and select the checkbox with the paramater
                time.sleep(10)
                checkbox = WebDriverWait(driver, TimeWait).until(
                    EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{param}')]/preceding-sibling::td/input"))
                )
                driver.execute_script("arguments[0].click();", checkbox)
                logging.info(f"Selected checkbox for parameter variable: {param}")

            except Exception as e:
                logging.error(f"Failed to select parameter {param}. Error: {e}")
                continue

            logging.info("Step 4: Selecting department.") 
            time.sleep(10)
            dept_dropdown = WebDriverWait(driver, TimeWait).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="first"]/table/tbody/tr[1]/td[2]/span/span/span[1]')) #//*[@id="first"]/table/tbody/tr[1]/td[2]/span/span/span[1] #//*[@id="first"]/table/tbody/tr[1]/td[2]/span'
            )
            driver.execute_script("arguments[0].click();", dept_dropdown)
            time.sleep(10)
            dept_option = WebDriverWait(driver, TimeWait).until(
                EC.element_to_be_clickable((By.XPATH, f"//ul[@aria-hidden='false']//li[text()='{departamento}']"))
            )
            driver.execute_script("arguments[0].click();", dept_option)
            logging.info(f"Selected department: {departamento}")

            # Click the "Filtrar" button
            time.sleep(10)
            scroll_down(driver, TimeWait)
            logging.info("Clicking the 'Filtrar' button.") 
            filtrar_button = WebDriverWait(driver, TimeWait).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="first"]/div[3]/div'))  
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", filtrar_button)
            driver.execute_script("arguments[0].click()", filtrar_button)
            logging.info("Clicked the 'Filtrar' button.")

            time.sleep(10)
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
            # Set date range
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

            # Select next 
            logging.info("Step 8: Agregar la consulta")
            time.sleep(2)
            button = WebDriverWait(driver, TimeWait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="first"]/div[6]/div[1]')))
            button.click()
            time.sleep(10)
            # Select the format to download the data/CSV
            logging.info("Step 9: Select CSV format.")
            time.sleep(10)
            WebDriverWait(driver, TimeWait).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="OptionCSV"]'))
            ).click()
            logging.info("Starting download button sequence")
            time.sleep(10)
            # Download button sequence
            WebDriverWait(driver, TimeWait).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="second"]/div/div[4]/div[1]'))
            ).click()
            time.sleep(15)
            logging.info("Handle terms and conditions")#//*[@id="dijit_form_Button_2_label"]
            download_button = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="dijit_form_Button_2_label"]'))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
            time.sleep(1)  # Wait for the element to be fully visible
            # try:
            #     download_button = WebDriverWait(driver, 60).until(
            #         EC.element_to_be_clickable((By.XPATH, '//*[@id="dijit_form_Button_2_label"]'))
            #     )
            #     logging.info("Button is clickable.")
            # except Exception as e:
            #     logging.error(f"Button is not clickable: {e}")
            #     driver.save_screenshot("/src/data/button_not_clickable.png")
            #     raise
            # driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
            # time.sleep(1)  # Wait for the element to be fully visible
            # driver.execute_script("arguments[0].click();", download_button)
            # logging.info("Button clicked using JavaScript.")
            # download_button = WebDriverWait(driver, TimeWait).until(
            #     EC.element_to_be_clickable((By.XPATH, '//*[@id="dijit_form_Button_2_label"]'))
            # )
            
            time.sleep(10)
            logging.info("Terms and conditions accepted successful...")
            download_button.click()
            logging.info("Download initiated.")
            driver.close()
            return  
        except Exception as e:
            logging.warning(f"Attempt {attempt + 1} failed. Retrying... Error: {e}")
            time.sleep(2)
    logging.error("Max retries reached. Failed to complete the download process.")
    raise Exception("Max retries reached. Failed to complete the download process.")

def handle_accept_button(driver, TimeWait):
    # Handle the "Aceptar" button
    try:
        # Wait for the "Aceptar" button to be clickable and click it
        accept_button = WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "enable-btn"))
        )
        print(f"'Aceptar' button displayed: {accept_button.is_displayed()}, enabled: {accept_button.is_enabled()}")
        driver.execute_script("arguments[0].scrollIntoView(true);", accept_button)
        driver.execute_script("arguments[0].click();", accept_button)
        print(f"'Aceptar' button clicked successfully using JavaScript.")
    except TimeoutException as e:
        print(f"Failed to handle the 'Aceptar button: {e}")
        driver.quit()
        return False
    print("Terms accepted successfully...")
    return True
def handle_terms_and_conditions(driver, TimeWait):
    # Handle the checkbox for terms and conditions
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
            return False
    except Exception as e:
        print(f"Failed to handle the checkbox: {e}")
        return False
    return True
# def configure_chrome_driver(download_dir):
#     chrome_options = Options()
#     chrome_prefs = {
#         "download.default_directory": download_dir,
#         "download.prompt_for_download": False,
#         "download.directory_upgrade": True,
#         "safebrowsing.enabled": True
#     }
#     chrome_options.add_experimental_option("prefs", chrome_prefs)
#     service = Service('/usr/local/bin/chromedriver')  
#     driver = webdriver.Chrome(service=service, options=chrome_options)
#     driver.set_page_load_timeout(180)
#     return driver

def handle_terms_and_conditions_and_download(path, variable, param, departamento, code, date_ini, date_fin):
    print("Initializing the Chrome driver...")
    driver =  configure_chrome_driver(path)
    #driver = webdriver.Chrome()
    driver.get("http://dhime.ideam.gov.co/atencionciudadano/")
    TimeWait = 60

    if not handle_terms_and_conditions(driver, TimeWait):
        driver.quit()
        return

    if not handle_accept_button(driver, TimeWait):
        driver.quit()
        return

    print("Starting to download the variables.")
    variable_deparment_and_date_set_up(driver, path, variable, param, departamento, code, date_ini, date_fin, retries=1)
    driver.quit()
