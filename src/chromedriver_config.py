# ##--------- Please, use it only to test in local -----------##
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service

# def configure_chrome_driver(download_dir):
#     chrome_options = Options()

#     chrome_prefs = {
#         "download.default_directory": download_dir,
#         "download.prompt_for_download": False,
#         "download.directory_upgrade": True,
#         "safebrowsing.enabled": True,
#         "safebrowsing.disable_download_protection": True,
#         "profile.default_content_settings.popups": 0,
#         "profile.default_content_setting_values.automatic_downloads": 1,
#         "profile.default_content_setting_values.notifications": 2
#     }
#     chrome_options.add_argument("--safebrowsing-disable-download-protection")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--disable-extensions")
#     chrome_options.add_argument("--disable-popup-blocking")

#     driver = webdriver.Chrome(options=chrome_options)
#     driver.set_page_load_timeout(600)
#     return driver
##------------- Headless mode, Container CI -------------##
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def configure_chrome_driver(download_dir):
    chrome_options = Options()
    chrome_prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "safebrowsing.disable_download_protection": True,
        "profile.default_content_setting_values.popups": 0,
        "profile.default_content_setting_values.automatic_downloads": 1,
        "profile.default_content_setting_values.notifications": 2
    }

    chrome_options.add_experimental_option("prefs", chrome_prefs)

    # Headless + stability for CI
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--user-data-dir=/tmp/chrome-user-data")
    chrome_options.add_argument("--safebrowsing-disable-download-protection")
    chrome_options.add_argument("--safebrowsing-disable-extension-blacklist")


    # Needed for seleniarm image
    chrome_options.binary_location = "/usr/bin/chromium"

    # Use local chromedriver (already in seleniarm container)
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(600)
    return driver
