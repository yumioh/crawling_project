from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from dotenv import load_dotenv
import os

#load .env
load_dotenv()
id = os.environ.get('TWITTER_ID')
pw = os.environ.get('TWITTER_PW')
email = os.environ.get('TWITTER_EMAIL')


options=Options()
options.add_experimental_option('detach', True) #브라우저 바로꺼짐 방지

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get('https://twitter.com/i./flow/login')
driver.implicitly_wait(10)

driver.find_element(By.CSS_SELECTOR, "input.r-30o5oe").send_keys(email)
time.sleep(1)
driver.find_elements(By.CSS_SELECTOR, ".css-901oao.css-16my406.r-poiln3")[8].click()
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, "input.r-30o5oe").send_keys(id)
time.sleep(1)
driver.find_elements(By.CSS_SELECTOR, "span.css-901oao")[6].click()
time.sleep(1)
driver.find_elements(By.CSS_SELECTOR, "input.r-30o5oe")[1].send_keys(pw)
time.sleep(1)
driver.find_elements(By.CSS_SELECTOR, ".css-901oao.css-16my406.r-poiln3")[13].click()
time.sleep(1)

for cookie in driver.get_cookies():
    print(cookie['name'])
    print(cookie['value'])