from time import sleep

import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture()
def main_page():
    driver = webdriver.Chrome()
    driver.get("https://localhost:2443")
    wait = WebDriverWait(driver, 10)

    # Обход незащищенного подключения
    driver.find_element(By.XPATH, "//button[@id='details-button']").click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//a[@id='proceed-link']"))).click()
    return driver

def test_correct_sign_in(main_page):
    login = main_page.find_element(By.XPATH, "//input[@id='username']")
    password = main_page.find_element(By.XPATH, "//input[@id='password']")
    login_btn = main_page.find_element(By.XPATH, "//button[@data-test-id='login-button-submit']")
    login.send_keys('root')
    password.send_keys('0penBmc')
    login_btn.click()


def test_incorrect_sign_in(main_page):
    login = main_page.find_element(By.XPATH, "//input[@id='username']")
    password = main_page.find_element(By.XPATH, "//input[@id='password']")
    login_btn = main_page.find_element(By.XPATH, "//button[@data-test-id='login-button-submit']")
    login.send_keys('root1')
    password.send_keys('0penBmc')
    login_btn.click()



