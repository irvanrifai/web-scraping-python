import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="data_pendamping_halal"
)
if db.is_connected():
  print("connected to database!")
cursor = db.cursor()
email = 'adiecoet@gmail.com'
sql = "SELECT * FROM data_pph_province WHERE email = '%s' LIMIT 10" % email
# sql = "INSERT INTO data_pph_province (province, email, name, no_telp, pendampingan_pelaku_usaha) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE name = VALUES(name), no_telp = VALUES(no_telp), pendampingan_pelaku_usaha = VALUES(pendampingan_pelaku_usaha)"
# val = (nameProv, result[0]['email'], result[0]['name'], result[0]['no_telp'], result[0]['pendampingan_pelaku_usaha'])
# cursor.execute(sql, val)
cursor.execute(sql)

result = list(cursor.fetchall())

if len(result) > 0:
   print(result)
else:
   print('nothing')

# db.commit()