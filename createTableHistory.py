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
sql = """CREATE TABLE history (
   id INT AUTO_INCREMENT PRIMARY KEY,
   last_page VARCHAR(255),
   last_row VARCHAR(255)
)"""
cursor.execute(sql)

print('table history created')