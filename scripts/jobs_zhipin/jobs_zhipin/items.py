# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobsZhipinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_name = scrapy.Field() 
    company_name = scrapy.Field() 
    company_image_url = scrapy.Field() 
    city = scrapy.Field() 
    jobyear = scrapy.Field() 
    education = scrapy.Field() 
    financing = scrapy.Field() 
    num_of_people = scrapy.Field() 
    field = scrapy.Field() 
    pay = scrapy.Field() 
