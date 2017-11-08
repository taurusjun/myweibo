#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import datetime

import re
import scrapy
from Cookie import SimpleCookie

from scrapy import Request

from myweibo.items import MyweiboItem


class Mywbspider01Spider(scrapy.Spider):
    name = 'mywbspider01'
    # allowed_domains = ['url.com']

    # myid:6384923569
    # 2849479587
    # url_tweets = "http://weibo.cn/%s/profile?filter=1&page=1" % ID
    host='https://weibo.cn'
    # start_urls = ['2849479587?page=1']
    weibo_ids=[
        # '2849479587'
        # ,
        # '1762594520', # 肉包山nyako大魔王
        # '5621546867' # 米妮大萌萌mini
        # ,
        # '6364302384' #苏糯米Ml
        # ,
        # '5404464551' # sugar杨晨晨
    ]

    def start_requests(self):
        while self.weibo_ids.__len__():
            wid = self.weibo_ids.pop()
            weiboURL="https://weibo.cn/%s?page=1" % wid
            yield Request(url=weiboURL, meta={"ID": wid}, callback=self.parse0)

    def parse0(self, response):
        myweiboItems = self.parseCttContents(response)
        for itm in myweiboItems:
            allPicURL=itm['allPicsURL']
            if allPicURL:
                yield scrapy.Request(url=allPicURL, meta={'item': itm}, callback=self.parseAllPics)
            else:
                yield itm
            yield itm
        url_next = response.xpath(
            u'body/div[@class="pa" and @id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract_first()
        if url_next:
            yield Request(url=self.host + url_next, meta={"ID": response.meta["ID"]}, callback=self.parse0)
        # return self.parseCttContents(response)


    def parseAllPics(self, response):
        weiboitem = response.meta['item']
        picURLs= response.xpath('//div[@class="c"]//img/@src').extract()
        weiboitem['image_urls'] = picURLs
        return weiboitem


    def parseCttContents(self, response):
        userid = response.meta["ID"]
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
            myweiboItem['userid']=userid
            myweiboItem['id'] = id
            myweiboItem['textContent'] = txtContent
            myweiboItem['originalContent'] = wbContent
            myweiboItem['allPicsURL'] = allPicsURL
            myweiboItem['like'] = like
            myweiboItem['comment'] = comment
            myweiboItem['repost'] = repost
            myweiboItem['tag'] = tag
            m = re.findall(u'(.*)\u6765\u81ea(.*)',tag)
            deviceStr = m[0][1]
            if deviceStr:
                myweiboItem['device'] = deviceStr.strip()
            dateWStr = m[0][0]
            if dateWStr:
                myweiboItem['postDate'] = self.parseDateFromTag(dateWStr)
            yield myweiboItem

    # 日期格式处理，目前只支持4种格式，见代码里面的p1-p4的注释
    def parseDateFromTag(self, dateWStr):
        dt = None
        dateWStr = dateWStr.strip()
        p1 = u'(\d+)\u5206\u949f\u524d'  # 6分钟前
        p2 = u'\u4eca\u5929 (\d+):(\d+)'  # 今天 13:59
        p3 = u'(\d+)\u6708(\d+)\u65e5 (\d+):(\d+)'  # 02月26日 09:11
        p4 = u'(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)'  # 2016-12-11 07:46:05
        try:
            if re.findall(p1, dateWStr).__len__() > 0:
                now = datetime.datetime.now()
                min = re.findall(p1, dateWStr)[0][0]
                dt = now - datetime.timedelta(minutes=int(min))
            else:
                if re.findall(p2, dateWStr).__len__() > 0:
                    now = datetime.datetime.now()
                    match = re.findall(p2, dateWStr)
                    hh = match[0][0]
                    mm = match[0][1]
                    dt = now.replace(hour=int(hh), minute=int(mm))
                else:
                    if re.findall(p3, dateWStr).__len__() > 0:
                        now = datetime.datetime.now()
                        match = re.findall(p3, dateWStr)
                        month = match[0][0]
                        day = match[0][1]
                        hh = match[0][2]
                        mm = match[0][3]
                        dt = now.replace(month=int(month), day=int(day), hour=int(hh), minute=int(mm))
                    else:
                        if re.findall(p4, dateWStr).__len__() > 0:
                            match = re.findall(p4, dateWStr)
                            year = match[0][0]
                            month = match[0][1]
                            day = match[0][2]
                            hh = match[0][3]
                            mm = match[0][4]
                            ss = match[0][5]
                            dt = datetime.datetime(year=int(year), month=int(month), day=int(day),
                                                                        hour=int(hh), minute=int(mm), second=int(ss))
                        else:
                            print "无法处理的日期格式: %s" % dateWStr
        except Exception,e:
            print "Error!%s"%e
        return dt
