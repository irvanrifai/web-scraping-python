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

# link to scrap
url = "https://info.halal.go.id/pendampingan/"

# Make a request
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')


# make request with selenium
driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get(url)

time.sleep(0.4)
driver.implicitly_wait(20)
# Get button and click it
# WebElement
# btn_click = WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.ID, "GridView3_lbView_0")))
# driver.execute_script("arguments[0].click();", btn_click)
# btn_click = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, "//div[contains(@id, 'GridView3_lbView_0')]//span//following::a[1]")))
btn_click = WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.XPATH, "//a[contains(@id,'GridView3_lbView_0')]")))
driver.execute_script("arguments[0].click();", btn_click)

# print(btn_click.text)
driver.implicitly_wait(20)

# WebElement 
# y = driver.find_element(By.XPATH, "//a[contains(@id,'GridView3_lbView_0')]").click()

# WebElement 
# x = driver.find_element(By.XPATH, "//a[contains(@id,'GridView3_lbView_0')]").click()

# print(x)
# for x in driver.find_element(By.XPATH, "//a[contains(@id,'GridView3_lbView_0')]"):
#     if x.text.isdigit():
#         print(x.text)

driver.switch_to.active_element
driver.switch_to.window(driver.window_handles[0])
# print(driver.page_source)
time.sleep(1)
# print(soup.select('span#lblNamaPendamping'))

driver.implicitly_wait(20)
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

# r = pd.read_html(page.content)
# r = pd.DataFrame(result)
# print(r)

keys = result[0].keys()

with open('data_pendamping_halal.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(result)



# 
# 
# 

# Create var data_pendamping_pph as empty list
# driver.switchTo().activeElement()
# parsed_code = BeautifulSoup(driver.page_source, 'html.parser')
# modal = driver.find_element(By.ID, "GridView3_lbView_0").click()

# modal = driver.find_element(By.ID, 'viewModalPPH')
# modal = parsed_code.select('div#viewModalPPH')

# print(parsed_code)

# modal_pendamping = modal.find('div', id='viewModalPPH')

# data_source_nama = modal_pendamping.find('span', id='lblNamaPendamping').get_text()
# data_source_email = modal_pendamping.find('span', id='lblEmailPendamping').get_text()
# data_source_no_telp = modal_pendamping.find('span', id='lblNoTelponPendamping').get_text()
# data_source_nama = modal('span', id='lblNamaPendamping').get_text()
# data_source_email = modal('span', id='lblEmailPendamping').get_text()
# data_source_no_telp = modal('span', id='lblNoTelponPendamping').get_text()

# data_pendamping_pph = []

# data_pendamping_pph.append({
#         "name" : data_source_nama,
#         "email" : data_source_email,
#         "no_telp" : data_source_no_telp
# })

# print(data_pendamping_pph)

# testing = BeautifulSoup(driver.page_source)
# print(testing)

# Create var data_pendamping_pph as empty list
# data_pendamping_pph = []

# print(table_pph)
# print(data_pendamping_pph)

# print(datas_pendamping)

# for data_pendamping in datas_pendamping:
#     email = data_pendamping.select('td.text-center')[0].text.strip()
#     # no_telp = data_pendamping.select('p.description')[0].text.strip()
#     # pelaku_usaha = data_pendamping.select('h4.price')[0].text.strip()
#     # image = product.select('img')[0].get('src')

#     data_pendamping_pph.append({
#         "email": email,
#         # "no_telp": no_telp,
#         # "pelaku_usaha": pelaku_usaha,
#         # "image": image
#     })

# # parse to csv
# keys = data_pendamping_pph[0].keys()

# with open('datas_pendamping.csv', 'w', newline='') as output_file:
#     dict_writer = csv.DictWriter(output_file, keys)
#     dict_writer.writeheader()
#     dict_writer.writerows(data_pendamping_pph)