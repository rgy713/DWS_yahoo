# -*- coding: utf-8 -*-
import csv
import json
from testmodels.models import TestModels
from testmodels import const

class LangTrans():
    @classmethod
    def main(cls):
        field_trans = ['product_id', 'product_name', 'product_name(j)', 'category_id', 'category_name', 'category_name(j)', 'color_size_stock', 'color_size_stock(j)', 'price', 'product_desc', 'product_desc(j)', 'brand_name', 'brand_name(j)', 'product_url', 'product_img_url']

        fp_trans = open(const.CSV_ITEM_TRANS, 'wb')
        fp_trans.truncate()
        # fp_trans.write(u'\ufeff'.encode('utf8'))
        wr_trans = csv.writer(fp_trans, dialect='excel')
        wr_trans.writerow([item.encode('utf-8') for item in field_trans])

        colorCSV = open(const.CSV_COLOR, 'r')
        color_reader = csv.reader(colorCSV, delimiter=',')
        color_data = {}
        for color_line in color_reader:
            color_data[color_line[1].upper()] = color_line[2]
        colorCSV.close()

        brandCSV = open(const.CSV_BRAND, 'r')
        brand_reader = csv.reader(brandCSV, delimiter=',')
        brand_data = {}
        for brand_line in brand_reader:
            brand_data[brand_line[1].upper()] = brand_line[2]
        brandCSV.close()

        catCSV = open(const.CSV_CAT, 'r')
        cat_reader = csv.reader(catCSV, delimiter=',')
        cat_data = {}
        for cat_line in cat_reader:
            if cat_line[1].strip():
                cat_data[cat_line[1]] = cat_line[2]
            else:
                break
        catCSV.close()

        prod_transCSV = open(const.CSV_PROD_TRANS, 'r')
        prod_reader = csv.reader(prod_transCSV, delimiter=',')
        prod_data = {}
        for prod_line in prod_reader:
            if prod_line[0].strip():
                prod_data[prod_line[0]] = prod_line[2]
            else:
                break
        prod_transCSV.close()

        tmp = TestModels.get_test2_data()
        file_name = const.CSV_ITEMS_PRE_NAME + str(tmp[3])
        with open(file_name) as csvfile:
            readCSV = csv.DictReader(csvfile)
            for line in readCSV:
                color_size_stock_trans = ''
                brand_trans = ''
                cat_trans = ''
                prod_trans = ''
                # color field translate
                if line['color_size_stock'].strip():
                    color_size_stock = line['color_size_stock']
                    css_list = color_size_stock.split('|')
                    flag_first = True
                    for one in css_list:
                        one_split = one.split(':')
                        color = (one_split[0]).upper()
                        color_trans = ''
                        if color != '':
                            if color in color_data:
                                color_trans = color_data[color]
                            else:
                                color_trans = one_split[0]
                        if flag_first == False:
                            color_size_stock_trans += '|'
                        color_size_stock_trans += color_trans + ":" + one_split[1] + ":" + one_split[2]
                        if flag_first == True:
                            flag_first = False

                # brand field translate
                if line['brand_name'].strip():
                    brand_name = line['brand_name'].upper()
                    if brand_name in brand_data:
                        brand_trans = brand_data[brand_name]
                    else:
                        brand_trans = line['brand_name']
                # category name field translate
                if line['category_name'].strip():
                    category_name = line['category_name']
                    if category_name in cat_data:
                        cat_trans = cat_data[category_name]
                    else:
                        cat_trans = line['category_name']

                # product name field translate
                if line['product_name'].strip():
                    product_id = line['product_id']
                    if product_id in prod_data:
                        prod_trans = prod_data[product_id]
                    else:
                        err_list = ['"', 'é', 'è', '®', 'â']
                        rep_list = ['', 'e', 'e', '', 'a']
                        product_name = line['product_name']
                        for er, re in zip(err_list, rep_list):
                            product_name = product_name.replace(er, re)
                        prod_trans = product_name

                row = [line['product_id'], line['product_name'], prod_trans, line['category_id'], line['category_name'],
                               cat_trans, line['color_size_stock'], color_size_stock_trans, line['price'],
                               line['product_desc'], line['product_desc'], line['brand_name'], brand_trans, line['product_url'],
                               line['product_img_url']]
                wr_trans.writerow([item for item in row])
        fp_trans.close()
