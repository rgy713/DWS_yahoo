# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import sqlite3
from testmodels import const
import time
# import MySQLdb

class TestModels():
    db_name = const.SQLITE_DB_NAME

    @classmethod
    def db_connect(self):
        try:
            db = sqlite3.connect(self.db_name)
        except sqlite3.Error:
            time.sleep(0.5)
            db = self.db_connect()
        return db

    # 상태를 기록하는 함수
    # 꺼짐:0, 실행중:1, 성공완료:2, 실패완료:3
    @classmethod
    def set_status(self, status):
        # Open database connection
        db = self.db_connect()

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        # execute SQL query using execute() method.
        cursor.execute("UPDATE tbl_test2 SET status=? WHERE id=?",(status,1))
        db.commit()
        db.close()

    # find_type 설정
    @classmethod
    def set_find_type(self, find_type):
        # Open database connection
        db = self.db_connect()

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        # execute SQL query using execute() method.
        cursor.execute("UPDATE tbl_test2 SET find_type=? WHERE id=?", (find_type, 1))
        db.commit()
        db.close()

    # 화일이름을 기록하는 함수
    @classmethod
    def set_file_name(self, file_name):
        # Open database connection
        db = self.db_connect()

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        # execute SQL query using execute() method.
        cursor.execute( "UPDATE tbl_test2 SET file_name=? WHERE id=?", (file_name,1))
        db.commit()
        db.close()

    @classmethod
    def set_test2_all_data(self, find_type, cur_alphaindex, cur_linkindex, file_name, status):
        # Open database connection
        db = self.db_connect()

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        # execute SQL query using execute() method.
        cursor.execute( "UPDATE tbl_test2 SET find_type=?, current_alphaindex=?, current_linkindex=?, file_name=?, status=? WHERE id=1",
            (find_type, cur_alphaindex, cur_linkindex,file_name,status))
        db.commit()
        db.close()

    @classmethod
    def set_test2_index_data(self, cur_alphaindex, cur_linkindex):
        # Open database connection
        db = self.db_connect()

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        # execute SQL query using execute() method.
        cursor.execute(
            "UPDATE tbl_test2 SET current_alphaindex=?, current_linkindex=? WHERE id=1",
            (cur_alphaindex, cur_linkindex))
        db.commit()
        db.close()

    @classmethod
    def set_test2_linkindex_data(self):
        # Open database connection
        db = self.db_connect()

        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        cursor.execute("SELECT current_linkindex FROM tbl_test2 WHERE id=1")

        data = cursor.fetchone()
        linkindex = int(data[0]) + 1
        # execute SQL query using execute() method.
        cursor.execute(
            "UPDATE tbl_test2 SET current_linkindex=? WHERE id=?",
            (linkindex,1))
        db.commit()
        db.close()

    @classmethod
    def get_test2_data(self):
        # Open database connection
        db = self.db_connect()

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        # execute SQL query using execute() method.
        cursor.execute( "SELECT find_type,current_alphaindex,current_linkindex,file_name,status FROM tbl_test2 WHERE id=1")

        data = cursor.fetchone()
        db.close()
        return data

    # 찾은 상품개수를 초기화하는 함수
    @classmethod
    def set_init_count(self):
        # Open database connection
        db = self.db_connect()

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        # execute SQL query using execute() method.
        cursor.execute("UPDATE tbl_product_count SET all_product_count=?, find_product_count=?, fail_product_count=? where id=?",(0,0,0,1))
        db.commit()
        db.close()

    # 찾은 상품개수를 얻는 함수
    @classmethod
    def get_find_count(self):
        # Open database connection
        db = self.db_connect()

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        # execute SQL query using execute() method.
        cursor.execute("SELECT all_product_count,find_product_count,fail_product_count FROM tbl_product_count WHERE id=1")

        # Fetch a single row using fetchone() method.
        data = cursor.fetchone()
        # disconnect from server
        db.close()
        return data

    # def getMySqlDBData():
    #     # Open database connection
    #     db = MySQLdb.connect("localhost", "root", "", "wc_db")
    #
    #     # prepare a cursor object using cursor() method
    #     cursor = db.cursor()
    #
    #     # execute SQL query using execute() method.
    #     cursor.execute("SELECT all_product_count,find_product_count FROM tbl_product_count WHERE id=1")
    #
    #     # Fetch a single row using fetchone() method.
    #     data = cursor.fetchone()
    #     # disconnect from server
    #     db.close()
    #     return data