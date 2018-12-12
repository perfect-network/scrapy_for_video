import re, requests, json, time

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
b = json.dumps(object)
file.write(b)