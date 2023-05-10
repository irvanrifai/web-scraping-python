import mysql.connector

# connect to DB
db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="data_pendamping_halal"
)
cursor = db.cursor()

# create table
sql = """CREATE TABLE data_pph (
   id INT AUTO_INCREMENT PRIMARY KEY,
   email VARCHAR(255),
   name VARCHAR(255),
   no_telp VARCHAR(255),
   pendampingan_pelaku_usaha TEXT
)"""
cursor.execute(sql)

print('table data_pph created')