from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chromedriver_binary

def configure_chrome_driver(download_dir):
    chrome_options = Options()
    chrome_prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", chrome_prefs)

    # # Add headless mode and other options: only with container
    # chrome_options.add_argument("--headless")  # Run in headless mode,
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--remote-debugging-port=9222")  # Enable remote debugging

    # Set the path to Chromium binary
    #chrome_options.binary_location = "/usr/bin/chromium" #only with container
    #service = Service('/usr/bin/chromedriver')  #only with container

    # Use chromedriver_binary to set the correct ChromeDriver path
    service = Service(chromedriver_binary.chromedriver_filename)
    print(chromedriver_binary.chromedriver_filename)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(1200)
    return driver