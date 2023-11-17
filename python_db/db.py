import pymysql

db = pymysql.connect(host="101.101.210.141", port=3306, user='ymh6162', passwd="1234", db="ymh6162", charset="utf8")

cursor = db.cursor()
# cursor = db.cursor()
# sql = """
#     CREATE TABLE ljb(
#         name varchar(20) not null,
#         math INT null,
#         english INT null,
#         PRIMARY KEY (name)
#     )
# """

# sql = """
#     INSERT INTO ljb(name, math, english)
#     values('lee', 80, 20)
# """

# sql = """
#     update ljb
#     set math = 10, english=10
#     where name = "lee"
# """

sql = """
    select * 
    from ljb
"""
cursor.execute(sql)
rs = cursor.fetchall()
print(rs)

db.commit()
cursor.close()
db.close()
