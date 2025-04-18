import time
import os
import subprocess
import pandas as pd
from datetime import timedelta, datetime
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
import sys
sys.path.append(os.path.abspath(os.path.join('..')))
from variables import Variables
from data_extraction import handle_terms_and_conditions_and_download
from preprocessing import filtering_data
import logging
print("Chromium version:", subprocess.getoutput("chromium --version"))
print("Chromedriver version:", subprocess.getoutput("chromedriver --version"))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#configuring_path
#base_dir = os.path.abspath(os.path.join(os.getcwd(), '.', '..'))
base_dir = os.path.abspath(os.getcwd())
output_path_bronze = os.path.join(base_dir, 'data', 'bronze')
output_path_silver = os.path.join(base_dir, 'data', 'silver')
# Ensure the output directories exist
os.makedirs(output_path_bronze, exist_ok=True)
os.makedirs(output_path_silver, exist_ok=True)

# file_name = next((f for f in os.listdir(output_path_bronze) if f.endswith('.zip')), 'report.zip')
# file_path = os.path.join(output_path_bronze, file_name)
# print(file_path)
# Find the .zip file
file_name = next((f for f in os.listdir(output_path_bronze) if f.endswith('.zip')), None)

current = datetime.today()
_= current - timedelta(days = 20)
formated_fin_time = _.strftime("%d/%m/%Y")

def main():
    while True:
        try:
            handle_terms_and_conditions_and_download(
                path=output_path_bronze,
                variable="Temperatura",
                param='Temperatura máxima diaria',
                departamento="Atlantico",
                code="29035080",
                date_ini="01/01/2000",
                date_fin=formated_fin_time
            )
            break
        except (ElementNotInteractableException, NoSuchElementException, TimeoutException, ElementClickInterceptedException):
            logging.warning("Retrying...")
        except (FileNotFoundError, NoSuchWindowException, UnexpectedAlertPresentException):
            logging.warning("No Data")
            break
        except SessionNotCreatedException as e:
            logging.error(f"Session not created: {e}")
            break

    if file_name:
        old_path = os.path.join(output_path_bronze, file_name)
        new_path = os.path.join(output_path_bronze, 'report.zip')

        # Rename to standard name for the pipeline
        os.rename(old_path, new_path)
        file_path = new_path
        print(f"Renamed downloaded file to: {file_path}")

    filtering_data(output_path_bronze, output_path_silver, file_path)

if __name__ == "__main__":
    main()