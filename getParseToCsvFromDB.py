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

query = "select distinct email, name, no_telp, pendampingan_pelaku_usaha from data_pph"

cursor.execute(query)

result = list(cursor.fetchall())

# print(result)
for data in result:
    print(data)

# parsed to csv
with open('data_test.csv', 'w', newline='') as output_file:
    dict_writer = csv.writer(output_file)
    # dict_writer = csv.DictWriter(output_file)
    # dict_writer.writeheader()
    dict_writer.writerow([i[0] for i in cursor.description])
    dict_writer.writerows(result)
