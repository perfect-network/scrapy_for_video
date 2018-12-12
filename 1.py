import re, requests, json, time, mysql.connector

file = open("text.txt","w",encoding="utf-8")
body = requests.get(url="https://v.qq.com/x/cover/c6pp7uwg1o4h4bq.html").content
body = str(body,"utf-8")
body = re.search("var COVER_INFO = ([\s\S]*)var COLUMN_INFO",body).group()
body = body.replace("var COVER_INFO = ","")
body = body.replace("var COLUMN_INFO","")
object = json.loads(body,encoding="utf-8")
if object['pay_status'] == 6:
    member = 1
else:
    member = 0
if 'title_en' in object:
    en = object['title_en']
else:
    en = "none"
value = (
    object['title'],
    en,
    object['main_genre'],
    object['year'],
    object['vertical_pic_url'],
    object['new_pic_hz'],
    object['description'],
    member,
    object['director'][0],
    json.dumps(object['leading_actor']),
    object['publish_date'],
    object['current_num'],
    object['episode_all'],
    object['area_name'],
    object['score']['score'],
    int(time.time()),
    object['payfree_num'],
    1,
    object['score']['hot'],
    object['second_title'],
    object['langue']
)


mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database = "tv"
        )

command = "INSERT INTO `tv`.`play` (`chinese`, `english`, `classify`, `year`, `picture`, `picture_hor`, `description`, `member`, `performer`, `publishdate`, `current_num`, `total`, `region`, `payfree_num`, `title`, `lang`, `score`, `hot`, `tid`, `addtime`, `director`) " \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
key = ("title", 'title_en', 'main_genre', 'year', 'vertical_pic_url', 'new_pic_hz', 'description', 'pay_status',
       'leading_actor', 'publish_date', 'current_num', 'episode_all', 'area_name', 'payfree_num', 'second_title',
       'langue')
value = []
for k in key:
    if k in object:
        if isinstance(object[k], list):
            value.append(json.dumps(object[k]))
        elif isinstance(object[k], int):
            value.append(str(object[k]))
        else:
            value.append(object[k])
    else:
        value.append(str(0))
value.append(str(object['score']['score']))
value.append(str(object['score']['hot']))
value.append(str(1))
value.append(str(int(time.time())))
value.append(object['director'][0])
bb = tuple(value)
for b in bb:
    print(type(b))
    print(b)
