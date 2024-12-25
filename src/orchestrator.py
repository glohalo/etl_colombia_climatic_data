import time
import os
import subprocess
import pandas as pd

import variables
import extraction
import preprocessing
from preprocessing import filtering_data
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
from variables import Variables
from extraction import DHIME_Download

import logging
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
current = datetime.today()
_= current - timedelta(days = 20)
formated_fin_time = _.strftime("%d/%m/%Y")

# Retry loop
while True:
    try:
        DHIME_Download(
            path="/Users/gloriacarrascal/master/research_data/dm_project/data/",
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

#define path
file_path = "/Users/gloriacarrascal/master/research_data/dm_project/data/bronze/report.zip"
output_path_bronze = "/Users/gloriacarrascal/master/research_data/dm_project/data/bronze/"
output_path_silver = "/Users/gloriacarrascal/master/research_data/dm_project/data/silver/"
filtering_data(output_path_bronze, output_path_silver, file_path)