# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PetDiseaseItem(scrapy.Item):
    name_str = scrapy.Field()
    cat_id_i = scrapy.Field()
    intr_str = scrapy.Field()
    reason_str = scrapy.Field()
    symptom_str = scrapy.Field()
    standard_str  = scrapy.Field()
    way_str = scrapy.Field()
    add_time_date =  scrapy.Field()
    is_delete_i = scrapy.Field()
    genera_str = scrapy.Field()
    prevention_str = scrapy.Field()
    url_str = scrapy.Field()
    pass