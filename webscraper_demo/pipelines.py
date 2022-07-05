# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# Define your item pipelines here
#
from scrapy import log
from twisted.enterprise import adbapi
import csv
from time import gmtime, strftime
# import MySQLdb.cursors
from testmodels.models import TestModels
from testmodels import const

# Database storage pipeline. Adapted from Scrapy docs
# Connects to a MySQL database via a connection pool to allow
# for non blocking DB access

# class DbPipeline(object):
#     def __init__(self):
#         self.dbpool = adbapi.ConnectionPool('MySQLdb',
#                 host='localhost',
#                 db='wc_db',
#                 user='root',
#                 passwd='',
#                 cursorclass=MySQLdb.cursors.DictCursor,
#                 charset='utf8',
#                 use_unicode=True
#                 )
#
#     def process_item(self,item,spider):
#         query = self.dbpool.runInteraction(self.__insertdata, item, spider.name)
#         query.addErrback(self.handle_error)
#         return item
#
#     def __insertdata(self, tx, item, spidername):
#         if item:
#             if ('product_count' and 'find_count') in item :
#                 tx.execute("UPDATE tbl_product_count SET all_product_count=%s, find_product_count=%s where id=%s",
#                            (item['product_count'],item['find_count'],1))
#                 log.msg("Item stored in db", level=log.DEBUG)
#
#     def handle_error(self, e):
#         log.err(e)
class DbSqlitePipeline(object):
    def __init__(self):
        """Initialize"""
        db_name =  const.SQLITE_DB_NAME
        self.__dbpool = adbapi.ConnectionPool('sqlite3',
                database= db_name,
                check_same_thread=False)

    def shutdown(self):
        """Shutdown the connection pool"""
        self.__dbpool.close()

    def process_item(self,item,spider):
        """Process each item process_item"""
        query = self.__dbpool.runInteraction(self.__insertdata, item, spider)
        query.addErrback(self.handle_error)
        return item

    def __insertdata(self,tx,item,spider):
        """Insert data into the sqlite3 database"""
        if item:
            if ('all_product_count' and 'find_product_count' and 'fail_product_count') in item :
                tx.execute("UPDATE tbl_product_count SET all_product_count=?, find_product_count=?, fail_product_count=? where id=?",
                           (item['all_product_count'],item['find_product_count'],item['fail_product_count'],1))
                log.msg("Item stored in db", level=log.DEBUG)
    def handle_error(self,e):
        log.err(e)

class CsvWriterPipeline(object):

    def open_spider(self, spider):
        file_name = const.CSV_ITEMS_TMP_PRE_NAME
        self.item_fp = open(file_name, "wb")
        self.item_fp.truncate()
        self.item_wr = csv.writer(self.item_fp, dialect='excel')
        log.msg("Open items csv file name " + file_name, level=log.DEBUG)

    def process_item(self, item, nfl):
        # build your row to export, then export the row
        if item:
            if ('product_id' and 'product_name' and 'category_id' and 'category_name' and 'color_size_stock' and 'price' and 'product_desc' and 'brand_name' and 'product_url' and 'product_img_url') in item:
                row = [item['product_id'], item['product_name'], item['category_id'], item['category_name'],
                       item['color_size_stock'], item['price'], item['product_desc'], item['brand_name'], item['product_url'],
                       item['product_img_url']]
                self.item_wr.writerow(row)
                log.msg("write item in csv file", level=log.DEBUG)
        return item

    def close_spider(self, spider):
        self.item_fp.close()
        TestModels.set_find_type(const.FIND_SUCCESS)
        log.msg("Close items csv file", level=log.DEBUG)
