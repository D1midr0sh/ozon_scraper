import scrapy


class OzonScrapperSpider(scrapy.Spider):
    name = "ozon_scraper"
    allowed_domains = ["ozon.ru"]
    start_urls = [
        "https://www.ozon.ru/category/smartfony-15502/?sorting=rating"
    ]

    def parse(self, response):
        pass
