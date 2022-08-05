from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FoxService

CHROME_DRIVER_PATH = "drivers/chromedriver.exe"
FFOX_DRIVER_PATH = "drivers/geckodriver.exe"


def driver_service():
    # ser = Service(CHROME_DRIVER_PATH)
    ser = FoxService(FFOX_DRIVER_PATH)
    # driver = webdriver.Chrome(service=ser)
    driver = webdriver.Firefox(service=ser)
    return driver
