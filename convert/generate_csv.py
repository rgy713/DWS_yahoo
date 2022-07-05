# -*- coding: utf-8 -*-
import csv
import json
from testmodels import const

class Generate_CSV():
    @classmethod
    def main(cls):
        field_item = ['path',
                      'name',
                      'code',
                      'sub-code',
                      'original-price',
                      'price',
                      'sale-price',
                      'options',
                      'headline',
                      'caption',
                      'abstract',
                      'explanation',
                      'additional1',
                      'additional2',
                      'additional3',
                      'relevant-links',
                      'ship-weight',
                      'taxable',
                      'release-date',
                      'temporary-point-term',
                      'point-code',
                      'meta-key',
                      'meta-desc',
                      'template',
                      'sale-period-start',
                      'sale-period-end',
                      'sale-limit',
                      'sp-code',
                      'brand-code',
                      'person-code',
                      'yahoo-product-code',
                      'product-code',
                      'jan',
                      'delivery',
                      'astk-code',
                      'condition',
                      'taojapan',
                      'product-category',
                      'spec1',
                      'spec2',
                      'spec3',
                      'spec4',
                      'spec5',
                      'display',
                      'sort',
                      'sp-additional',
                      'original-price-evidence',
                      'lead-time-instock',
                      'lead-time-outstock']

        fp_item = open(const.CSV_ITEM, 'wb')
        # fp_item.write(u'\ufeff'.encode('utf8'))
        wr_item = csv.writer(fp_item, dialect='excel')
        wr_item.writerow([item for item in field_item])

        with open(const.CSV_ITEM_TRANS) as baseCSV:
            readCSV = csv.DictReader(baseCSV)
            for line in readCSV:
                if line['category_name(j)'] != '':
                    path = line['category_name(j)'].replace('\\',':')
                else:
                    path = line['category_name'].replace('\\', ':')
                if line['product_name(j)'] != '':
                    name = line['product_name(j)']
                else:
                    name = line['product_name']
                code = line['product_id']
                sub_code = ''
                options_size='サイズ|15333'
                options_color='カラー|10011'
                css_list = line['color_size_stock'].split('|')
                css_tran_list = line['color_size_stock(j)'].split('|')
                first_flag = True
                for css,css_tran in zip(css_list, css_tran_list):
                    color = (css.split(':')[0]).lower()
                    size = (css.split(':')[1]).lower()
                    if color != '' or size != '':
                        color_trans=css_tran.split(':')[0]
                        if first_flag == True:
                            one_sub_code = ''
                            first_flag = False
                        else:
                            one_sub_code = '&'
                        one_sub_code_id ='=' + line['product_id']
                        if color_trans != '':
                            one_sub_code += 'カラー:' + color_trans
                            one_sub_code_id += "-" + color
                            # TODO
                            color_id = '10683'
                            options_color += '|' + color_trans + '|' + color_id
                        size_trans = css_tran.split(':')[1]
                        if size_trans != '':
                            one_sub_code += '#サイズ:' + size_trans
                            one_sub_code_id += "-" + size
                            # TODO
                            size_id = '210762'
                            options_size += '|' + size_trans + '|' + size_id
                        one_sub_code += one_sub_code_id
                original_price = line['price']
                price = line['price']
                sale_price = ''
                options = options_size + "|" + options_color
                headline = line['brand_name(j)']
                caption = ''
                abstract = ''
                explanation = line['product_desc(j)']
                additional1 = ''
                additional2 = ''
                additional3 = ''
                relevant_links = ''
                ship_weight = ''
                taxable = 1
                release_date = ''
                temporary_point_term = ''
                point_code = ''
                meta_key = ''
                meta_desc = line['product_name(j)']
                # TODO
                template = 'IT03'
                sale_period_start = ''
                sale_period_end = ''
                sale_limit = ''
                sp_code = ''
                brand_code = ''
                person_code= ''
                yahoo_product_code = ''
                product_code = ''
                jan = ''
                delivery = 1
                astk_code = 0
                condition = 0
                taojapan = 1
                # TODO
                product_category = ''
                spec1 = ''
                spec2 = ''
                spec3 = ''
                spec4 = ''
                spec5 = ''
                display = 0
                sort = ''
                sp_additional = ''
                original_price_evidence = ''
                lead_time_instock = 0
                lead_time_outstock = ''
                row_item = [path, name, code, sub_code, original_price, price, sale_price, options, headline,
                            caption, abstract, explanation, additional1, additional2, additional3, relevant_links,
                            ship_weight, taxable, release_date, temporary_point_term, point_code, meta_key,
                            meta_desc, template, sale_period_start, sale_period_end, sale_limit, sp_code,
                            brand_code, person_code, yahoo_product_code, product_code, jan, delivery, astk_code,
                            condition, taojapan, product_category, spec1, spec2, spec3, spec4, spec5, display, sort,
                            sp_additional, original_price_evidence, lead_time_instock, lead_time_outstock]
                wr_item.writerow([item for item in row_item])
        fp_item.close()
