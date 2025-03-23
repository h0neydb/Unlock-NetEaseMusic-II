# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00836B5835824FABBA5B2513F318EC49A41E04C89B12FD34305260CA2FDC8603303F84C337788F9FBECB53D104413B122667F2C9E67718E50B194A8AE03BB5B7DA67983704E34654A736960CDA745A3151B039B1F559CB122211D9275CA4D8BC5CFF22D9DE46DB0150B90AF41004DA5BEC691CEAB88051E40D1F36CD5C8BDAC10ADA000C4AFD28D707BE9BA92BD3EE8E1F472BCA7C01B342140F09B7663F4129ABC81CD95C7CD5E3C1C60FA7402121713BBE3E20599A43429F15022EB3B835A57F324A4831664FD40490BFC62FFBA46C74674F4A5B74C6AAE56D22CFCAFE281D97E68B360682BE9CA475386C46F0F5F2BD37432B594C42FBB35E5EA0BA81D810F35EE96C122E15EB92BF6B699C99FBEC27F40B37983211903B5FBB3DB858C016CB0CB99FBC3EE55207681A9E958DE68352481597CB51C85E9AF1C7700C21B2ABFADF83C6187AB094D2AEA639ECB1FB627CD9B3E6C1B37A14633B5DF6C369798158"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
