# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field
from scrapy.http import Request, Response


class LearnscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()  # Field类继承自dict
    pass

class XiaoquItem(scrapy.Item):
    zone = Field()
    name = Field()
    year = Field()
    greenRatio = Field()
    parkingSpot = Field()
    avgPrice = Field()
    totArea = Field()
    sellingNumber = Field()
    rentingNumber = Field()

class SellingItem(scrapy.Item):
    zone = Field()
    xiaoqu = Field()
    totPrice = Field()
    price = Field()
    area = Field()
    description = Field()


class RentingItem(scrapy.Item):
    zone = Field()
    xiaoqu = Field()
    pricePerMonth = Field()
    description = Field()
