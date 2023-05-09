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

query = "select * from history"

cursor.execute(query)

result = list(cursor.fetchall())

# print(result)
for data in result:
    print(data)

# (1, '17', '7')

# (1, '50', '7')