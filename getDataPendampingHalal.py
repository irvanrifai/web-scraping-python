# import plugin
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import csv

# link to scrap
url = "https://info.halal.go.id/pendampingan/"

# Make a request
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

# make request with selenium
driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get(url)

driver.implicitly_wait(20)
# Get button and click it
btn_click = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.ID, "GridView3_lbView_0")))
driver.execute_script("arguments[0].click();", btn_click)

# print(btn_click.text)

driver.switch_to.active_element

# Create var data_pendamping_pph as empty list
# driver.switchTo().activeElement()
parsed_code = BeautifulSoup(driver.page_source, 'html.parser').select('div#viewModalPPH')
# modal = driver.find_element(By.ID, "GridView3_lbView_0").click()

# modal = driver.find_element(By.ID, 'viewModalPPH')
# modal = parsed_code.select('div#viewModalPPH')

print(parsed_code)

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