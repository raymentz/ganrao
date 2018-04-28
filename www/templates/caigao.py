import mysql.connector

conn = mysql.connector.connect(user='root', password='password', database='test', charset='utf8')
cursor = conn.cursor()
cursor.execute('create table gongdan (gongdanid varchar(20) primary key, name varchar(20))')
conn.commit()
conn.close()