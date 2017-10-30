# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
from Cookie import SimpleCookie

from scrapy import signals
from cookies import cookies
from user_agents import agents


class MyweiboSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class UserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent


class CookiesMiddleware(object):
    """ 换Cookie """

    def process_request(self, request, spider):
        url = request.url
        cookie = random.choice(cookies)
        request.cookies = cookie
        # if url.find("picAll")==-1:
        #     request.cookies = cookie
        # else:
        #     request.cookies.update(cookie)
        # request.cookies.update(cookie)
        # cStr = "_T_WM=1d066e8fd90dd2f475cdfa189ff48b80; SUB=_2A25094CJDeThGeBN41YY8i3JzTWIHXVUGyDBrDV6PUJbkdBeLW_nkW2cHl_ZlVIfuU2cpY9M7kXsez-gcg..; SUHB=0P1cckQgWWlNiF; SCF=AmukTVKs-OXwSD7l8C_LEm4B_UVL-wDVKel6QBHwiQ2Oxxb6MRsGgl8GPW5WXyywFbdC-4m1uStGUD6aQMSv2uw.; SSOLoginState=1509159129; M_WEIBOCN_PARAMS=featurecode%3D20000320%26luicode%3D20000174%26lfid%3Dhotword"
        # pCookie=self.parseStrToCookies(cStr)
        # request.cookies = pCookie

    def parseStrToCookies(self,cookieStr):
        SC = SimpleCookie()
        SC.load(cookieStr)
        cookies = {}
        for key, morsel in SC.items():
            cookies[key] = morsel.value
        return cookies