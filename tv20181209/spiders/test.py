import scrapy,json,sys


class QuotesSpider(scrapy.Spider):
    name = "test"
    def start_requests(self):
        url = "http://v.qq.com/x/list/tv?offset=0&sort=19"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        count = response.css("em.hl::text").extract_first()
        print(response.url)

