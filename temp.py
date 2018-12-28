for item in items:
    cid = item.css("li::attr(__wind)").extract()[0].replace("cid=", "")
    data = {'cid': cid}
    tid = response.meta['tid']
    data = json.dumps(data)
    rep = requests.post(
        url="http://access.video.qq.com/tinyapp/video_detail?vappid=65939066&vsecret=07c58e0c93150c4254a2a24131574b94cab6142ba4210efa&vversion_name=5.2.0.1234&vplatform=3",
        data=data)
    body = rep.content.decode().replace("data=", "")  # 请求结果，并替换掉其中的多余字符
    data = json.loads(body)  # 序列化，转为dict
    info = {}  # 定义一个dict类型的变量，将用于存储信息，将传递到下一步，结合下一步获得的信息得到完整的信息
    other = {}  # 储存另外一些信息（非play表的信息）
    introduct = data['data']['introductionMap'][cid]
    detailInfo = {}  # 用于临时存放部分信息
    for item in introduct['detailInfo']:
        if len(item['itemValue']) != 0:
            detailInfo[item['itemId']] = item['itemValue'].replace("更新至", "").replace("集", "").replace("全", "")
        else:
            detailInfo[item['itemId']] = item['itemValues']
    if "total" in detailInfo:
        if not "update" in detailInfo:
            detailInfo['update'] = detailInfo['total']
    if "update" in detailInfo and "total" in detailInfo:
        if int(detailInfo['update']) == int(detailInfo['total']):
            info['finish'] = "1"
        else:
            info['finish'] = "0"
    if "year" in detailInfo:
        info['year'] = detailInfo['year']
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
        # elif actor['title']=="主 演：":
        #     for res in actor['actorInfoList']:
        #         if len(res['actorName']) != 0:
        #             performer.append(res['actorName'])
        # 下面的代码替换这里的代码，这里的代码 当 cid=9muu93hgnc8z5xa 时 会出现主演名称为数字的（其实根本没有，是一个id罢了，下面的代码不会出现）
    for res in data['data']['actorDataMap']['intro']['actorInfoList']:
        if len(res['actorName']) != 0:
            performer.append(res['actorName'])
        elif len(res['actorId']) != 0:
            performer.append(res['actorId'])

    other['performer'] = performer
    other['type'] = detailInfo['type']
    info['chinese'] = introduct['poster']['firstLine']
    info['description'] = introduct['text']
    info['picture'] = introduct['poster']['imageUrl']
    info['region'] = detailInfo['area']
    if "update" in detailInfo and "total" in detailInfo:
        info['current_num'] = detailInfo['update']
        info['total'] = detailInfo['total']
    info['score'] = round(introduct['poster']['rating'] / 10, 1)
    info['addtime'] = round(time.time())
    info['tid'] = tid

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


