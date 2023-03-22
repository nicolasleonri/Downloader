import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import read_version_from_cmd, PATTERN
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import pandas as pd


def initiate_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options, service=service)
    driver.maximize_window()
    driver.implicitly_wait(10)

    return driver

driver = initiate_driver()
driver.get("https://www.pressreader.com/catalog")
time.sleep(5)

driver.find_element(By.XPATH, "//button[@class='btn btn-login']").click()
driver.find_element(By.XPATH, "//a[@class='btn btn-library']").click()
driver.find_element(By.XPATH, "//input[@placeholder='Search Libraries and Groups']").click()
driver.find_element(By.XPATH, "//input[@placeholder='Search Libraries and Groups']").send_keys("verbund")
time.sleep(2)
driver.find_element(By.XPATH, "//div[@class='title']").click()
driver.find_element(By.XPATH, "//button[@class='btn btn-action']").click()

driver.switch_to.window(driver.window_handles[1])

driver.find_element(By.XPATH, "//input[@id='L#AUSW']").send_keys("58983917609")
driver.find_element(By.XPATH, "//input[@id='LPASSW']").send_keys("22081997")
driver.find_element(By.XPATH, "//input[@id='LPASSW']").send_keys(Keys.RETURN)
time.sleep(5)

driver.switch_to.window(driver.window_handles[0])
driver.get("https://www.pressreader.com/peru/diario-trome/20230321/page/1")
time.sleep(5)

driver.find_element(By.XPATH, "//a[@class='btn btn-underline']").click()
time.sleep(10)

#html = driver.page_source

img_list = []
for element in driver.find_elements(By.TAG_NAME, "img"):
    img_list.append(str(element.get_attribute('src')))

link_list = []
for idx, val in enumerate(img_list):
    if ".co/" in val:
        link_list.append(val)

df = pd.DataFrame()

for idx, val in enumerate(link_list):
    #print(idx, val)
    #print(val.split("&"))
    df_toadd = pd.DataFrame([val.split("&")])
    df = pd.concat([df, df_toadd], axis = 0, join = "outer", copy = True)

df.drop_duplicates(subset=df.iloc[:,[4]], keep = "last", inplace = True)
df.reset_index()
print(df)

#driver.find_element(By.XPATH, "//*[@id='thumbsToolbarBottom_0']").click()


#page_list = driver.find_elements(By.XPATH, "//a[@href='javascript:void(0)']")

#print(len(page_list))


#print(html)


#https://t.prcdn.co/img?file=eag82023032100000000001001&page=1&scale=120&layer=fg








##################################

trome = "https://t.prcdn.co/img?file=eag82023032100000000001001&page=1&scale=94&layer=fg"
elcomercio = "https://t.prcdn.co/img?file=eaaj2023032100000000001001&page=1&scale=177"

for year in range(2023, 2024, 1):
    year = str(year)

    for month in range(1,13,1):
        month = int(month)

        for day in range(1, 32,1):
            day = int(day)

            #print(year+str(f"{month:02d}")+str(f"{day:02d}"))

            
path = "https://www.pressreader.com/catalog"

