import scrapy, math, json, requests, mysql.connector, time


class QuotesSpider(scrapy.Spider):
    name = "qq"
    urls = []
    #action = sys.argv[3].replace("a=","")
    def __init__(self):
        self.file = open("temp.txt", "w")
        self.status = 0
        self.num = 0
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database = "tv"
        )
    '''
    生成全部链接
    '''
    def start_requests(self):
        '''
        PS：因为在腾讯视频web版本的列表只显示5000条信息
        http://v.qq.com/x/list/tv
        所以，如果某个类型的视频总数超过5000时需要加上分类遍历，才能爬全部信息
        而且，某些类型下游许多的预告，但是本程序并不爬预告（主要是纪录片这个类型）
        但是，我也不太确定这种前N个是正片后面都是预告的，是否那N个正片就是这个类型的全部片儿。。。。。。。
        '''
        kind = {
            "movie": {"iyear": ["4330", "4331", "4332", "4333", "4334", "4335", "4336", "4337", "4338"], "sort": "19"},
            "tv": {"iyear": ["2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010", "99"],
                   "sort": "19"},
            "variety": {"sort": "5"},
            "cartoon": {"sort": "19"},
            "children": {"sort": "19"},
            "doco": {"sort": "19"},
            "dv": {"c_category": ["1", "2"], "sort": "19"}
        }
        tid = {
            "movie": 1,
            "tv": 2,
            "variety": 3,
            "cartoon": 4,
            "children": 5,
            "doco": 6,
            "dv": 7
        }
        urls = []
        for key, value in kind.items():
            url1 = []
            url = key + "?"
            for key1, value1 in value.items():
                if isinstance(value1, str):
                    url += key1 + "=" + value1
            for key1, value1 in value.items():
                if isinstance(value1, list):
                    for value2 in value1:
                        url2 = url + "&" + key1 + "=" + value2
                        urls.append(("http://v.qq.com/x/list/" + url2,tid[key]))
                        url1.append("http://v.qq.com/x/list/" + url2)
            if len(url1) == 0:
                urls.append(("http://v.qq.com/x/list/" + url,tid[key]))
        for url in urls:
            yield scrapy.Request(url=url[0], callback=self.list,meta={"tid":url[1]})

    '''
    遍历全部页面（包括加页码的）
    '''
    def list(self, response):
        count = response.css("em.hl::text").extract_first()
        page = math.ceil(int(count) / 30)
        url = response.url
        urls = []
        i = 1
        while (i <= page):
            offset = (i-1) * 30
            url1 = url + "&offset=" + str(offset)
            urls.append(url1)
            i = i + 1
        for url in urls:
            yield scrapy.Request(url=url,callback=self.info,meta=response.meta)

    def info(self, response):
        items = response.css(".list_item")
        url = "http://access.video.qq.com/tinyapp/video_detail?vappid=65939066&vsecret=07c58e0c93150c4254a2a24131574b94cab6142ba4210efa&vversion_name=5.2.0.1234&vplatform=3"
        if len(items)!=0:
            for item in items:
                cid = item.css("li::attr(__wind)").extract()[0].replace("cid=", "")
                data = {'cid': cid}
                db = self.mydb.cursor()
                db.execute("INSERT INTO `tv`.`cid` (`cid`) VALUES ('" + cid + "');")
                self.mydb.commit()
                data = json.dumps(data)
                yield scrapy.Request(url=url,method="POST",body=data,callback=self.info1,meta={"tid":response.meta['tid'],"cid":cid})

    def info1(self,response):
        tid = response.meta['tid']
        body = response.body.decode().replace("data=", "")  # 请求结果，并替换掉其中的多余字符
        data = json.loads(body)  # 序列化，转为dict
        if type(data)==type({}) and "data" in data: # 如果没有请求到正确的数据
            cid = data['data']['cid']
            info = {}  # 定义一个dict类型的变量，将用于存储信息，将传递到下一步，结合下一步获得的信息得到完整的信息
            other = {}  # 储存另外一些信息（非play表的信息）
            introduct = data['data']['introductionMap'][cid]
            detailInfo = {}  # 用于临时存放部分信息
            for item in introduct['detailInfo']:
                if len(item['itemValue']) != 0:
                    if item['itemId']=="total":
                        detailInfo['total1'] = item['itemValue']
                    detailInfo[item['itemId']] = item['itemValue'].replace("更新至", "").replace("集", "").replace("全", "").replace("更新时", "").replace("第", "")
                else:
                    detailInfo[item['itemId']] = item['itemValues']
            if "total" in detailInfo:
                if not "update" in detailInfo or detailInfo['total1'].find("全"):
                    detailInfo['update'] = detailInfo['total']
            if "update" in detailInfo and "total" in detailInfo:
                self.file.write(detailInfo['update'] + "  " + detailInfo['total'] + "  " + cid)
                if int(detailInfo['update']) == int(detailInfo['total']):
                    info['finish'] = "1"
                else:
                    info['finish'] = "0"
            if "year" in detailInfo:
                info['year'] = detailInfo['year']
            if data['data']['defaultVideoDataKey'] in data['data']['videoDataMap']:
                videolist = data['data']['videoDataMap'][data['data']['defaultVideoDataKey']]['videoList']
                for video in videolist:
                    info['picture_hor'] = video['shareItem']['shareImgUrl']
                    break
            performer = []
            for actor in introduct['actorInfo']:
                if actor['title'] == "导 演：":
                    for res in actor['actorInfoList']:
                        if len(res['actorName']) != 0:
                            info['director'] = res['actorName']
                        elif len(res['actorId']) != 0:
                            info['director'] = res['actorId']
            if "intro" in data['data']['actorDataMap']:
                for res in data['data']['actorDataMap']['intro']['actorInfoList']:
                    if len(res['actorName']) != 0:
                        performer.append(res['actorName'])
                    elif len(res['actorId']) != 0:
                        performer.append(res['actorId'])

            other['performer'] = performer
            other['type'] = detailInfo['type']
            if 'poster' in introduct and 'firstLine' in introduct['poster']:
                info['chinese'] = introduct['poster']['firstLine']
            if 'text' in introduct:
                info['description'] = introduct['text']
            if 'poster' in introduct and 'imageUrl' in introduct['poster']:
                info['picture'] = introduct['poster']['imageUrl']
            if 'area' in detailInfo:
                info['region'] = detailInfo['area']
            if "update" in detailInfo and "total" in detailInfo:
                info['current_num'] = detailInfo['update']
                info['total'] = detailInfo['total']
            if 'poster' in introduct and 'rating' in introduct['poster']:
                info['score'] = round(introduct['poster']['rating'] / 10, 1)
            info['addtime'] = round(time.time())
            info['tid'] = tid
            #------------------第二-------------------
            episode = []
            lastid = ""
            thisid = "x"
            link = []
            links = {}
            while lastid != thisid:
                thisid = lastid
                if thisid:
                    vid = "vid=" + thisid
                else:
                    vid = ""
                data = {'dataKey': "req_type=2&lid=&cid=" + cid + "&vid=&ui=0", 'pageContext': vid}
                data = json.dumps(data)
                rep = requests.post(
                    url="http://access.video.qq.com/tinyapp/detail_video_list?vappid=65939066&vsecret=07c58e0c93150c4254a2a24131574b94cab6142ba4210efa&vversion_name=5.2.0.1234&vplatform=3",
                    data=data)
                body = rep.content.decode().replace("data=", "")  # 请求结果，并替换掉其中的多余字符
                data = json.loads(body)  # 序列化，转为dict
                for res in data['data']['videoList']:
                    if not res['isTrailor'] and not res['poster']['firstLine'] in links:  # 过滤掉预告与已经存在的视频
                        if int(res['payStatus']) == 8:
                            member = 0
                        else:
                            member = 1
                        episode.append({"episode": res['poster']['firstLine'], "member": member})
                        links[res['poster']['firstLine']] = "1"
                        link.append({
                            "episode": res['poster']['firstLine'],
                            "member": member,
                            'image': res['poster']['imageUrl'],
                            'name': res['title'],
                            'start': res['skipStart'],
                            'end': res['skipEnd'],
                            'site': "qq",
                            'link': cid + "/" + res['vid']
                        })
                    lastid = res['vid']
            info['site'] = {}
            info['site']['qq'] = episode
            self.info2({"info":info,"other":other,"link":link,"cid":cid})

    def info2(self,response):
        state = 0
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
        db = self.mydb.cursor()
        command = "SELECT * FROM  `play` WHERE  `chinese` LIKE  '" + response['info']['chinese'] + "' AND  `tid` =" + str(response['info']['tid'])
        db.execute(command)
        if not db.fetchone() and len(response['link'])!=0:
            # -------------------增加此影片基本信息----------------------
            command = "INSERT INTO `tv`.`play` (" + sql1 + ") VALUES (" + sql2 + ")"
            db.execute(command, data)
            if db.rowcount==1:
                state = 1
            self.mydb.commit()
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
                i = 0
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
            self.mydb.commit()
            # ---------------------------------------------------------------

            # ---------------------------------------------------------------
            if len(response['other']['type']) != 0:
                type_data = []
                for res in response['other']['type']:
                    type_data.append((res, playid))
                command = "INSERT INTO `tv`.`classify` (`value`,`pid`) VALUES (%s,%s)"
                db.executemany(command, type_data)
                self.mydb.commit()
            if len(response['other']['performer']) != 0:
                performer_data = []
                for res in response['other']['performer']:
                    performer_data.append((res, playid))
                command = "INSERT INTO `tv`.`performer` (`name`,`pid`) VALUES (%s,%s)"
                db.executemany(command, performer_data)
                self.mydb.commit()
            if state==1:
                db.execute("UPDATE  `tv`.`cid` SET  `status` =  '1' WHERE  `cid` = '"+ response['cid'] +"';")
                self.mydb.commit()
                self.num = self.num + 1
                arr = ["电影","电视剧","综艺","动漫","少儿","纪录片","微电影"]
                print(self.num,"入库成功",arr[int(info['tid']-1)],info['chinese'],"一共有"+ str(len(response['link'])) + "条视频",response['cid'])
            else:
                print("入库失败",response['cid'])











