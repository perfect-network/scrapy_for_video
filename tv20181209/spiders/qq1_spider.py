import scrapy, json, mysql.connector, re, requests, time


class QuotesSpider(scrapy.Spider):
    name = "qq1"

    def __init__(self):
        self.file = open("text.txt", "w")
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database = "tv"
        )

    def start_requests(self):
        url = "http://v.qq.com/x/list/tv?offset=0&sort=19"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = response.css(".list_item")
        for item in items:
            cid = item.css("li::attr(__wind)").extract()[0].replace("cid=","")
            if item.css(".mark_v>img::attr(alt)"):
                vip = 1
            else:
                vip = 0
            mycursor = self.mydb.cursor()
            where = 'SELECT cid FROM `cid` WHERE `cid`="' + cid + '"'
            mycursor.execute(where)
            select = mycursor.fetchone()
            if select is None:
                sql = "INSERT INTO cid (cid, vip, site) VALUES (%s, %s, %s)"
                val = (cid, vip, self.name)
                mycursor.execute(sql,val)
                self.mydb.commit()
                body = {'dataKey' :"req_type=2&lid=&cid="+cid+ "&vid=&ui=0", 'pageContext' :""}
                body = json.dumps(body)
                url = "http://access.video.qq.com/tinyapp/detail_video_list?vappid=65939066&vsecret=07c58e0c93150c4254a2a24131574b94cab6142ba4210efa&vversion_name=5.2.0.1234&vplatform=3"
                yield scrapy.Request(method="POST",url=url,body=body,callback=self.link,meta={'cid':cid})

    def link(self,response):
        mycursor = self.mydb.cursor()
        url = "https://v.qq.com/x/cover/" + response.meta['cid'] + ".html"
        body = requests.get(url=url).content
        body = str(body, "utf-8")
        body = re.search("var COVER_INFO = ([\s\S]*)var COLUMN_INFO", body).group()
        body = body.replace("var COVER_INFO = ", "")
        body = body.replace("var COLUMN_INFO", "")
        object = json.loads(body, encoding="utf-8")
        command = "INSERT INTO `tv`.`play` (`chinese`, `english`, `classify`, `year`, `picture`, `picture_hor`, `description`, `member`, `performer`, `publishdate`, `current_num`, `total`, `region`, `payfree_num`, `title`, `lang`, `score`, `hot`, `tid`, `addtime`, `director`, `finish`) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        key = ("title", 'title_en', 'main_genre', 'year', 'vertical_pic_url', 'new_pic_hz', 'description', 'pay_status',
               'leading_actor', 'publish_date', 'current_num', 'episode_all', 'area_name', 'payfree_num',
               'second_title',
               'langue')
        value = []
        current_num = 0
        episode_all = 1
        for k in key:
            if k in object:
                if k=="pay_status":
                    if object[k]==6:
                        value.append(str(1))
                    else:
                        value.append(str(0))
                elif isinstance(object[k], list):
                    value.append(json.dumps(object[k]))
                elif isinstance(object[k], int):
                    value.append(str(object[k]))
                else:
                    value.append(str(object[k]))
            else:
                value.append(str(0))
        value.append(str(object['score']['score']))
        value.append(str(object['score']['hot']))
        value.append(str(1))
        value.append(str(int(time.time())))
        value.append(str(object['director'][0]))
        if str(object['current_num'])==str(object['episode_all']):
            value.append(str(1))
        else:
            value.append(str(0))

        value = tuple(value)
        update = mycursor.execute(command, value)
        update = self.mydb.commit()
        sql = "select max(id) from cid"
        mycursor.execute(sql)
        playid = str(mycursor.fetchone()[0])
        body = response.body.decode()
        body = body.replace("data=","")
        data = []
        play = []
        body = json.loads(body)
        videoList = body["data"]["videoList"]
        for video in videoList:
             if "videoShowFlags" in video and video['videoShowFlags']==0:
                 # 视频VID，视频标题，视频集数，
                 if "playStatus" in video and video['playStatus']==8:
                     member = str(0)
                 else:
                     member = str(1)
                 play.append(str(video['poster']['firstLine']))
                 play.append({"episode":str(video['poster']['firstLine']),"member":member})
                 res = (video['title'], playid, member, self.name, response.meta['cid'] + "/" + video['vid'], str(video['poster']['firstLine']))
                 data.append(res)
        play = json.dumps(play)
        play = json.loads(play)
        update = {self.name:{"count":len(play),"episode":play}}
        update = (json.dumps(update),)
        command = "UPDATE `play` SET `site`=%s"
        mycursor.execute(command,update)
        command = "INSERT INTO `link` (`name`, `pid`, `member`, `site`, `link`, `episode`) VALUES (%s, %s, %s, %s, %s, %s)"
        mycursor.executemany(command,data)
        self.mydb.commit()