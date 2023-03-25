import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.core.utils import read_version_from_cmd, PATTERN

#### FUNCTIONS#####


def initiate_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    service = ChromeService(executable_path=ChromeDriverManager().install())
    browser = webdriver.Chrome(options=options, service=service)

    browser.maximize_window()
    browser.implicitly_wait(10)
    return browser


def login(browser, username="58983917609", password="22081997"):
    browser.get("https://www.pressreader.com/catalog")
    time.sleep(5)

    browser.find_element(By.XPATH, "//button[@class='btn btn-login']").click()
    browser.find_element(By.XPATH, "//a[@class='btn btn-library']").click()
    browser.find_element(
        By.XPATH, "//input[@placeholder='Search Libraries and Groups']").click()
    browser.find_element(
        By.XPATH, "//input[@placeholder='Search Libraries and Groups']").send_keys("verbund")
    time.sleep(2)
    browser.find_element(By.XPATH, "//div[@class='title']").click()
    browser.find_element(By.XPATH, "//button[@class='btn btn-action']").click()

    browser.switch_to.window(driver.window_handles[1])

    browser.find_element(
        By.XPATH, "//input[@id='L#AUSW']").send_keys(str(username))
    browser.find_element(
        By.XPATH, "//input[@id='LPASSW']").send_keys(str(password))
    browser.find_element(
        By.XPATH, "//input[@id='LPASSW']").send_keys(Keys.RETURN)
    time.sleep(5)


### Goes to website and logs in###
driver = initiate_driver()
login(driver)
driver.switch_to.window(driver.window_handles[0])
driver.find_element(
    By.XPATH, "//button[@id='CybotCookiebotDialogBodyButtonDecline']").click()

### Go to website and get links to download####
url = "https://www.pressreader.com/peru/diario-trome/"

spanish_clicked = False

for year in range(2023, 2024, 1):
    year = str(year)

    for month in range(1, 13, 1):
        month = int(month)

        for day in range(1, 32, 1):
            day = int(day)

            number_checked = False
            number_of_pages = 0

            df_links = pd.DataFrame()

            for page in range(1, 51, 2):
                page = int(page)

                extension = str(
                    str(year)+str(f"{month:02d}")+str(f"{day:02d}")+"/page/"+str(page))
                url_todownload = url + extension

                try:
                    driver.get(str(url_todownload))
                except Exception as e:
                    print(f'error while open url - {e}')
                    break

                if spanish_clicked == False:
                    driver.find_element(
                        By.XPATH, "//a[@class='btn btn-underline']").click()
                    spanish_clicked = True
                    time.sleep(10)
                else:
                    time.sleep(5)

                if number_checked == False:
                    driver.find_element(
                        By.XPATH, "//li[@id='thumbsToolbarBottom_0']").click()
                    time.sleep(2)

                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')

                    elements = soup.find_all(
                        "a", attrs={"page-number": True, "href": True})

                    for element in elements:
                        number_of_pages = element['page-number']

                    number_checked = True
                else:
                    pass

                # if page > int(number_of_pages):
                if page > 6:
                    print("Finished")
                    break

                img_list = []

                for element in driver.find_elements(By.TAG_NAME, "img"):
                    img_list.append(str(element.get_attribute('src')))

                link_list = []

                for idx, val in enumerate(img_list):
                    if ".co/" in val:
                        link_list.append(val)

                df = pd.DataFrame()

                for idx, val in enumerate(link_list):
                    df_toadd = pd.DataFrame([val.split("&")])
                    df = pd.concat([df, df_toadd], axis=0,
                                   join="outer", copy=True)

                df.drop_duplicates(
                    subset=df.iloc[:, [4]], keep="last", inplace=True)
                df.reset_index()

                df_links = pd.concat(
                    [df_links, df], axis=0, join="outer", copy=True)
                print(len(df_links))

            df_links.drop_duplicates(
                subset=df_links.iloc[:, [4]], keep="last", inplace=True)

            df_links = df_links.rename(columns={df_links.columns[0]: "http", df_links.columns[1]: "page-number",
                                       df_links.columns[2]: "scale", df_links.columns[3]: "layer", df_links.columns[4]: "token", })

            df_links["scale"] = 'scale=172'
            df_links["layer"] = 'layer=fg'
            df_links = df_links.fillna('')

            df_links[['page', 'number']] = df_links["page-number"].str.split('=', 1, expand=True)
            df_links = df_links.sort_values(by=["number"])
            df_links.reset_index()

            df_links["result"] = df_links["http"] + "&" + df_links["page-number"] + "&" + df_links["scale"] + "&" + df_links["layer"] + "&" + df_links["token"]
            
            final_list = df_links["result"].values.tolist()

            for idx, val in enumerate(final_list):
                print(idx, val)

            ##ToDO: download final list and save it in directory
