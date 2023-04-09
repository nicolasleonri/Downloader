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
from selenium.webdriver.common.action_chains import ActionChains

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

    # Closes cookies:
    driver.find_element(
        By.XPATH, "//button[@id='CybotCookiebotDialogBodyButtonDecline']").click()

    browser.find_element(By.XPATH, "//button[@class='btn btn-login']").click()
    browser.find_element(By.XPATH, "//a[@class='btn btn-library']").click()
    browser.find_element(
        By.XPATH, "//input[@placeholder='Search Libraries and Groups']").click()
    browser.find_element(
        By.XPATH, "//input[@placeholder='Search Libraries and Groups']").send_keys("verbund")
    time.sleep(2)
    browser.find_element(By.XPATH, "//div[@class='title']").click()
    time.sleep(2)
    browser.find_element(By.XPATH, "//button[@class='btn btn-action']").click()

    browser.switch_to.window(driver.window_handles[1])

    browser.find_element(
        By.XPATH, "//input[@id='L#AUSW']").send_keys(str(username))
    browser.find_element(
        By.XPATH, "//input[@id='LPASSW']").send_keys(str(password))
    browser.find_element(
        By.XPATH, "//input[@id='LPASSW']").send_keys(Keys.RETURN)
    time.sleep(7)


def write_to_txt_results(input):
    with open(r'final_list.txt', 'w') as fp:
        for item in input:
            fp.write("%s\n" % item)
        print('Done')


def write_to_txt_errors(input):
    with open(r'errors.txt', 'w') as fp:
        for item in input:
            fp.write("%s\n" % item)
        print('Done')


def click_spanish(browser):
    browser.find_element(By.XPATH, "//a[@class='btn btn-underline']").click()
    time.sleep(10)
    return True


def check_number(browser):
    try:
        browser.find_element(
            By.XPATH, "//li[@id='thumbsToolbarBottom_0']").click()
    except Exception as e:
        print(f'error while opening url - {e}')
        return False, 0

    time.sleep(2)

    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    elements = soup.find_all("a", attrs={"page-number": True, "href": True})

    for element in elements:
        output = element['page-number']

    browser.find_element(By.XPATH, "//li[@id='thumbsToolbarBottom_0']").click()

    return True, int(output)


### Goes to website and logs in###
driver = initiate_driver()
login(driver)
driver.switch_to.window(driver.window_handles[0])

### Go to website and get links to download####
spanish_clicked = False
final_list = []
errors = []
url = "https://www.pressreader.com/peru/diario-trome/"


for year in range(2022, 2023, 1):

    for month in range(1, 13, 1):

        for day in range(1, 32, 1):

            page_number_checked = False
            df_links = pd.DataFrame()

            for page in range(1, 51, 2):

                extension = str(
                    str(year)+str(f"{int(month):02d}")+str(f"{int(day):02d}")+"/page/"+str(page))
                url_todownload = url + extension

                try:
                    driver.get(str(url_todownload))
                except Exception as e:
                    print(f'error while opening url - {e}')
                    break

                if spanish_clicked == False:
                    spanish_clicked = click_spanish(driver)
                else:
                    time.sleep(5)

                if page_number_checked == False:
                    page_number_checked, number_of_pages = check_number(driver)
                else:
                    pass

                if page > number_of_pages:
                    print("Finished!", str(url_todownload))
                    break

                img_list = []

                if len(driver.find_elements(By.TAG_NAME, "img")) == 0:
                    continue

                for element in driver.find_elements(By.TAG_NAME, "img"):
                    img_list.append(str(element.get_attribute('src')))

                link_list = []

                for idx, val in enumerate(img_list):
                    if ".co/" in val and "nd_id" not in val:
                        link_list.append(val)

                df = pd.DataFrame()

                for idx, val in enumerate(link_list):
                    df_toadd = pd.DataFrame([val.split("&")])

                    df = pd.concat([df, df_toadd], axis=0,
                                   join="outer", copy=True)

                if len(df) == 0:
                    continue

                #print(df)

                try:
                    df.drop_duplicates(
                        subset=df.iloc[:, [3]], keep="last", inplace=True)
                except Exception as e:
                    print(f'error while droping - {e}')
                    errors.append(str(url_todownload))
                    write_to_txt_errors(errors)
                    continue

                df.reset_index()

                df_links = pd.concat(
                    [df_links, df], axis=0, join="outer", copy=True)
                
                print(len(df_links))
                #print(df_links)

            try:
                df_links.drop_duplicates(
                    subset=df_links.iloc[:, [3]], keep="last", inplace=True)
            except Exception as e:
                print(f'error while droping duplicates - {e}')
                continue

            #df_links = df_links.rename(columns={df_links.columns[0]: "http", df_links.columns[1]: "page-number", df_links.columns[2]: "scale", df_links.columns[3]: "layer", df_links.columns[4]: "token", })
            df_links = df_links.rename(columns={df_links.columns[0]: "http", df_links.columns[1]: "page-number", df_links.columns[2]: "scale", df_links.columns[3]: "token",})

            df_links["scale"] = 'scale=172'
            df_links["layer"] = 'layer=fg'
            df_links = df_links.fillna('')

            df_links[['page', 'number']
                     ] = df_links["page-number"].str.split('=', 1, expand=True)
            df_links = df_links.sort_values(by=["number"])
            df_links.reset_index()

            df_links["result"] = df_links["http"] + "&" + df_links["page-number"] + \
                "&" + df_links["scale"] + "&" + \
                df_links["layer"] + "&" + df_links["token"]

            final_list = final_list + df_links["result"].values.tolist()
            write_to_txt_results(final_list)

            print("Length final_list:", len(final_list))
