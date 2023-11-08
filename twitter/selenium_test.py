from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

options=Options()
options.add_experimental_option('detach', True) #브라우저 바로꺼짐 방지

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get('https://n.news.naver.com/mnews/article/119/0002766828?sid=105')
driver.implicitly_wait(10)

print(driver.find_element(By.CSS_SELECTOR, "h2#title_area").text)

for li in driver.find_elements(By.CSS_SELECTOR, "li.u_likeit_list"):
    print(li.find_element(By.CSS_SELECTOR, ".u_likeit_list_name").text)
    print(li.find_element(By.CSS_SELECTOR, ".u_likeit_list_count").text)

driver.find_element(By.CSS_SELECTOR, ".Nicon_search").click()
driver.find_element(By.CSS_SELECTOR, "._search_input").send_keys("지드래곤")
driver.find_element(By.CSS_SELECTOR, "._total_search_btn").click()

time.sleep(10)