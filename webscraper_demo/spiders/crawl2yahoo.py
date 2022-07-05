# -*- coding: utf-8 -*-
import scrapy
from webscraper_demo.items import WebscraperDemoItem
import re
import json
from scrapy.http import FormRequest
from scrapy.selector import Selector
import base64
import time
# from . import data
from testmodels import const
from testmodels.models import TestModels
import hashlib
from scrapy.utils.python import to_bytes

class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'crawl2yahoo'
    base_url = "http://www.neimanmarcus.com"
    first_url = "http://www.neimanmarcus.com/en-jp/index.jsp"
    all_count = 0
    find_count = 0
    fail_count = 0
    page_size = 120

    def start_requests(self):
        # '{"RWD.deferredContent.DeferredContentReqObj":{"contentPath":"/page_rwd/header/silos/silos.jsp","category":"cat000000","cacheKey":"r_responsiveDrawersHeader_JP_en"}}'
        data = "$b64$eyJSV0QuZGVmZXJyZWRDb250ZW50LkRlZmVycmVkQ29udGVudFJlcU9iaiI6eyJjb250ZW50UGF0aCI6Ii9wYWdlX3J3ZC9oZWFkZXIvc2lsb3Mvc2lsb3MuanNwIiwiY2F0ZWdvcnkiOiJjYXQwMDAwMDAiLCJjYWNoZUtleSI6InJfcmVzcG9uc2l2ZURyYXdlcnNIZWFkZXJfSlBfZW4ifX0$"
        post_url = self.base_url + "/en-jp/deferred.service"
        timestamp = str(time.time() * 1000)
        formdata = {'data': data,
                    'sid': 'getResponse',
                    'bid': 'DeferredContentReqObj',
                    'timestamp': timestamp}
        yield FormRequest(url=post_url, formdata=formdata, callback=self.parse_menubar)

    def parse_menubar(self, response):

        def extract_var(text,reg):
            return re.search(reg, text).groups()[0]

        TestModels.set_find_type(const.FIND_PROGRESS)
        
        href_all_list = []
        category_list = []
        json_data = json.loads(response.body)
        resp = Selector(text=json_data.get('RWD.deferredContent.DeferredContentRespObj', '').get('content', ''))

        # Women's Apparel , Shoes, Handbags
        # silo_id=[2,4,5]
        # cat0="Women's"
        # cat1_array = ['Apparel','Shoes','Handbags']
        # for id, cat1 in zip(silo_id, cat1_array):
        #     silo_li='//li[@id="silo' + str(id) + '"]//div[@class="silo-column"]'
        #     categories = resp.xpath(silo_li)[1]
        #     href_list = categories.xpath('.//ul//a/@href').extract()
        #     first = True
        #     for href in href_list:
        #         if first:
        #             first = False
        #             continue
        #         href_all_list.append(href)
        #         cat2 = extract_var(href,r"en-jp/(.*?)/cat")
        #         category = cat0 + "\\" + cat1 +"\\" + str(cat2).replace("/", "\\")
        #         category_list.append(category)
        #
        # #Jewelry & Accessories
        # silo_li = '//li[@id="silo6"]//div[@class="silo-column"]'
        # categories = resp.xpath(silo_li)[1]
        # href_list = categories.xpath('.//ul//a/@href').extract()
        # first = True
        # for href in href_list:
        #     if first:
        #         first = False
        #         continue
        #     href_all_list.append(href)
        #     cat2 = extract_var(href, r"en-jp/(.*?)/cat")
        #     category = cat0 + "\\" + str(cat2).replace("/", "\\")
        #     category_list.append(category)
        #
        # categories = resp.xpath(silo_li)[2]
        # href_list = categories.xpath('.//ul//a/@href').extract()
        # first = True
        # for href in href_list:
        #     if first:
        #         first = False
        #         continue
        #     href_all_list.append(href)
        #     cat2 = extract_var(href, r"en-jp/(.*?)/cat")
        #     category = cat0 + "\\" + str(cat2).replace("/", "\\")
        #     category_list.append(category)
        #
        # href_list = categories.xpath('.//h6//a/@href').extract()
        # first = True
        # cat1 = "Accessories"
        # for href in href_list:
        #     if first:
        #         first = False
        #         continue
        #     href_all_list.append(href)
        #     cat2 = extract_var(href, r"Accessories/(.*?)/cat")
        #     category = cat0 + "\\" + cat1 + "\\" + str(cat2).replace("/", "\\")
        #     category_list.append(category)
        #
        # # Beauty
        # silo_li = '//li[@id="silo7"]//div[@class="silo-column"]'
        # categories = resp.xpath(silo_li)[1]
        # all_beauty = str(categories.xpath('.//h6//a/text()').extract()[0])
        # cat1 = "Beauty"
        # if all_beauty == ' All Beauty ':
        #     ul_list = categories.xpath('.//ul')[0]
        #     href_list = ul_list.xpath('.//a/@href').extract()
        #     for href in href_list:
        #         href_all_list.append(href)
        #         cat2 = extract_var(href, r"en-jp/(.*?)/cat")
        #         category = cat0 + "\\" + cat1 + "\\" + str(cat2).replace("/", "\\")
        #         category_list.append(category)
        #
        #     ul_list = categories.xpath('.//ul')[1]
        #     href_list = ul_list.xpath('.//a/@href').extract()
        #     for href in href_list:
        #         href_all_list.append(href)
        #         cat2 = extract_var(href, r"en-jp/(.*?)/cat")
        #         category = cat0 + "\\" + cat1 + "\\" + str(cat2).replace("/", "\\")
        #         category_list.append(category)
        #     cat0 = "Men's"
        #     cat1 = "Cologne-Grooming"
        #     ul_list = categories.xpath('.//ul')[2]
        #     href_list = ul_list.xpath('.//a/@href').extract()
        #     for href in href_list:
        #         href_all_list.append(href)
        #         cat2 = extract_var(href, r"Cologne-Grooming/(.*?)/cat")
        #         category = cat0 + "\\" + cat1 + "\\" + str(cat2).replace("/", "\\")
        #         category_list.append(category)
        #
        #     cat0 = "Women's"
        #     href_list = categories.xpath('.//h6//a/@href').extract()
        #     href_all_list.append(href_list[2])
        #     cat2 = extract_var(href_list[2], r"en-jp/(.*?)/cat")
        #     category = cat0 + "\\"  + str(cat2).replace("/", "\\")
        #     category_list.append(category)
        #     href_all_list.append(href_list[4])
        #     cat2 = extract_var(href_list[4], r"en-jp/(.*?)/cat")
        #     category = cat0 + "\\"  + str(cat2).replace("/", "\\")
        #     category_list.append(category)
        #     href_all_list.append(href_list[5])
        #     cat2 = extract_var(href_list[5], r"en-jp/(.*?)/cat")
        #     category = cat0 + "\\" + str(cat2).replace("/", "\\")
        #     category_list.append(category)
        # else:
        #     categories = resp.xpath(silo_li)[0]
        #     ul_list = categories.xpath('.//ul')[1]
        #     href_list = ul_list.xpath('.//a/@href').extract()
        #     for href in href_list:
        #         href_all_list.append(href)
        #         cat2 = extract_var(href, r"en-jp/(.*?)/cat")
        #         category = cat0 + "\\" + cat1 + "\\" + str(cat2).replace("/", "\\")
        #         category_list.append(category)
        #
        #     ul_list = categories.xpath('.//ul')[2]
        #     href_list = ul_list.xpath('.//a/@href').extract()
        #     for href in href_list:
        #         href_all_list.append(href)
        #         cat2 = extract_var(href, r"en-jp/(.*?)/cat")
        #         category = cat0 + "\\" + cat1 + "\\" + str(cat2).replace("/", "\\")
        #         category_list.append(category)
        #
        #     ul_list = categories.xpath('.//ul')[3]
        #     href_list = ul_list.xpath('.//a/@href').extract()
        #     cat0 = "Men's"
        #     cat1 = "Cologne-Grooming"
        #     for href in href_list:
        #         href_all_list.append(href)
        #         cat2 = extract_var(href, r"Cologne-Grooming/(.*?)/cat")
        #         category = cat0 + "\\" + cat1 + "\\" + str(cat2).replace("/", "\\")
        #         category_list.append(category)
        #
        #     cat0 = "Women's"
        #     href_list = categories.xpath('.//h6//a/@href').extract()
        #     href_all_list.append(href_list[4])
        #     cat2 = extract_var(href_list[4], r"en-jp/(.*?)/cat")
        #     category = cat0 + "\\" + str(cat2).replace("/", "\\")
        #     category_list.append(category)
        #     href_all_list.append(href_list[6])
        #     cat2 = extract_var(href_list[6], r"en-jp/(.*?)/cat")
        #     category = cat0 + "\\" + str(cat2).replace("/", "\\")
        #     category_list.append(category)
        #     href_all_list.append(href_list[7])
        #     cat2 = extract_var(href_list[7], r"en-jp/(.*?)/cat")
        #     category = cat0 + "\\" + str(cat2).replace("/", "\\")
        #     category_list.append(category)
        #
        # # The Man's Store
        # cat0 = "Men's"
        # silo_li = '//li[@id="silo8"]//div[@class="silo-column"]'
        # categories = resp.xpath(silo_li)[1]
        # href_list = categories.xpath('.//ul//a/@href').extract()
        # for href in href_list:
        #     href_all_list.append(href)
        #     cat2 = extract_var(href, r"en-jp/(.*?)/cat")
        #     category = cat0 + "\\" + str(cat2).replace("/", "\\")
        #     category_list.append(category)
        #
        # categories = resp.xpath(silo_li)[2]
        # href_list = categories.xpath('.//ul//a/@href').extract()
        # for href in href_list:
        #     href_all_list.append(href)
        #     cat2 = extract_var(href, r"en-jp/(.*?)/cat")
        #     category = cat0 + "\\" + str(cat2).replace("/", "\\")
        #     category_list.append(category)
        #NM Kids
        cat0 = "Kids"
        silo_li = '//li[@id="silo9"]//div[@class="silo-column"]'
        categories = resp.xpath(silo_li)[0]
        ul_list = categories.xpath('.//ul')[0]
        href_list = ul_list.xpath('.//a/@href').extract()
        for href in href_list:
            href_all_list.append(href)
            cat2 = extract_var(href, r"en-jp/(.*?)/cat")
            category = cat0 + "\\" + str(cat2).replace("/", "\\")
            category_list.append(category)

        # categories = resp.xpath(silo_li)[1]
        # href_list = categories.xpath('.//ul//a/@href').extract()
        # for href in href_list:
        #     href_all_list.append(href)
        #     cat2 = extract_var(href, r"en-jp/(.*?)/cat")
        #     category = cat0 + "\\" + str(cat2).replace("/", "\\")
        #     category_list.append(category)
        # categories = resp.xpath(silo_li)[2]
        # href_list = categories.xpath('.//ul//a/@href').extract()
        # for href in href_list:
        #     href_all_list.append(href)
        #     cat2 = extract_var(href, r"en-jp/(.*?)/cat")
        #     category = cat0 + "\\" + str(cat2).replace("/", "\\")
        #     category_list.append(category)
        # href_list = categories.xpath('.//h6//a/@href').extract()
        # href_all_list.append(href_list[1])
        # cat2 = extract_var(href_list[1], r"Kids/(.*?)/cat")
        # category = cat0 + "\\" + str(cat2).replace("/", "\\")
        # category_list.append(category)
        #
        # # Home
        # cat0 = "Home"
        # silo_li = '//li[@id="silo10"]//div[@class="silo-column"]'
        # categories = resp.xpath(silo_li)[0]
        # href_list = categories.xpath('.//ul//a/@href').extract()
        # for href in href_list:
        #     href_all_list.append(href)
        #     cat2 = extract_var(href, r"en-jp/(.*?)/cat")
        #     category = cat0 + "\\" + str(cat2).replace("/", "\\")
        #     category_list.append(category)
        # categories = resp.xpath(silo_li)[1]
        # href_list = categories.xpath('.//ul//a/@href').extract()
        # for href in href_list:
        #     href_all_list.append(href)
        #     cat2 = extract_var(href, r"en-jp/(.*?)/cat")
        #     category = cat0 + "\\" + str(cat2).replace("/", "\\")
        #     category_list.append(category)
        # categories = resp.xpath(silo_li)[2]
        # ul_list = categories.xpath('.//ul')[0]
        # href_list = ul_list.xpath('.//a/@href').extract()
        # for href in href_list:
        #     href_all_list.append(href)
        #     cat2 = extract_var(href, r"en-jp/(.*?)/cat")
        #     category = cat0 + "\\" + str(cat2).replace("/", "\\")
        #     category_list.append(category)
        # href_list = categories.xpath('.//h6//a/@href').extract()
        # href_all_list.append(href_list[1])
        # cat2 = extract_var(href_list[1], r"en-jp/(.*?)/cat")
        # category = str(cat2).replace("/", "\\")
        # category_list.append(category)
        # href_all_list.append(href_list[2])
        # cat2 = extract_var(href_list[2], r"en-jp/(.*?)/cat")
        # category = str(cat2).replace("/", "\\")
        # category_list.append(category)
        # href_all_list.append(href_list[3])
        # cat2 = extract_var(href_list[3], r"en-jp/(.*?)/cat")
        # category = str(cat2).replace("/", "\\")
        # category_list.append(category)
        # href_all_list.append(href_list[4])
        # cat2 = extract_var(href_list[4], r"en-jp/(.*?)/cat")
        # category = str(cat2).replace("/", "\\")
        # category_list.append(category)

        pageSize = '?pageSize=' + str(self.page_size)
        for href,cat in zip(href_all_list,category_list):
            url = href + pageSize
            yield scrapy.Request(url=url, callback=self.parse_categorylink,
                                 meta={'type': 0, 'url1': href, 'items_count': 0, 'find_count': 0, 'page_num': 0 , 'cat':cat})

    def parse_categorylink(self, response):
        if response.meta['type'] == 2:
            json_data = json.loads(response.body)
            sel = Selector(text=json_data.get('GenericSearchResp', '').get('productResults',''))
            numItems = [0]
        else:
            navLastItem = response.xpath('//a[contains(@class,"navLastItem")]/@href').extract()
            numItems = response.xpath('//span[@id="numItems"]/text()').extract()
        if len(numItems)>0 :
            items_count = response.meta['items_count']
            find_count = response.meta['find_count']
            page_num = response.meta['page_num']
            if int(response.meta['type']) == 0:
                items_count = int(numItems[0])
                self.all_count += items_count
                find_count = 0
                page_num = 0
            if response.meta['type'] == 2:
                productList = sel.xpath('//a[@id="productTemplateId"]/@href').extract()
            else:
                productList = response.xpath('//a[@id="productTemplateId"]/@href').extract()
            for href in productList:
                url = self.base_url + href
                find_count += 1
                yield scrapy.Request(url=url, callback=self.parse_product, meta={'data':url,'cat':response.meta['cat']})
            if find_count < items_count and page_num * self.page_size <= items_count :
                page_num += 1
                catId ='cat'+ str(re.search(r"\/cat(.*?)_cat",response.meta['url1']).groups()[0])
                tmp = '{"GenericSearchReq":{"pageOffset":' + str(page_num) + ',"pageSize":"' + str(self.page_size) \
                      + '","refinements":"","selectedRecentSize":"","activeFavoriteSizesCount":"0","activeInteraction":"true","mobile":false,' \
                        '"sort":"PCS_SORT","personalizedPriorityProdId":"","endecaDrivenSiloRefinements":"pageSize=120","definitionPath":"/nm/commerce/pagedef_rwd/template/EndecaDrivenHome",' \
                        '"userConstrainedResults":"true","updateFilter":"false","rwd":"true","advancedFilterReqItems":{"StoreLocationFilterReq":[{"allStoresInput":"false","onlineOnly":""}]},' \
                        '"categoryId":"' + catId + '","sortByFavorites":false,"isFeaturedSort":false,"prevSort":""}}'
                tmp1="$b64$" + base64.b64encode(tmp)
                data=tmp1.replace("=", "$")
                post_url = self.base_url + "/en-jp/category.service"
                timestamp = str(time.time() * 1000)
                formdata = {'data': data,
                            'service':'getCategoryGrid',
                            'sid':'getCategoryGrid',
                            'bid':'GenericSearchReq',
                            'timestamp':timestamp}
                yield FormRequest(url=post_url, formdata=formdata, callback=self.parse_categorylink,meta={'type': 2,'url1':response.meta['url1'],'items_count':items_count,'find_count':find_count,'page_num':page_num,'cat':response.meta['cat']})
        else:
            if len(navLastItem)>0:
                pageSize = '?pageSize=' + str(self.page_size)
                for href in navLastItem:
                    url = self.base_url + href + pageSize
                    url1 = self.base_url + href
                    yield scrapy.Request(url=url, callback = self.parse_categorylink, meta={'type': 0,'url1':url1,'items_count':0,'find_count':0,'page_num':0,'cat':response.meta['cat']})

    def parse_product(self, response):
        self.fail_count += 1
        # TODO 상세페지 구현부분/
        def extract_var(reg):
            return response.xpath('//script').re(reg)

        product_url = response.meta['data']

        prodInfo = json.loads((extract_var(r"window.utag_data=(.*?);\n"))[0])
        product_id = (prodInfo["product_id"])[0]
        # get product other detail info
        product_name = (prodInfo["product_name"])[0].encode('utf-8')
        category_id = (prodInfo["cat_id"])[len(prodInfo["cat_id"]) - 1]
        price = float((prodInfo["product_price"])[0])
        exchangeRate = float((extract_var(r"var exchangeRate = (.*?);"))[0])
        # prodPrice = format(round(price * exchangeRate), ",.2f")
        prodPrice = round(price * exchangeRate)

        brand_span = response.xpath('//span[contains(@class, "product-designer")]')
        if len(brand_span) > 0:
            brandEle = brand_span[0]
            if len(brandEle.xpath('.//a')) > 0:
                brand_name = brandEle.xpath('.//a/text()').extract()[0]
            else:
                brand_name = brandEle.css('::text').extract()[0]
        else:
            brand_name = ''

        # 수정한 부분 시작
        categoryList = response.meta['cat']
        category_name = categoryList.encode('shift_jis')
        category_set_name = (categoryList.split("\\")[0]).encode('shift_jis')
        # 수정한부분 끝

        product_img_url = (response.xpath('//div[@id="prod-img"]//img/@src').extract()[0]).encode('shift_jis')

        # get product description
        product_desc = ''
        prodDetailList = response.xpath('//div[@class="productCutline"]')
        if len(prodDetailList) > 0:
            prodInfoList = prodDetailList[0].xpath('.//li')
            if len(prodInfoList) < 1:
                prodInfoList = prodDetailList[0].xpath('.//div')
            for i in range(len(prodInfoList)):
                text_in_li = prodInfoList[i].css('::text, *::text').extract()
                for j in range(len(text_in_li)):
                    str_one = text_in_li[j].encode('utf-8')
                    if str_one.strip():
                        product_desc = product_desc + str_one
                    else:
                        product_desc = product_desc + " "
                if i < len(prodInfoList) - 1:
                    product_desc = product_desc + '\n\r'

        aboutDesignerList = response.xpath('//div[@class="aboutDesignerCopy"]')
        if len(aboutDesignerList) > 0:
            if product_desc.strip():
                product_desc = product_desc + '\n\r\n\r'
            list = aboutDesignerList[0].css('::text').extract()
            print(len(list))
            for k in range(len(list)):
                if k < len(list) - 1:
                    product_desc = product_desc + list[k].encode('utf-8') + "\n\r"
                else:
                    product_desc = product_desc + list[k].encode('utf-8')
        # check shipable product
        ship_error = False
        error_text = ""
        error_text_list = response.xpath('//p[@class="error-text"]')
        if len(error_text_list) > 0:
            error_text = error_text_list[0].xpath('./text()').extract()[0]
            if "We are sorry" in error_text:
                ship_error = True
        if str((prodInfo["product_available"])[0]) == "true" and not ship_error:
            # get product balance and color type
            req_url = "http://www.neimanmarcus.com/en-jp/product.service"
            tmp = '{"ProductSizeAndColor":{"productIds":"' + str(product_id) + '"}}'
            tmp1 = "$b64$" + base64.b64encode(tmp)
            data = tmp1.replace("=", "$")
            timestamp = str(time.time() * 1000)
            request_data = {
                "data": data,
                "sid": "getSizeAndColorData",
                "bid": "ProductSizeAndColor",
                "timestamp": timestamp,
            }

            yield FormRequest(url=req_url, formdata=request_data, callback=self.parse_detail_product,
                              meta={'product_id':product_id,
                                    'product_name':product_name,
                                    'category_name':category_name,
                                    'product_url':product_url,
                                    'category_id':category_id,
                                    'category_set_name':category_set_name,
                                    'brand_name':brand_name,
                                    'prodPrice':prodPrice,
                                    'product_desc':product_desc,
                                    'product_img_url':product_img_url
                                    })

    def parse_detail_product(self,response):
        json_data = json.loads(response.body)
        res1 = json.loads(json_data['ProductSizeAndColor']['productSizeAndColorJSON'])

        product_id = response.meta['product_id']
        skusList = res1[0]['skus']
        color_size_stock = ''
        first_flag = True
        for m in range(len(skusList)):            
            if first_flag == False:
                color_size_stock += "|"
            color = ''
            size = ''
            stock = 0
            if 'color' in skusList[m]:
                color = (skusList[m]['color']).encode('utf-8').split("?")[0]
            if 'size' in skusList[m]:
                if skusList[m]['size'] != None and skusList[m]['size'].upper() != "NO SIZE":
                    size = (skusList[m]['size']).encode('utf-8')
            if 'stockLevel' in skusList[m]:
                stock = int(skusList[m]['stockLevel'])
            else:
                stock = int(skusList[m]['stockAvailable'])
            if stock == 0:
                stock = 999
            color_size_stock += color + ":" + size + ":" + str(stock)
            if first_flag == True:
                first_flag = False        

        item = WebscraperDemoItem()
        item['product_id'] = product_id
        item['product_name'] = response.meta['product_name']
        item['category_id'] = response.meta['category_id']
        item['category_name'] = response.meta['category_name']
        item['color_size_stock'] = color_size_stock
        item['price'] = response.meta['prodPrice']
        item['product_desc'] = response.meta['product_desc']
        item['product_url'] = response.meta['product_url']
        item['brand_name'] = response.meta['brand_name']

        img_url = response.meta['product_img_url']
        if not 'http:' in img_url:
            if '//' in img_url:
                img_url = 'http:' + img_url
            else:
                img_url = self.base_url + img_url
        thumb_guid = hashlib.sha1(to_bytes(img_url)).hexdigest()
        img_path=const.IMAGE_UPLOAD_PATH
        item['product_img_url'] = '%s%s.jpg' % (img_path, thumb_guid)
        item['image_urls'] = [img_url]

        self.fail_count -= 1
        self.find_count += 1
        item['all_product_count'] = self.all_count
        item['find_product_count'] = self.find_count
        item['fail_product_count'] = self.fail_count

        yield item