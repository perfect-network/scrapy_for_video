import scrapy,json,sys,math


class QuotesSpider(scrapy.Spider):
    name = "test"


    def start_requests(self):
        url = "http://access.video.qq.com/tinyapp/video_detail?vappid=65939066&vsecret=07c58e0c93150c4254a2a24131574b94cab6142ba4210efa&vversion_name=5.2.0.1234&vplatform=3"
        cid = ""
        tid = 1
        data = {'cid': cid}
        db = self.mydb.cursor()
        db.execute("INSERT INTO `tv`.`cid` (`cid`) VALUES ('" + cid + "');")
        self.mydb.commit()
        data = json.dumps(data)
        yield scrapy.Request(url=url,method="POST",body=data,callback=self.info1,meta={"tid":tid,"cid":cid})