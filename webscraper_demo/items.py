# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class WebscraperDemoItem(scrapy.Item):
    # define the fields for your item here like:
    all_product_count = scrapy.Field()
    find_product_count = scrapy.Field()
    fail_product_count = scrapy.Field()

    product_id = scrapy.Field()
    product_name = scrapy.Field()
    category_id = scrapy.Field()
    category_name = scrapy.Field()
    color_size_stock = scrapy.Field()
    price = scrapy.Field()
    product_desc = scrapy.Field()
    brand_name = scrapy.Field()
    product_url = scrapy.Field()
    product_img_url = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()