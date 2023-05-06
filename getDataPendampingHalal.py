# import plugin
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import pandas as pd
import time
import mysql.connector
import csv

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="data_pendamping_halal"
)

if db.is_connected():
  print("Berhasil terhubung ke database")

cursor = db.cursor()
# cursor.execute("CREATE DATABASE data_pendamping_halal")

# sql = """CREATE TABLE history (
#   id INT AUTO_INCREMENT PRIMARY KEY,
#   last_page VARCHAR(255),
#   last_row VARCHAR(255)
# )
# """
# cursor.execute(sql)

sql = "INSERT INTO data_pph (email, name, no_telp, pendampingan_pelaku_usaha) VALUES (%s, %s, %s, %s)"
val = ("dian@example.com", "dian", "d14n", "diaann")
cursor.execute(sql, val)

db.commit()

print('table created!')

# identify pagination
# <a href="javascript:__doPostBack('GridView3','Page$3')">3</a> --changing (Page$1 - Page$11 - Page$Last/Page$5352)

# note
# per pagination have default row is 10
# per pagination especially last page not have full-row(10 row), so make counter amount row per pagination
# be carefull with page 11,21,31, etc

# identify button lihat(detail) per row
# <a id="GridView3_lbView_6" href="javascript:__doPostBack('GridView3$ctl08$lbView','')">Lihat</a> --changing (GridView3_lbView_0 - GridView3_lbView_9/depend on amount row)
# ordering with start from index 0

# link to scrap
url = "https://info.halal.go.id/pendampingan/"

# make request with selenium
driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get(url)
# sleep and/or wait until web full opened
time.sleep(2)
driver.implicitly_wait(30)

def openModalGetDataCloseModalPerRow():
    # wait data fetched full after clicked button lihat
   driver.implicitly_wait(60)
   driver.switch_to.active_element
   driver.switch_to.window(driver.window_handles[0])
   time.sleep(2)

   # checking is modal displayed or not yet
   modal = driver.find_element(By.ID, 'viewModalPPH')
   time.sleep(2)
   driver.implicitly_wait(30)
   print(f"modal view pph {modal.is_displayed()}")
   if not modal.is_displayed():
      print("Wait 3 sec.. until modal displayed True")
                  
      time.sleep(3)
      driver.implicitly_wait(60)
         
   # execute (scrap data with identifier) rules execute script, if modal is displayed
   # if modal.is_displayed(): (too take risk)
   result = driver.execute_script(
      """
         var data_pendamping = [];
         for (var i of document.querySelectorAll('.modal#viewModalPPH')){
            data_pendamping.push({
               email:i.querySelector('span#lblEmailPendamping').textContent,
               name:i.querySelector('span#lblNamaPendamping').textContent,
               no_telp:i.querySelector('span#lblNoTelponPendamping').textContent,
               pendampingan_pelaku_usaha: i.querySelector('div#UpdatePanel1>div>table#gvData3>tbody').textContent,
            });
         }
         return data_pendamping;
      """
   )

   print(f"fetched data {result}")
   data_pendamping_halal.append({
      "name": result[0]['name'],
      "email": result[0]['email'],
      "no_telp": result[0]['no_telp'],
      "pendampingan_pelaku_usaha": result[0]['pendampingan_pelaku_usaha'],
   })

   # click button close after click detail(lihat) row
   modal = driver.find_element(By.ID, 'viewModalPPH')
   print(f"modal view pph {modal.is_displayed()}, then close")
   if modal.is_displayed() == False:
      print("Wait 3 sec.. until modal displayed True, then close")
                     
      time.sleep(3)
      driver.implicitly_wait(60)

   # init btn close modal selector
   btn_close_click = WebDriverWait(driver, 40).until(ec.presence_of_all_elements_located((By.CLASS_NAME, "btn-close")))
   visible_buttons = [close_button for close_button in btn_close_click if close_button.is_displayed()]

   # do click close modal button
   time.sleep(2)
   driver.implicitly_wait(40)
   btn_lihat_click = visible_buttons[len(visible_buttons) - 1]
   driver.execute_script("arguments[0].click();", btn_lihat_click)
   time.sleep(1)
   driver.implicitly_wait(40)

def clickDetailPerRow():
   # amount of row in current table show, should decrease 2 row, cause first row is thead and last row is pagination
   row_table_pendamping = len(driver.find_elements(By.XPATH, "//table[@id='GridView3']/tbody/tr")) - 2

   time.sleep(3)
   driver.implicitly_wait(60)
   for i in range(row_table_pendamping):
      # if y+1 != 1 and i != 0:
         # time.sleep(2)
         # driver.implicitly_wait(60)
         # print(f"data index {i}")
         # btn_lihat_click = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH, f"//a[contains(@id,'GridView3_lbView_{i}')]")))
         # driver.execute_script("arguments[0].click();", btn_lihat_click)

         # openModalGetDataCloseModalPerRow()
         
         
      time.sleep(2)
      driver.implicitly_wait(60)
      print('')
      print(f"data index {i}")
      print('')
      btn_lihat_click = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH, f"//a[contains(@id,'GridView3_lbView_{i}')]")))
      driver.execute_script("arguments[0].click();", btn_lihat_click)

      time.sleep(2)
      driver.implicitly_wait(60)

      openModalGetDataCloseModalPerRow()

