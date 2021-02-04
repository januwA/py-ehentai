# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EhentaiItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    page = scrapy.Field()
    img = scrapy.Field()
