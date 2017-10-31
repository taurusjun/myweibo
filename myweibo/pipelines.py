# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline


class MyweiboPipeline(object):
    def process_item(self, item, spider):
        return item


class MyImagesPipeline(ImagesPipeline):
    """先安装：pip install Pillow"""

    def get_media_requests(self, item, info):
        return [Request(x, meta={"item":item}) for x in item.get(self.images_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        picURL = request.url
        picName= picURL[picURL.rfind("/")+1:]
        item = request.meta['item']
        userid = item['userid']
        weiboId=item['id']
        path = '%s/%s|%s' % (userid,weiboId,picName)
        return path