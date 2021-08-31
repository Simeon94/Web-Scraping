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

#cars_data_df = pd.read_json(r"C:\Users\Simeon\aicore\Data-scraping-project\Web-Scraping\cars_data.json")

#print(cars_data_df.head())

# with open("cars_data_df.csv", 'w+', newline='') as g:
#     write = csv.writer(g)
#     write.writerows(cars_data_df)

with open(r"C:\Users\Simeon\aicore\Data-scraping-project\Web-Scraping\cars_data.json", 'r') as f:
    cars_data = json.load(f)
    cars_data_df = pd.DataFrame(cars_data)

#print(cars_data_df)

#cars_data_df.to_csv("cars_data_df.csv")
# with open("cars_data_df.csv", 'w+', newline='') as f:
#     write = csv.writer(f)
#     write.writerows(cars_data_df)

from sqlalchemy import create_engine
import pandas as pd
DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
HOST = 'localhost'
USER = 'postgres'
PASSWORD = 'password*'
DATABASE = 'cars_data'
PORT = 5432
engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

cars_data_df.to_sql('cars', engine, if_exists='replace')