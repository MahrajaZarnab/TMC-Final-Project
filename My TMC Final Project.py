from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv
import pandas as pd
import mysql.connector
from selenium.webdriver.chrome.service import Service


service = Service('C:\chromedriver_win32\chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get('https://www.qlik.com/us/partners/find-a-partner')
driver.maximize_window()
select = Select(driver.find_element(By.ID,'zl_countryCode'))
select.select_by_value("US")
time.sleep(5)
button = driver.find_element(By.ID, "zl_show-more-btn")
while True:
    button.click()
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"zl_show-more-btn")))
    div = driver.find_element(By.ID,"zl_show-more")
    if div.value_of_css_property("display") == "none":
        print("No more load button")
        break


soup = BeautifulSoup(driver.page_source,'html.parser')
elements = soup.find('div',class_="zl_partner-tiles")
stores_partners=[]
for row in elements('div',class_="zl_partner-tile zl_partner-tile-hover"):
    store={}
    store['title']=row.find('div',class_="zl_partner-name zl_partner-name-hover").text
    #store['url']=row.a['href']
    store['address']=row.find('div',class_="zl_partner-address").get_text(separator = " ").strip()
    stores_partners.append(store)
#stores_partners
    
df=pd.DataFrame.from_dict(stores_partners)
df.head(5) 


conn = mysql.connector.connect(user='root', password='allah', host='localhost', database='sakila')
if (conn.is_connected()):
    print("Connected")
else:
    print("Not connected")
# Create a table called "customers"
mycursor = conn.cursor()

mycursor.execute("DROP TABLE IF EXISTS qlik")
mycursor.execute("CREATE TABLE qlik (title VARCHAR(255), address VARCHAR(255))")

q=""" insert into qlik (title, address) values (%s,%s)"""
values=[( store['title'],store['address']) for store in stores_partners]
mycursor.executemany(q, values)
conn.commit()

print(mycursor.rowcount, "record(s) inserted.")
