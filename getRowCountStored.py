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

# query = "select count(email) from data_pph"
query = "select count(distinct no_telp) from data_pph_province"

cursor.execute(query)

result = list(cursor.fetchall())

for data in result:
    print(data)