# click last page to count amount of page
last_page_btn = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, "//table[@id='GridView3']/tbody/tr[@class='GridPager']/td/table/tbody/tr/td/a[text() = '>>']")))
driver.execute_script("arguments[0].click();", last_page_btn)
time.sleep(3)
driver.implicitly_wait(60)
last_page = driver.find_element(By.XPATH, "//table[@id='GridView3']/tbody/tr[@class='GridPager']/td/table/tbody/tr/td/span")
time.sleep(2)
driver.implicitly_wait(20)
print('')
print(f"amount all pagination is {last_page.text}")
print('')

# click firt page to back default
# if last_page_btn.is_selected():
   # first_page_btn = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, "//table[@id='GridView3']/tbody/tr[@class='GridPager']/td/table/tbody/tr/td/a[text() = '<<']")))
   # driver.execute_script("arguments[0].click();", first_page_btn)
   # time.sleep(1)
   # driver.implicitly_wait(20)
first_page_btn = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, "//table[@id='GridView3']/tbody/tr[@class='GridPager']/td/table/tbody/tr/td/a[text() = '<<']")))
driver.execute_script("arguments[0].click();", first_page_btn)
time.sleep(1)
driver.implicitly_wait(20)

# list null for datas
data_pendamping_halal = []

# init looping page
# time.sleep(1)
# driver.implicitly_wait(30)
for x in range(int(last_page.text)):
   print(f"Current page is {x+1}")

   # amount of pagination, except '...', another '...', '<<' and '>>'
   # on first and last pager is 12, etc is 14
   amount_pagination_current_page = len(driver.find_elements(By.XPATH, "//table[@id='GridView3']/tbody/tr[@class='GridPager']/td/table/tbody/tr/td"))

   if amount_pagination_current_page == 12 :
      amount_pagination_12 = amount_pagination_current_page - 2
      print(f"amount pagination {amount_pagination_current_page}")
      print('')
      # click btn pagination if not in current page, give condition (only first page)
      for y in range(1, int(last_page.text), 1):
         # exception first page cause error
         if y+1 != 1 and y % 10 != 0:
            # time.sleep(2)
            # driver.implicitly_wait(30)
            btn_page_click = WebDriverWait(driver, 50).until(ec.element_to_be_clickable((By.XPATH,f"//table[@id='GridView3']/tbody/tr[@class='GridPager']/td/table/tbody/tr/td/a[text() = '{y+1}']")))
            driver.execute_script("arguments[0].click();", btn_page_click)
            time.sleep(3)
            driver.implicitly_wait(60)
            print('')
            print(f"click pager's {y+1} --non % 10")
            print('')

         elif y % 10 == 0 :
            btn_page_next_click = WebDriverWait(driver, 50).until(ec.element_to_be_clickable((By.XPATH,f"//table[@id='GridView3']/tbody/tr[@class='GridPager']/td/table/tbody/tr/td/a[contains(@href,'{y+1}')]")))
            driver.execute_script("arguments[0].click();", btn_page_next_click)
            time.sleep(3)
            driver.implicitly_wait(60)
            print('')
            print(f"click pager's {y+1} --can % 10")
            print('')

         clickDetailPerRow()

   # elif amount_pagination_current_page == 14 :
   #    amount_pagination_14 = amount_pagination_current_page - 4
   #    print(f"amount pagination {amount_pagination_14}")
   #    # click btn pagination if not in current page, give condition (to all page)
   #    if amount_pagination_14 <= x+1:
   #       btn_again_page_click = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,f"//table[@id='GridView3']/tbody/tr[@class='GridPager']/td/table/tbody/tr/td/a[text() = '{x+1}']")))
   #       driver.execute_script("arguments[0].click();", btn_again_page_click)
   #       time.sleep(2)
   #       driver.implicitly_wait(60)
   #    elif amount_pagination_14 > x+1 :
   #       btn_again_page_next_click = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,"//table[@id='GridView3']/tbody/tr[@class='GridPager']/td/table/tbody/tr/td/a[contains(@href,'21')]")))
   #       driver.execute_script("arguments[0].click();", btn_again_page_next_click)
   #       time.sleep(2)
   #       driver.implicitly_wait(60)

   # else :
   #    btn_else_page_click = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,f"//table[@id='GridView3']/tbody/tr[@class='GridPager']/td/table/tbody/tr/td/a[text() = '{x+1}']")))
   #    driver.execute_script("arguments[0].click();", btn_else_page_click)
   #    time.sleep(2)
   #    driver.implicitly_wait(60)

print(data_pendamping_halal)
print(f"total data fetched {len(data_pendamping_halal)}")

# get keys (header) of data
keys = data_pendamping_halal[0].keys()

# parsed to csv
with open('data_pendamping_halal.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(data_pendamping_halal)