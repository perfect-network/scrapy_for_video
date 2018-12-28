import scrapy,json,sys,math


class QuotesSpider(scrapy.Spider):
    name = "test"

    def __init__(self):
        self.cidd = {}

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
                self.cidd[cid] = 1
        print(len(self.cidd))

