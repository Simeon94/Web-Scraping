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
import pandas as pd

cars_data_df = pd.read_json(r"C:\Users\Simeon\aicore\Data-scraping-project\cars_data.json")

print(cars_data_df.tail())
