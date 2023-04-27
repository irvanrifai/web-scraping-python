# import plugin
import requests
from bs4 import BeautifulSoup
import csv

# link to scrap
url = "https://info.halal.go.id/pendampingan/"

# Make a request
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

# Create var data_pendamping_pph as empty list
data_pendamping_pph = []

# Extract and store in data_pendamping according to instructions on the left
datas_pendamping = soup.select('tr')

print(datas_pendamping)

for data_pendamping in datas_pendamping:
    email = data_pendamping.select('td.text-center')[0].text.strip()
    # no_telp = data_pendamping.select('p.description')[0].text.strip()
    # pelaku_usaha = data_pendamping.select('h4.price')[0].text.strip()
    # image = product.select('img')[0].get('src')

    data_pendamping_pph.append({
        "email": email,
        # "no_telp": no_telp,
        # "pelaku_usaha": pelaku_usaha,
        # "image": image
    })

# parse to csv
keys = data_pendamping_pph[0].keys()

with open('datas_pendamping.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(data_pendamping_pph)