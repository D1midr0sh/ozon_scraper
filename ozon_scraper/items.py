import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags


def clear(s: str):
    ans = s.replace("(EMUI 12)", "").replace(".x", "").strip()
    return ans.split()[-1]


class OzonScraperItem(scrapy.Item):
    os = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    ver = scrapy.Field(input_processor=MapCompose(remove_tags, clear), output_processor=TakeFirst())
