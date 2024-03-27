import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from ozon_scraper.items import OzonScraperItem

from urllib.parse import urlencode


API_KEY = "5ce39613901c3ea43e64f41efd5ab85f"


def proxy(url):
    payload = {"url": url, "api_key": API_KEY}
    return "http://api.scraperapi.com/?" + urlencode(payload)


class OzonScrapperSpider(scrapy.Spider):
    name = "ozon_scraper"
    allowed_domains = ["ozon.ru"]
    start_urls = [
        "https://www.ozon.ru/category/smartfony-15502/?sorting=rating"
    ]
    handle_httpstatus_list = [403]
    general_links = []
    current_page = 1

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=proxy(url), callback=self.parse)

    def parse(self, response: HtmlResponse):
        smartphone_links = response.xpath(
            "//a[@class='tile-hover-target is6 si6']//@href"
        ).extract()
        next_page = f"https://www.ozon.ru/category/smartfony-15502/?page={self.current_page + 1}&sorting=rating"
        for link in smartphone_links:
            self.general_links.append(response.urljoin(link.split("?")[0]))
        if len(self.general_links) < 100:
            self.current_page += 1
            yield scrapy.Request(url=next_page, callback=self.parse)
        else:
            for link in self.general_links[:100]:
                yield scrapy.Request(url=link, callback=self.parse_product)

    def parse_product(self, response: HtmlResponse):
        loader = ItemLoader(item=OzonScraperItem(), response=response)
        loader.add_xpath("os", "//dt[span[contains(text(), 'Операционная')]]/following-sibling::dd")
        loader.add_xpath("ver", "//dt[span[contains(text(), 'Версия')]]/following-sibling::dd")
        yield loader.load_item()
        
