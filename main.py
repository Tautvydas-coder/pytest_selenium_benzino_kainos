from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from resources import mail_credentials
from services.webdriver_service import driver_service
from selenium.webdriver.support.select import Select
from resources.variables import *

# TODO prisukti pytest

driver = driver_service()
# driver.get('chrome://settings/clearBrowserData')


def open_website():
    driver.implicitly_wait(5)
    driver.get(GAS_PRICE_URL)


def choose_city():
    select_element = driver.find_element(By.ID, 'city')
    select_object = Select(select_element)
    select_object.select_by_visible_text(CITY)


def press_button():
    driver.find_element(By.XPATH, FIND_BUTTON).click()


def fetch_address_and_price():
    main = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, PRICE_TABLE))
    )
    rows_table = main.find_elements(By.TAG_NAME, "tr")
    list_of_address_prices = []
    for row_table in rows_table:
        columns = row_table.find_elements(By.TAG_NAME, "td")
        list_of_address_prices.append((columns[2].text, columns[4].text))
    list_of_address_prices.sort(key=lambda i: i[1])
    address_and_price_tuple = list(filter(lambda x: x[1] != ("-" or "A95"), list_of_address_prices))[0]
    address_and_price_string = ' '.join(address_and_price_tuple)
    return address_and_price_string


def open_new_tab():
    driver.switch_to.new_window('tab')


def goto_gmail_web():
    driver.get(GMAIL_LOGIN_URL)


def input_login_name(login_name: str):
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, BOX_LOGIN_NAME))
    ).send_keys(login_name)
    driver.find_element(By.XPATH, LOGIN_NAME_BUTTON_NEXT).click()


def input_login_password(login_password: str):
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable(
            (By.XPATH, BOX_LOGIN_PASSWORD))
    ).send_keys(login_password)
    driver.find_element(By.XPATH, LOGIN_PASSWORD_BUTTON_NEXT).click()


def create_letter():
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable(
            (By.XPATH, CREATE_LETTER_BUTTON))
    ).click()


def input_sender_email(sender_mail: str):
    sender_address = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, EMAIL_TO_SEND_BOX))
    )
    ActionChains(driver).click(sender_address).send_keys(sender_mail).perform()
    ActionChains(driver).click(sender_address).send_keys(Keys.ENTER).perform()


def input_letter(address_and_price: str):
    mail_content = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    EMAIL_TEXT_FIELD))
    )
    ActionChains(driver).move_to_element(mail_content).click(mail_content).send_keys(address_and_price).perform()


def send_email():
    button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH,
                                    GMAIL_SEND_BUTTON))
    )
    ActionChains(driver).move_to_element(button).click().perform()


if __name__ == '__main__':
    open_website()
    choose_city()
    press_button()
    address_price = fetch_address_and_price()
    open_new_tab()
    goto_gmail_web()
    email_name = mail_credentials.email_name()
    email_password = mail_credentials.email_password()
    input_login_name(email_name)
    input_login_password(email_password)
    create_letter()
    input_sender_email(email_name)
    input_letter(address_price)
    send_email()
    # driver.close()
