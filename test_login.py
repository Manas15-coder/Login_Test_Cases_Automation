import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

# Parameterizing the test with combinations of username, password, and pin
@pytest.mark.parametrize(
    "username_input, password_input, pin_input, expected_url",
    [
        ("1038636","orbis@123","2002","https://dstradeuat.dhanistocks.com/home/dashboard"),#all correct
        ("1038636","Orbis@123","2002","https://dstradeuat.dhanistocks.com/home/dashboard"),#wrong password
        ("1038637","orbis@123","2002","https://dstradeuat.dhanistocks.com/home/dashboard"),#wrong username
        ("1038636", "orbis@123", "2003","https://dstradeuat.dhanistocks.com/home/dashboard"),#wrong pin

    ]
)
def test_login_combinations(driver, username_input, password_input, pin_input, expected_url):
    driver.get('https://dstradeuat.dhanistocks.com/base/login')

    time.sleep(2)

    # Locate and input the username
    username = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/center/div/div/div[1]/div/div[2]/div[1]/input')
    username.clear()
    username.send_keys(username_input)

    # Locate and input the password
    password = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/center/div/div/div[1]/div/div[2]/div[2]/input')
    password.clear()
    password.send_keys(password_input)

    # Locate and input the pin
    pin = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/center/div/div/div[1]/div/div[2]/div[3]/div[2]/input')
    pin.clear()
    pin.send_keys(pin_input)

    # Click the login button
    login_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/center/div/div/div[1]/div/div[2]/button')
    time.sleep(2)
    login_btn.click()

    # Wait for the page to load and verify the URL
    time.sleep(5)
    current_url = driver.current_url

    # Validate the URL based on input combinations
    try:
        assert current_url == expected_url, f"Expected URL {expected_url}, but got {current_url}"
        print(f"Login test passed for username: {username_input}, password: {password_input}, pin: {pin_input}")
    except AssertionError as e:
        driver.save_screenshot(f'Login_failure_{username_input}_{password_input}_{pin_input}.png')
        pytest.fail(f"Test failed for username: {username_input}, password: {password_input}, pin: {pin_input} - {str(e)}")
