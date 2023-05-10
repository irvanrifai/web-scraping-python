import mysql.connector

# connect to DB
db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd=""
)

if db.is_connected():
  print("Berhasil terhubung ke database")

# create DB
cursor = db.cursor()
cursor.execute("CREATE DATABASE data_pendamping_halal")

print('database created')