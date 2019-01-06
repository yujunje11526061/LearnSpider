# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, Response, FormRequest
from traceback import format_exc
from scrapy import Selector
from LearnScrapy.items import XiaoquItem, SellingItem, RentingItem
from pyquery import PyQuery


class SpiderCity58Spider(scrapy.Spider):
    name = 'spider_city_58'
    allowed_domains = ['58.com']
    # start_urls = ['http://58.com/']
    url = 'https://hz.58.com/xiaoqu/'
    xiaoquPageNum = 2
    sellingPageNum = 2
    rentingPageNum = 2

    def start_requests(self):
        return [Request(self.url, callback=self.parse, errback=self.error_back, priority=10)]

    def parse(self, response):
        self.logger.debug('获取各行政区小区页面')
        sel = Selector(text=response.text)
        zoneList = sel.css('body > div.main-wrap > div.filter-wrap > dl:nth-child(1) > dd > a::attr(value)').extract()[
                   1:]
        zoneNameList = sel.css('body > div.main-wrap > div.filter-wrap > dl:nth-child(1) > dd > a::text').extract()[1:]
        for zone, zoneName in zip(zoneList, zoneNameList):
            yield Request(self.url + zone + '/',
                          callback=self.get_xiaoqu_list,
                          errback=self.error_back,
                          meta={'zoneName': zoneName.strip(), 'page': 1},
                          priority=9
                          )

    def get_xiaoqu_list(self, response):
        page = response.meta['page']
        meta = response.meta
        if page < self.xiaoquPageNum:
            url = response.url + '/pn_{}/'.format(page + 1)
            meta['page'] += 1
            yield Request(url,
                          callback=self.get_xiaoqu_list,
                          errback=self.error_back,
                          meta=meta,
                          priority=9
                          )

        sel = Selector(text=response.text)
        xiaoqu_list = sel.css(
            'body > div.main-wrap > div.content-wrap > div.content-side-left > ul > li > div.list-info > h2 > a::attr(href)').extract()
        for xiaoqu_url in xiaoqu_list:
            yield Request(xiaoqu_url,
                          callback=self.get_xiaoqu_info,
                          errback=self.error_back,
                          meta={'zoneName': meta['zoneName']},
                          priority=8
                          )

    def get_xiaoqu_info(self, response):
        item = XiaoquItem()
        sel = Selector(text=response.text)
        item['zone'] = response.meta['zoneName']
        item['name'] = sel.css('body > div.body-wrapper > div.title-bar > span.title::text').extract_first()
        item['year'] = sel.css(
            'body > div.body-wrapper > div.basic-container > div.info-container > div.info-tb-container > table tr:nth-child(5) > td:nth-child(2)::text').extract_first().strip()
        item['greenRatio'] = sel.css(
            'body > div.body-wrapper > div.basic-container > div.info-container > div.info-tb-container > table tr:nth-child(5) > td:nth-child(4)::text').extract_first().strip()
        item['parkingSpot'] = sel.css(
            'body > div.body-wrapper > div.basic-container > div.info-container > div.info-tb-container > table tr:nth-child(7) > td.desc::text').extract_first().strip()
        item['avgPrice'] = sel.css(
            'body > div.body-wrapper > div.basic-container > div.info-container > div.price-container > span.price::text').extract_first().strip()
        item['totArea'] = sel.css(
            'body > div.body-wrapper > div.basic-container > div.info-container > div.info-tb-container > table tr:nth-child(6) > td:nth-child(4)::text').extract_first().strip()
        item['sellingNumber'] = sel.css('tr td.desc span::text').extract()[0].strip('套')
        item['rentingNumber'] = sel.css('tr td.desc span::text').extract()[1].strip('套')

        self.logger.debug(item)
        yield item

        pqsel = PyQuery(response.text)
        if item['rentingNumber'] != '0':
            renting_url = pqsel(
                'body > div.body-wrapper > div.basic-container > div.info-container > div.info-tb-container > table tr.tb-btm > td:nth-child(4) > a').attr(
                'href')
            yield Request('https:' + renting_url,
                          callback=self.get_renting_info,
                          errback=self.error_back,
                          meta={'zone': item['zone'], 'name': item['name']},
                          priority=8
                          )
        if item['sellingNumber'] != '0':
            selling_url = pqsel(
                'body > div.body-wrapper > div.basic-container > div.info-container > div.info-tb-container > table tr.tb-btm > td:nth-child(2) > a').attr(
                'href')
            yield Request('https:' + selling_url,
                          callback=self.get_selling_info,
                          errback=self.error_back,
                          meta={'zone': item['zone'], 'name': item['name']},
                          priority=8
                          )

    def get_selling_info(self, response):
        sel = Selector(text = response.text)
        totPriceList = sel.css('tr > td.tc>b::text').extract()
        totPriceList = [n+'万' for n in totPriceList]
        priceList = sel.css('tr > td.tc > span:nth-child(3)::text').extract()
        areaList = sel.css('tr > td.tc > span:nth-child(5)::text').extract()
        descriptionList = sel.css('tr > td.t > a.t::text').extract()
        zone = response.meta['zone']
        xiaoqu = response.meta['name']
        for totPrice, price, area, description in zip(totPriceList,priceList,areaList,descriptionList):
            item = SellingItem()
            item['zone'] = zone
            item['xiaoqu'] = xiaoqu
            item['totPrice'] = totPrice
            item['price'] = price
            item['area'] = area
            item['description'] = description
            self.logger.debug(item)
            yield item


    def get_renting_info(self, response):
        sel = Selector(text=response.text)
        descriptionList = sel.css('tr > td.t > a.t::text').extract()
        pricePerMonthList = sel.css('tr > td.tc > b::text').extract()
        pricePerMonthList = [p+'元/月' for p in pricePerMonthList]
        zone = response.meta['zone']
        xiaoqu = response.meta['name']
        for pricePerMonth, description in zip(pricePerMonthList,descriptionList):
            item = RentingItem()
            item['zone'] =zone
            item['xiaoqu'] = xiaoqu
            item['pricePerMonth'] = pricePerMonth
            item['description'] = description
            self.logger.debug(item)
            yield item

    def error_back(self,e):
        self.logger.error(format_exc())
        return


if __name__ == '__main__':
    import requests

    spider = SpiderCity58Spider()
    response = requests.get(url=spider.url)
    print(response)
    for r in spider.parse(response):
        print(r, r.meta['zoneName'])
