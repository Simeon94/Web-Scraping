#!/usr/bin/env sh
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions as exception
import json
import time

def get_cars():

    """
    Function to get cars as listed on gumtree
    and write it to a file
    """

    cars_list = []

    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')

    # headless option to prevent opening a new browser window
    options.add_argument("headless")
    desired_capabilities = options.to_capabilities()

    #driver to open a new browser and navigate it
    driver = webdriver.Chrome(desired_capabilities=desired_capabilities)

    #Get car container from the website

    URL = ('https://www.ebay.co.uk/b/Cars/9801/bn_1839037')
    driver.get(URL)
    cookies = driver.find_element_by_xpath('//*[@id="gdpr-banner-accept"]')
    cookies.click()

    #Get cars from car_container

    ##cars_container = driver.find_element_by_xpath('//*[@id="mainContent"]')

    ##car_container = driver.find_element_by_class_name("b-list__items_nofooter srp-results srp-grid")

    cars = driver.find_elements_by_class_name("s-item__title").text
    ##cars_title_split = cars_title.split()
    ##cars = cars_title_split[:1]

    for car in cars:
        cars_list.append(car)

    driver.quit()

    #Write cars_list to a json file
    with open("cars_list.json", "w") as f:
        json.dump(cars_list, f)

def get_pages():
    """
    Function to get cars page containers of cars and write it to a file
    """

    #Open cars_list written by get_cars()
    with open("cars_list.json", "r") as f:
        cars_list = json.load(f)


    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')

    # headless option to prevent opening a new browser window
    options.add_argument("headless")
    desired_capabilities = options.to_capabilities()

    #driver to open a new browser and navigate it
    driver = webdriver.Chrome(desired_capabilities=desired_capabilities)

    #Use page final to let allow code to stop after extrcating data on the final page
    #pages_final = []

    for cars in cars_list:

        #Open site
        URL = ('https://www.ebay.co.uk/b/Cars/9801/bn_1839037')
        driver.get(URL)
        cookies = driver.find_element_by_xpath('//*[@id="gdpr-banner-accept"]')
        cookies.click()
        time.sleep(3)

        pages = []

        #scrolling down the page(s)
        action = ActionChains(driver)
        action.move_to_element(driver.find_element_by_xpath('//*[@id="s0-27_1-9-0-1[0]-0-1"]/ul/li[47]/div/div[2]/a/h3'))
        #action.move_to_element(driver.find_element_by_xpath('//h3[contains(text()," s-item__title'))
        action.perform()

        #Identifying on each car
        car_button = driver.find_element_by_css_selector('h3.s-item__title')
        car_button.click()
        time.sleep(3)

        while True:

            page_container = driver.find_elements_by_xpath('//*[@id="s0-27_1-9-0-1[0]-0-1"]/div[2]/nav/ol')
            #page_container = driver.find_elements_by_xpath('//ol[@class="pagination__items"]')
            #page_container = driver.find_elements_by_class_name("pagination__items")

            #Get "href" of page links from page_container and append to pages list as page
            for link in page_container:

                page = link.get_attribute("href")
                pages.append(page)

            #Pressing 'NEXT' button

            try:
                next_button = driver.find_element_by_xpath('//*[@id="s0-27_1-9-0-1[0]-0-1"]/div[2]/nav/a[2]')
                #next_button = driver.find_element_by_xpath('//a[@_sp="p2489527.m4335.l1513"]')
                next_button.click()

            except exception.NoSuchElementException:
                pages.append(None)
                #logger.debug(f"Last page reached for {pages}")
                break

        driver.quit()

        # Write the pages to a file
        with open("pages.json", "w") as f:
            json.dump(pages, f)


def get_car_data():
    """
    Function to extract car data from all the pages
    and write it to a file.
    """

    # Load the pages written by get_pages()
    with open("pages.json", "r") as f:
        pages = json.load(f)

    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')

    # headless option to prevent opening a new browser window
    options.add_argument("headless")
    desired_capabilities = options.to_capabilities()

    #driver to open a new browser and navigate it
    driver = webdriver.Chrome(desired_capabilities=desired_capabilities)

    car_dict = {"sale_price": [], "year": [], "mileage": [], "description": [], "condtion": [], "location": [], "contact_number": []}

    for i, page in enumerate(pages):

        # Open each page using the links saved in pages
        driver.get(page)
        time.sleep(3)

        try:
            #sale_price = driver.find_element_by_xpath('//span[@class="notranslate"]').text
            sale_price = driver.find_element_by_xpath('//*[@id="prcIsum"]').text
            data['sale_price'].append(sale_price)

        except NoSuchElementException:
            data['sale_price'].append(None)

        try:
            #year = driver.find_element_by_xpath('//td').text
            year = driver.find_element_by_xpath('//*[@id="ds_div"]/div[1]/div[4]/table[1]/tbody/tr[3]/td').text
            data['year'].append(year)

        except NoSuchElementException:
            data['year'].append(None)

        try:
            mileage = driver.find_element_by_xpath('//*[@id="ds_div"]/div[1]/div[4]/table[2]/tbody/tr[3]/td').text
            data['mileage'].append(mileage)

        except NoSuchElementException:
            data['mileage'].append(None)

        try:
            #description = driver.find_element_by_xpath('//div[@class="enp__description"]').text
            description = driver.find_element_by_xpath('//*[@id="ds_div"]/div[1]/div[6]').text
            data['description'].append(description)

        except NoSuchElementException:
            data['description'].append(None)

        try:
            #condtion = driver.find_element_by_xpath('//div[@class="u-flL labe"]').text
            condtion = driver.find_element_by_xpath('//*[@id="vi-itm-cond"]').text
            data['condtion'].append(condtion)

        except NoSuchElementException:
            data['condtion'].append(None)

        try:
            #location = driver.find_element_by_xpath('//span[@itemprop="availableAtOrFrom"]').text
            location = driver.find_element_by_xpath('//*[@id="LeftSummaryPanel"]/div/form/div[10]/span').text
            data['location'].append(location)

        except NoSuchElementException:
            data['location'].append(None)

        try:
            #contact_number = driver.find_element_by_xpath('//div[@id="sleCntctNum"]').text
            contact_number = driver.find_element_by_xpath('//*[@id="slrCntctNum"]').text
            data['contact_number'].append(contact_number)

        except NoSuchElementException:
            data['contact_number'].append(None)

    driver.quit()
    # Write the pages to a file
    with open("car_data.json", "w") as f:
        json.dump(car_data, f)
