import scrapy,json


class QuotesSpider(scrapy.Spider):
    name = "test"

    def start_requests(self):
        url = "http://122.114.214.21/python/bin.php"
        yield scrapy.Request(url=url, callback=self.parse,method="POST",body="xxxxxxxxxxxx")

    def parse(self, response):
        file = open("text.txt","r+")
        for res in response.body:
            file.write(str(res))
