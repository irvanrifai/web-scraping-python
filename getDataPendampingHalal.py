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
import csv

# amount_data = 53514
# amount_page = 5352

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
time.sleep(1)
driver.implicitly_wait(40)

# click btn pagination if not in current page, give condition
# btn_page_click = WebDriverWait(driver, 40).until(ec.element_to_be_clickable((By.XPATH,"//table[@id='GridView3']/tbody/tr[@class='GridPager']/td/table/tbody/tr/td/a[contains(@href,'11')]")))
# exec_click = driver.execute_script("arguments[0].click();", btn_page_click)

time.sleep(1)
driver.implicitly_wait(40)

# btn_page_click = WebDriverWait(driver, 40).until(ec.element_to_be_clickable((By.XPATH,"//table[@id='GridView3']/tbody/tr[@class='GridPager']/td/table/tbody/tr/td/a[contains(@href,'13')]")))
# exec_click = driver.execute_script("arguments[0].click();", btn_page_click)

for i in range(10):
   time.sleep(2)
   driver.implicitly_wait(40)
   print(i)
   btn_lihat_click = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH, f"//a[contains(@id,'GridView3_lbView_{i}')]")))
   driver.execute_script("arguments[0].click();", btn_lihat_click)

   # wait data fetched full after clicked button lihat
   driver.implicitly_wait(60)
   driver.switch_to.active_element
   driver.switch_to.window(driver.window_handles[0])
   time.sleep(2)

   # execute (scrap data with identifier) rules execute script
   result = driver.execute_script(
   """
   var data_pendamping = [];
   for (var i of document.querySelectorAll('.modal#viewModalPPH')){
      data_pendamping.push({
         name:i.querySelector('span#lblNamaPendamping').textContent,
         email:i.querySelector('span#lblEmailPendamping').textContent,
         no_telp:i.querySelector('span#lblNoTelponPendamping').textContent,
         pendampingan_pelaku_usaha:i.querySelector('table#gvData3>tbody').textContent,
      });
   }
   return data_pendamping;
   """
   )

   print(result)

   # click button close after click detail(lihat) row
   modal = driver.find_element(By.ID, 'viewModalPPH')
   print(modal.is_displayed())
   # if (WebDriverWait(driver, 20).until(modal.is_displayed())):
   time.sleep(2)
   driver.implicitly_wait(60)

   # init btn close modal selector
   btn_close_click = WebDriverWait(driver, 20).until(ec.presence_of_all_elements_located((By.CLASS_NAME, "btn-close")))
   visible_buttons = [close_button for close_button in btn_close_click if close_button.is_displayed()]

   # do click close modal button
   time.sleep(0.5)
   driver.implicitly_wait(20)
   btn_lihat_click = visible_buttons[len(visible_buttons) - 1]
   driver.execute_script("arguments[0].click();", btn_lihat_click)
   time.sleep(1)
   driver.implicitly_wait(40)

   time.sleep(1)
   driver.implicitly_wait(40)

# fn for click get amount row of current pagination
def dataPerPage(num_page):
   # click btn pagination if not in current page, give condition
   btn_page_click = WebDriverWait(driver, 30).until(ec.element_to_be_clickable((By.XPATH, "//a[contains(@href,'javascript:__doPostBack('GridView3','"+ num_page +"')')]")))
   driver.execute_script("arguments[0].click();", btn_page_click)

   # wait data fetched full after clicked button pagination
   driver.implicitly_wait(40)
   time.sleep(1)

   return 0

# fn for click btn lihat and scrap data selected
def clickAndGetOne(id_btn):
   # Get button Lihat and click it, use wait until clicked, and use rules execute script
   btn_lihat_click = WebDriverWait(driver, 30).until(ec.element_to_be_clickable((By.XPATH, "//a[contains(@id,'GridView3_lbView_"+ id_btn +"')]")))
   driver.execute_script("arguments[0].click();", btn_lihat_click)

   # wait data fetched full after clicked button Lihat
   driver.implicitly_wait(40)
   driver.switch_to.active_element
   driver.switch_to.window(driver.window_handles[0])
   time.sleep(1)

   # execute (scrap data with identifier) rules execute script
   result = driver.execute_script(
   """
   var data_pendamping = [];
   for (var i of document.querySelectorAll('.modal#viewModalPPH')){
      data_pendamping.push({
         name:i.querySelector('span#lblNamaPendamping').textContent,
         email:i.querySelector('span#lblEmailPendamping').textContent,
         no_telp:i.querySelector('span#lblNoTelponPendamping').textContent,
         pendampingan_pelaku_usaha:i.querySelector('table#gvData3>tbody').textContent,
      });
   }
   return data_pendamping;
   """
   )

   return result

# get keys (header) of data
# keys = result[0].keys()

# parsed to csv
# with open('data_pendamping_halal.csv', 'w', newline='') as output_file:
#     dict_writer = csv.DictWriter(output_file, keys)
#     dict_writer.writeheader()
#     dict_writer.writerows(result)