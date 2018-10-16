# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EsabnaItem(scrapy.Item):
    # define the fields for your item here like:
    product_detail = scrapy.Field()
    introduction = scrapy.Field()
    headings= scrapy.Field()
    industries_welding= scrapy.Field()
    welding_process= scrapy.Field()
    elements = scrapy.Field()
    values = scrapy.Field()
 
