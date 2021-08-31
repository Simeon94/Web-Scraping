from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions as exception
import json
import csv
import time

options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
options.add_argument('disable-infobars')

desired_capabilities = options.to_capabilities()

# driver to open a new browser and navigate it
driver = webdriver.Chrome(desired_capabilities=desired_capabilities)

page = 2

cars_data = []

for page in range(2, 10):

    URL = f"https://www.ebay.co.uk/b/Cars/9801/bn_1839037?page=%7Bpage%7D&_pgn={page}"
    driver.get(URL)
    time.sleep(3)
    cookies = driver.find_element_by_xpath('//button[@id="gdpr-banner-accept"]')
    cookies_click = driver.execute_script("arguments[0].click();", cookies)
    time.sleep(3)


    page_link_items = driver.find_element_by_xpath('//*[@id="mainContent"]')
    page_link = page_link_items.find_elements_by_xpath("./li")
    print(page_link)
    page_num = len(page_link)
    print(page_num)

    #while True:

    for page in range(page_num):

        time.sleep(5)
        # div_tag = driver.find_element_by_xpath('//div[@id="mainContent"]')
        try:

            wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='mainContent']")))
        except:
            driver.forward()

        #div_tag = driver.find_element_by_xpath("//div[@id='mainContent']")
        time.sleep(2)

        #section_tag = driver.find_element_by_xpath('//*[@id="s0-27_2-9-0-1[0]-0-1"]')
        ul_tag = driver.find_element_by_xpath('//*[@id="s0-27_1-9-0-1[0]-0-1"]/ul')
        cars = ul_tag.find_elements_by_xpath(".//li")
        car_numbers = len(cars)
        print(car_numbers)

        for j in range(car_numbers):

            # time.sleep(3)
            try:

                wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='mainContent']")))
            except:
                driver.forward()
            #section_tag = driver.find_element_by_xpath('//*[@id="s0-27_1-9-0-1[0]-0-1"]')
            ul_tag = section_tag.find_element_by_xpath('//*[@id="s0-27_1-9-0-1[0]-0-1"]/ul')
            car = ul_tag.find_elements_by_xpath("./li")[j]

            ActionChains(driver).move_to_element(car).click().perform()

            time.sleep(3)

            car_data = {"sale_price": [], "year": [], "fuel": [], "mileage": [], "condition": [], "location": [],
                        "contact_number": []}

            try:
                sale_price = driver.find_element_by_xpath('//*[@id="prcIsum"]').text
                car_data['sale_price'].append(sale_price)

            except NoSuchElementException:
                car_data['sale_price'].append(None)

            else:
                pass

            try:

                year = driver.find_element_by_xpath('//*[@id="viTabs_0_is"]/div/table/tbody/tr[1]/td[4]/span').text
                car_data['year'].append(year)

            except NoSuchElementException:
                car_data['year'].append(None)

            else:
                pass

            try:
                fuel = driver.find_element_by_xpath('//*[@id="viTabs_0_is"]/div/table/tbody/tr[6]/td[2]/span').text
                car_data['fuel'].append(fuel)

            except NoSuchElementException:
                car_data['fuel'].append(None)

            else:
                pass

            try:
                mileage = driver.find_element_by_xpath('//*[@id="viTabs_0_is"]/div/table/tbody/tr[2]/td[2]/span').text
                car_data['mileage'].append(mileage)

            except NoSuchElementException:
                car_data['mileage'].append(None)

            else:
                pass

            try:
                condition = driver.find_element_by_xpath('//*[@id="vi-itm-cond"]').text
                car_data['condition'].append(condition)

            except NoSuchElementException:
                car_data['condition'].append(None)

            else:
                pass

            try:
                loc_div_tag = driver.find_element_by_xpath('//*[@id="LeftSummaryPanel"]')
                loc_div2_tag = loc_div_tag.find_element_by_xpath('//*[@id="LeftSummaryPanel"]/div/form/div[9]')
                location = loc_div2_tag.find_element_by_xpath('//*[@id="LeftSummaryPanel"]/div/form/div[10]/span').text
                car_data['location'].append(location)

            except NoSuchElementException:
                car_data['location'].append(None)

            else:
                pass

            try:
                contact_number = driver.find_element_by_xpath('//div[@id="slrCntctNum"]').text
                car_data['contact_number'].append(contact_number)

            except NoSuchElementException:
                car_data['contact_number'].append(None)

            else:
                pass

            time.sleep(2)
            print(car_data)
            driver.back()
            time.sleep(2)
            cars_data.append(car_data)

        with open("cars_data.json", "w") as f:
            json.dump(cars_data, f)

        with open("cars_data.csv", 'w+', newline ='') as f:
            write = csv.writer(f)
            write.writerows(cars_data)

        pass

    #page = page + 1

    #next_button = driver.find_element_by_xpath('//*[@id="s0-27_2-9-0-1[0]-0-1"]/div[2]/nav/a[2]')
    #ActionChains(driver).move_to_element(next_button).click().perform()