import mysql.connector, sys
mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database = "tv"
        )
def delete():
    c = mydb.cursor()
    c.execute("DELETE FROM `cid` WHERE 1")
    mydb.commit()
    c.execute("DELETE FROM `play` WHERE 1")
    mydb.commit()
    c.execute("DELETE FROM `link` WHERE 1")
    mydb.commit()
    print("删除成功")

def insert():
    c = mydb.cursor()
    value = [("1122","1","qq"), ("1122","1","qq")]
    sql = "INSERT INTO cid (cid, vip, site) VALUES (%s, %s, %s)"
    x = c.executemany(sql, value)
    x = mydb.commit()
def max():
    c = mydb.cursor()
    sql = "select max(id) from cid"
    c.execute(sql)
    print(str(c.fetchone()[0]))

data = sys.argv
if data[1]=="delete":
    delete()
elif data[1]=="insert":
    insert()
elif data[1]=="max":
    max()