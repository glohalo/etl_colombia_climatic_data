import logging
from datetime import timedelta, datetime
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException,
    NoSuchWindowException,
    UnexpectedAlertPresentException,
    SessionNotCreatedException
)
from extraction import DHIME_Download

# Extract data
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
    # except (ElementNotInteractableException, NoSuchElementException, TimeoutException, ElementClickInterceptedException):
    #     print("Retrying...")
    # except (FileNotFoundError, NoSuchWindowException, UnexpectedAlertPresentException):
    #     print("No Data")
    #     break
    except (ElementNotInteractableException, NoSuchElementException, TimeoutException, ElementClickInterceptedException):

            logging.warning("Retrying...")
    except (FileNotFoundError, NoSuchWindowException, UnexpectedAlertPresentException):
        logging.warning("No Data")
        break
    except SessionNotCreatedException as e:
        logging.error(f"Session not created: {e}")
        break