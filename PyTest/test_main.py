import pytest
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from activate_driver.activate_drivers import *
from selenium.webdriver.support.select import Select
from resources.variables import *
from resources import mail_credentials
from selenium.webdriver.firefox.service import Service as FoxService
from resources.variables import CHROME_DRIVER_PATH, FFOX_DRIVER_PATH


# TODO prisukti PyTest
# six because six tests

@pytest.mark.six
def test_open_website():
    global driver
    driver = driver_service()
    driver.implicitly_wait(5)
    driver.maximize_window()
    driver.get(GAS_PRICE_URL)
    web_title = driver.title
    assert web_title == "Kuro kainos"


@pytest.mark.six
def test_choose_city():
    select_element = driver.find_element(By.ID, 'city')
    select_object = Select(select_element)
    select_object.select_by_visible_text(CITY)
    value = select_element.get_attribute("value")
    assert value == '1'


@pytest.mark.six
def test_press_button():
    button = driver.find_element(By.XPATH, FIND_BUTTON)
    name = button.get_attribute("value")
    button.click()
    assert name == "Ieškoti"


@pytest.mark.six
def test_fetch_address_and_price():
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
    assert isinstance(address_and_price_string, str)
    return address_and_price_string


@pytest.mark.six
def test_open_new_tab():
    driver.switch_to.new_window('tab')


@pytest.mark.six
def test_goto_gmail_web():
    driver.get(GMAIL_LOGIN_URL)
    gmail_title = driver.title
    assert gmail_title == "Gmail"


@pytest.mark.six
def test_input_login_name(login_name: str):
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, BOX_LOGIN_NAME))
    ).send_keys(login_name)
    driver.find_element(By.XPATH, LOGIN_NAME_BUTTON_NEXT).click()



# def test_input_login_password(login_password: str):
#     WebDriverWait(driver, 15).until(
#         EC.element_to_be_clickable(
#             (By.XPATH, BOX_LOGIN_PASSWORD))
#     ).send_keys(login_password)
#     driver.find_element(By.XPATH, LOGIN_PASSWORD_BUTTON_NEXT).click()
#
#
# def test_create_letter():
#     WebDriverWait(driver, 15).until(
#         EC.element_to_be_clickable(
#             (By.XPATH, CREATE_LETTER_BUTTON))
#     ).click()
#
#
# def test_input_sender_email(sender_mail: str):
#     sender_address = WebDriverWait(driver, 15).until(
#         EC.element_to_be_clickable(
#             (By.CLASS_NAME, EMAIL_TO_SEND_BOX))
#     )
#     ActionChains(driver).click(sender_address).send_keys(sender_mail).perform()
#     ActionChains(driver).click(sender_address).send_keys(Keys.ENTER).perform()
#
#
# def test_input_letter(address_and_price: str):
#     mail_content = WebDriverWait(driver, 15).until(
#         EC.element_to_be_clickable((By.CSS_SELECTOR,
#                                     EMAIL_TEXT_FIELD))
#     )
#     ActionChains(driver).move_to_element(mail_content).click(mail_content).send_keys(address_and_price).perform()
#
#
# def test_send_email():
#     button = WebDriverWait(driver, 15).until(
#         EC.element_to_be_clickable((By.XPATH,
#                                     GMAIL_SEND_BUTTON))
#     )
#     ActionChains(driver).move_to_element(button).click().perform()


# def test_teardown():
#     driver.close()
#     driver.quit()
#     print("Test Completed")

# if __name__ == '__main__':
#     test_open_website()
#     test_choose_city()
#     test_press_button()
#     address_price = test_fetch_address_and_price()
#     test_open_new_tab()
#     test_goto_gmail_web()
#     email_name = mail_credentials.email_name()
#     email_password = mail_credentials.email_password()
#     test_input_login_name(email_name)
#     test_input_login_password(email_password)
#     test_create_letter()
#     test_input_sender_email(email_name)
#     test_input_letter(address_price)
#     test_send_email()
#     test_teardown()
