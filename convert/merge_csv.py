# -*- coding: utf-8 -*-
import csv
from testmodels import const
from testmodels.models import TestModels
from time import gmtime, strftime

class MergeCsv():
    @classmethod
    def mycsv_reader(cls,csv_reader):
        while True:
            try:
                yield next(csv_reader)
            except csv.Error:
                # error handling what you want.
                pass
            continue

    @classmethod
    def items_merge(cls):
        tmp = TestModels.get_test2_data()
        file_date_name = str(tmp[3])
        items_file_name = const.CSV_ITEMS_PRE_NAME + file_date_name
        items_file = open(items_file_name, 'ab')
        writer = csv.writer(items_file, dialect='excel')
        tmp_items_file_name = const.CSV_ITEMS_TMP_PRE_NAME
        tmp_items_file = open(tmp_items_file_name, 'rb')
        reader = cls.mycsv_reader(csv.reader(tmp_items_file, dialect='excel'))
        for row in reader:
            writer.writerow(row)
        tmp_items_file.close()
        items_file.close()

    @classmethod
    def main(cls):
        # 초기화
        file_date_name = strftime("%Y_%m_%d_%H_%M_%S", gmtime()) + '.csv'
        file_name = const.CSV_ITEMS_PRE_NAME + file_date_name
        fp = open(file_name, "wb")
        fp.truncate()
        wr = csv.writer(fp, dialect='excel')
        # fp.write(u'\ufeff'.encode('utf8'))
        field = ['product_id', 'product_name', 'category_id', 'category_name', 'color_size_stock', 'price', 'product_desc', 'brand_name', 'product_url', 'product_img_url']
        wr.writerow([elem.encode('utf-8') for elem in field])
        fp.close()
        TestModels.set_file_name(file_date_name)

        cls.items_merge()