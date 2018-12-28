import json, mysql.connector

file = open("text.txt", "r")
res = file.read()
response = json.loads(res.encode())
selfmydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database = "tv"
        )















info = response['info']
other = response['other']
link = response['link']

sql1 = ""
sql2 = ""
data = []
i = 0
length = len(info)
for key, value in info.items():
    if i != 0:
        sql1 += ","
        sql2 += ","

    sql1 += "`" + key + "`"
    sql2 += "%s"
    i = i + 1
    if type(value) == type({}):
        data.append(json.dumps(value))
    else:
        data.append(str(value))
db = selfmydb.cursor()
command = "SELECT * FROM  `play` WHERE  `chinese` LIKE  '" + response['info']['chinese'] + "' AND  `tid` =" + str(response['info']['tid'])
db.execute(command)
if not db.fetchone():
    # -------------------增加此影片基本信息----------------------
    command = "INSERT INTO `tv`.`play` (" + sql1 + ") VALUES (" + sql2 + ")"
    db.execute(command, data)
    selfmydb.commit()
    # -----------------------完毕------------------------------

    # -------------------获取本次插入的ID----------------------
    sql = "select max(id) from `play`"
    db.execute(sql)
    playid = str(db.fetchone()[0])
    # ----------------------获取完毕--------------------------
    # --------------------插入link信息------------------------
    sql1 = ""
    sql2 = ""
    dataAll = []
    for res in response['link']:
        sql1 = ""
        sql2 = ""
        res['pid'] = playid
        data = []
        i=0
        for key, value in res.items():
            if i != 0:
                sql1 += ","
                sql2 += ","

            sql1 += "`" + key + "`"
            sql2 += "%s"
            i = i + 1
            if type(value) == type({}):
                data.append(json.dumps(value))
            else:
                data.append(str(value))
        dataAll.append(tuple(data))
    command = "INSERT INTO `tv`.`link` (" + sql1 + ") VALUES (" + sql2 + ")"
    db.executemany(command, dataAll)
    selfmydb.commit()
    # ---------------------------------------------------------------

    # ---------------------------------------------------------------
    if len(response['other']['type'])!=0:
        type_data = []
        for res in response['other']['type']:
            type_data.append((res,playid))
        command = "INSERT INTO `tv`.`classify` (`value`,`pid`) VALUES (%s,%s)"
        db.executemany(command, type_data)
        selfmydb.commit()
    if len(response['other']['performer'])!=0:
        performer_data = []
        for res in response['other']['performer']:
            performer_data.append((res,playid))
        command = "INSERT INTO `tv`.`performer` (`name`,`pid`) VALUES (%s,%s)"
        db.executemany(command, performer_data)
        selfmydb.commit()
else:
    print("已存在")



