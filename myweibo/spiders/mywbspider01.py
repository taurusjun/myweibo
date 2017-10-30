#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import datetime

import re
import scrapy
from Cookie import SimpleCookie

from myweibo.items import MyweiboItem


class Mywbspider01Spider(scrapy.Spider):
    name = 'mywbspider01'
    # allowed_domains = ['url.com']

    # myid:6384923569
    # 2849479587
    # url_tweets = "http://weibo.cn/%s/profile?filter=1&page=1" % ID
    start_urls = ['https://weibo.cn/2849479587?page=1']

    def parse(self, response):
        myweiboItems = self.parseCttContents(response)
        for itm in myweiboItems:
            allPicURL=itm['allPicsURL']
            if allPicURL:
                yield scrapy.Request(url=allPicURL, meta={'item': itm}, callback=self.parseAllPics)
            else:
                yield itm
            yield itm
        # return self.parseCttContents(response)


    def parseAllPics(self, response):
        weiboitem = response.meta['item']
        for picURL in response.xpath('//div[@class="c"]//img/@src'):
            print 1
        pass


    def parseCttContents(self, response):
        pathExp = '//div[@class="c"][not(descendant::span[@class="kt"]) and (descendant::span[@class="ctt"])]'
        # '//div[@class="c"]/*[descendant::span[@class="ctt"]]'
        cttHtmls = response.xpath(pathExp)
        for sel in cttHtmls:
            # 内容
            id = sel.xpath('@id').extract_first()  # 微博ID
            txtContent = sel.xpath('div/span[@class="ctt"]/text()').extract_first()
            wbContent = re.findall('<span.*?>(.*?)</span>', sel.xpath('div/span[@class="ctt"]').extract_first())[0]
            # wbContent = sel.xpath('div/span[@class="ctt"]').re('<span class="ctt">(.*?)<\/span>')
            # wbContent = sel.xpath('div[descendant::span[@class="ctt"]]').re('<div>(.*?)<\/div>')[0]
            # u'https://weibo.cn/mblog/picAll/Fs3Wtu746?rl=1'
            allPicsURL = sel.xpath('div/a[contains(@href,"picAll")]/@href').extract_first()
            # u'赞[267]'
            oLike = re.findall('\[(.*?)\]', sel.xpath('div/a[contains(@href,"attitude")]/text()').extract_first())
            if oLike:
                like = oLike[0]
            else:
                like=0
            # like = sel.xpath('div/a[contains(@href,"attitude")]/text()').re('\[(.*?)\]')
            # u'评论[111]'
            oComment = re.findall('\[(.*?)\]', sel.xpath('div/a[contains(@href,"comment")]/text()').extract_first())
            if oComment:
                comment = oComment[0]
            else:
                comment=0
            # comment = sel.xpath('div/a[contains(@href,"comment")]/text()').re('\[(.*?)\]')
            # u'转发[9]'
            oRepost = re.findall('\[(.*?)\]', sel.xpath('div/a[contains(@href,"repost")]/text()').extract_first())
            if oRepost:
                repost = oRepost[0]
            else:
                repost=0
            # repost = sel.xpath('div/a[contains(@href,"repost")]/text()').re('\[(.*?)\]')
            # u'10月25日 23:38 来自iPhone 7 Plus'
            tag = sel.xpath('div/span[@class="ct"]/text()').extract_first()
            # ctag = sel.xpath('div/span[@class="ct"]/text()').re(u'(.*?)\u6708(.*?)\u65e5 ([0-2][0-9]:[0-6][0-9])(.*)')
            print "id: %s\ntext: %s\ncontent: %s\npics: %s \nlike: %s \ncomment: %s \nrepost: %s \ntag: %s" % (id,txtContent,wbContent,allPicsURL,like,comment,repost,tag)
            print "\n"
            myweiboItem = MyweiboItem()
            myweiboItem['id'] = id
            myweiboItem['textContent'] = txtContent
            myweiboItem['originalContent'] = wbContent
            myweiboItem['allPicsURL'] = allPicsURL
            myweiboItem['like'] = like
            myweiboItem['comment'] = comment
            myweiboItem['repost'] = repost
            myweiboItem['tag'] = tag
            yield myweiboItem

