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

page = 1

cars_data = []

URL = 'https://www.gumtree.com/cars/london'
driver.get(URL)
time.sleep(3)
cookies = driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]')
cookies_click = driver.execute_script("arguments[0].click();", cookies)
time.sleep(3)

page_link_items = driver.find_element_by_xpath('//*[@id="srp-results"]/div[1]/div[2]/div[3]/ul[2]')
page_link = page_link_items.find_elements_by_xpath("./li")
print("page_link", format(page_link))
page_num = len(page_link)
print("page_num", format(page_num))

for page in range(page_num):

    time.sleep(5)
    try:

        wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='fullListings']"))) # - main & full-listings
    except:
        driver.forward()

    div_tag = driver.find_element_by_xpath("//*[@id='fullListings']")
    time.sleep(2)

    #section_tag = driver.find_element_by_xpath('//*[@id="s0-27_2-9-0-1[0]-0-1"]')
    ul_tag = driver.find_element_by_xpath('//*[@id="srp-results"]/div[1]/div[2]/div[3]/ul[2]')
    cars = ul_tag.find_elements_by_xpath(".//li")
    car_numbers = len(cars)
    print("cars_numbers", format(car_numbers))

    for j in range(car_numbers):

        # time.sleep(3)
        try:

            wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='fullListings']")))
        except:
            driver.forward()
        #section_tag = driver.find_element_by_xpath('//*[@id="s0-27_2-9-0-1[0]-0-1"]')

        div_tag = driver.find_element_by_xpath('//*[@id="fullListings"]')
        time.sleep(3)

        ul_tag = div_tag.find_element_by_xpath('//*[@id="srp-results"]/div[1]/div[2]/div[3]/ul[2]')
        car = ul_tag.find_elements_by_xpath("./li")[j]

        ActionChains(driver).move_to_element(car).click().perform()

        time.sleep(3)

        car_data = { "sale_price": [], "year": [], "mileage": [], "location": [], "title": [], "description": []}

        try:
            sale_price = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div/main/div[3]/div[1]/div/div/span[2]/h2').text
            car_data['sale_price'].append(sale_price)

        except NoSuchElementException:
            car_data['sale_price'].append(None)

        try:
            year = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div/main/div[5]/section/section/div[2]/ul/li[1]/div[2]').text
            car_data['year'].append(year)

        except NoSuchElementException:
            car_data['year'].append(None)

        try:
            mileage = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div/main/div[5]/section/section/div[2]/ul/li[2]/div[2]').text
            car_data['mileage'].append(mileage)

        except NoSuchElementException:
            car_data['mileage'].append(None)

        try:
            location = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div/main/div[3]/div[1]/div/div/span[1]/h4').text
            car_data['location'].append(location)

        except NoSuchElementException:
            car_data['location'].append(None)

        try:
            title = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div/main/div[3]/div[1]/div/h1').text
            car_data['title'].append(title)

        except NoSuchElementException:
            car_data['title'].append(None)

        try:
            description = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div/main/div[5]/section/div[2]/p[1]').text
            car_data['description'].append(description)

        except NoSuchElementException:
            car_data['description'].append(None)

        time.sleep(2)
        print(car_data)
        driver.back()
        time.sleep(2)
        cars_data.append(car_data)

    with open("cars_data.json", "w") as f:
        json.dump(cars_data, f)

    with open("cars_data.csv", 'w+', newline='') as f:
        write = csv.writer(f)
        write.writerows(cars_data)

next_button = driver.find_element_by_xpath('//*[@id="srp-results"]/div[2]/div/ul/li[9]/a/span')
ActionChains(driver).move_to_element(next_button).click().perform()