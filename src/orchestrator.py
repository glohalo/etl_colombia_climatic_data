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
   # FileNotFoundError,
    NoSuchWindowException,
    UnexpectedAlertPresentException,
    SessionNotCreatedException
)
from zipfile import ZipFile
import sys
sys.path.append(os.path.abspath(os.path.join('..')))
from src.variables import Variables
from src.data_extraction import handle_terms_and_conditions_and_download
from src.preprocessing import filtering_data
import logging
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#configuring_path
file_path = "/Users/gloriacarrascal/master/research_data/dm_project/data/bronze/report.zip"
output_path_bronze = "/Users/gloriacarrascal/master/research_data/dm_project/data/bronze/"
output_path_silver = "/Users/gloriacarrascal/master/research_data/dm_project/data/silver/"
current = datetime.today()
_= current - timedelta(days = 20)
formated_fin_time = _.strftime("%d/%m/%Y")

# # Retry loop
# while True:
#     try:
#         handle_terms_and_conditions_and_download(
#             path="/Users/gloriacarrascal/master/research_data/dm_project/data/bronze",
#             variable="Temperatura",
#             param='Temperatura máxima diaria',
#             departamento="Atlantico",
#             code="29035080",
#             date_ini="01/01/2000",
#             date_fin=formated_fin_time
#         )
#         break
#     except (ElementNotInteractableException, NoSuchElementException, TimeoutException, ElementClickInterceptedException):

#             logging.warning("Retrying...")
#     except (FileNotFoundError, NoSuchWindowException, UnexpectedAlertPresentException):
#         logging.warning("No Data")
#         break
#     except SessionNotCreatedException as e:
#         logging.error(f"Session not created: {e}")
#         break

# filtering_data(output_path_bronze, output_path_silver, file_path)
def main():
    # Retry loop
    while True:
        try:
            handle_terms_and_conditions_and_download(
                path="/Users/gloriacarrascal/master/research_data/dm_project/data/bronze",
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

    filtering_data(output_path_bronze, output_path_silver, file_path)

if __name__ == "__main__":
    main()