# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyweiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    userid = scrapy.Field()
    id = scrapy.Field()
    textContent = scrapy.Field()
    originalContent = scrapy.Field()
    allPicsURL = scrapy.Field()
    like = scrapy.Field()
    comment = scrapy.Field()
    repost = scrapy.Field()
    tag = scrapy.Field()
    image_urls = scrapy.Field()
    postDate = scrapy.Field()
    device = scrapy.Field()

    pass
