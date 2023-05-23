import mysql.connector
import csv

# connect to DB
db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="data_pendamping_halal"
)

if db.is_connected():
  print("Database connected")
cursor = db.cursor()

query = "select province, name, email, no_telp from data_pph_province order by province asc"

cursor.execute(query)

result = list(cursor.fetchall())

# print(result)
for data in result:
    print(data)

# parsed to csv
with open('data_pendamping_halal_all(by province-no filter).csv', 'w', newline='', encoding="utf-8") as output_file:
    dict_writer = csv.writer(output_file)
    # dict_writer = csv.DictWriter(output_file)
    # dict_writer.writeheader()
    dict_writer.writerow([i[0] for i in cursor.description])
    dict_writer.writerows(result)
