# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time

#from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import render
from convert.generate_csv import Generate_CSV
from convert.lang_trans import LangTrans
from convert.merge_csv import MergeCsv
from testmodels import const
from testmodels.models import TestModels
from .models import Question

from twisted.internet import reactor
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from webscraper_demo.spiders.crawl2yahoo import ToScrapeSpiderXPath
from webscraper_demo.spiders.data import URL_DATA
from threading import Thread

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'dwsyahoo/index.html', context)


def scrapy_exit(email_addr,url):
    tmp = TestModels.get_test2_data()
    find_type = tmp[0]
    start_time = time.time()
    while find_type != const.FIND_SUCCESS:
        time.sleep(3.5)
        tmp = TestModels.get_test2_data()
        find_type = tmp[0]
    end_time = time.time()
    MergeCsv.main()
    LangTrans.main()
    mail_result = sendmeail(email_addr,url,start_time,end_time)

# 메일보내기함수
def sendmeail(email_addr,url,start_time,end_time):
    diff_t= time.gmtime(end_time-start_time)
    diff_s = str(diff_t.tm_hour) + '時間' + str(diff_t.tm_min) + '分' + str(diff_t.tm_sec) + '秒'
    start_t = time.gmtime(start_time)
    start_s = str(start_t.tm_year) + '年' + str(start_t.tm_mon) + '月' + str(start_t.tm_mday) + '日' + str(
        start_t.tm_hour) + '時' + str(start_t.tm_min) + '分' + str(start_t.tm_sec) + '秒'
    end_t =time.gmtime(end_time)
    end_s = str(end_t.tm_year) + '年' + str(end_t.tm_mon) + '月' + str(end_t.tm_mday) + '日' + str(
        end_t.tm_hour) + '時' + str(end_t.tm_min) + '分' + str(end_t.tm_sec) + '秒'
    tmp = TestModels.get_find_count()
    find_p_count = tmp[1]
    sender = const.SENDER_EMAIL_ADDR
    receivers = [str(email_addr)]
    title = 'クローリング作業完了のお知らせ'
    message = "クローリング作業が完了しました。\n" + \
              "作業サイト: " + str(url) + "\n" + \
              "作業開始時間："  + start_s + "\n" + \
              "作業完了時間：" +  end_s + "\n" + \
              "作業時間：" + diff_s + "\n" + \
              "商品総数：" + str(find_p_count) + "\n" + \
              "作業総数：" + str(find_p_count) + "\n" + \
              "作業データをご確認ください。"

    msg = EmailMessage(
        title,
        message,
        sender,
        receivers,
        cc=const.CC_MAIL
    )
    try:
        msg.send(fail_silently=False)
    except:
        return False
    return  True

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
settings = get_project_settings()

settings.set('ITEM_PIPELINES', {'scrapy.pipelines.images.ImagesPipeline': 1,
                                'webscraper_demo.pipelines.DbSqlitePipeline': 313,
                                'webscraper_demo.pipelines.CsvWriterPipeline': 313,
                                }, priority='cmdline')
settings.set('IMAGES_STORE', const.IMAGE_PATH)
settings.set('BOT_NAME', 'webscraper_demo')
settings.set('SPIDER_MODULES', ['webscraper_demo.spiders'])
settings.set('NEWSPIDER_MODULE', 'webscraper_demo.spiders')
settings.set('ROBOTSTXT_OBEY', True)
settings.set('SPIDER_MIDDLEWARES', {'webscraper_demo.middlewares.WebscraperDemoSpiderMiddleware': 534, })
settings.set('USER_AGENT', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)')
# settings.set('LOG_ENABLED', False)
# settings.set('LOG_LEVEL', 'ERROR')
# settings.set('DOWNLOAD_DELAY', '0.25')
runner = CrawlerRunner(settings)

def detail(request):
    if request.is_ajax():
        question_id = request.POST.get('url_id', None)
        email_addr = str(request.POST.get('email_addr', None))
        req_type = int(request.POST.get('type', None))
        if question_id==None or email_addr==None or req_type==None:
            data = {
                'result': "FAIL",
                'content': 'Paramter Error...'
            }
            return JsonResponse(data)

        if req_type == const.SCRAPY_START or req_type == const.SCRAPY_RESTART:
            try:
                question = Question.objects.get(pk=question_id)
            except Question.DoesNotExist:
                raise Http404("Question does not exist")

            tmp = TestModels.get_test2_data()
            status = tmp[4]
            find_type = tmp[0]

            if find_type == const.FIND_INIT:
                if status == const.STATUS_ON:
                    if req_type == const.SCRAPY_START:
                        data = {
                            'result': "PROGRESS",
                            "content": {
                                "all": 0,
                                "find": 0,
                                "fail": 0,
                                "find_type": find_type,
                                "status": status,
                            }
                        }
                        return JsonResponse(data)
                    if req_type == const.SCRAPY_RESTART:
                        runner.stop()

                time.sleep(2)
                d = runner.crawl(ToScrapeSpiderXPath)
                # d.addBoth(lambda _: Thread(target=reactor.stop, args=(False,)).start())
                d.addBoth(lambda _: reactor.stop)
                # reactor.run()
                if reactor.running == False:
                    Thread(target=reactor.run, args=(False,)).start()

                time.sleep(2)
                Thread(target=scrapy_exit, args=(email_addr,question)).start()

        tmp = TestModels.get_find_count()
        all_p_count = tmp[0]
        find_p_count = tmp[1]
        fail_p_count = tmp[2]
        tmp = TestModels.get_test2_data()
        status = tmp[4]
        find_type = tmp[0]
        # current_link_index = int(tmp[2])
        if status == const.STATUS_ON:
            data = {
                'result': "PROGRESS",
                "content": {
                    "all": all_p_count,
                    "find": find_p_count,
                    "fail": fail_p_count,
                    "find_type": find_type,
                    "status": status,
                }
            }
        else:
            mail_result = False
            if (find_type == const.FIND_SUCCESS):
                # MergeCsv.main()
                # LangTrans.main()
                # mail_result = sendmeail(email_addr)
                data = {
                    'result': "SUCCESS",
                    "content": {
                        "all": all_p_count,
                        "find": find_p_count,
                        "fail": fail_p_count,
                        "status": status,
                        "find_type": find_type,
                        "mail_result": mail_result
                    }
                }
            else:
                data = {
                    'result': "PROGRESS",
                    "content": {
                        "all": all_p_count,
                        "find": find_p_count,
                        "fail": fail_p_count,
                        "find_type": find_type,
                        "status": status,
                    }
                }
        return JsonResponse(data)
    else:
        data = {
            'result': "FAIL",
            "content": "Server Error..."
        }
        return JsonResponse(data)

def convert_csv(request):
    if request.is_ajax():
        type = int(request.POST.get('type', None))
        tmp = TestModels.get_test2_data()
        status = tmp[4]
        if status == const.STATUS_ON:
            data = {
                'result': "FAIL",
            }
            return JsonResponse(data)
        if type == 1:
            Generate_CSV.main()

            # db 초기화
            TestModels.set_find_type(const.FIND_INIT)
            TestModels.set_test2_index_data(0, 0)
            TestModels.set_status(const.STATUS_INIT)
            TestModels.set_init_count()

            data = {
                'result': "SUCCESS",
                'content': ''
            }
            return JsonResponse(data)
        else:
            data = {
                'result': "FAIL",
            }
            return JsonResponse(data)
    else:
        data = {
            'result': "FAIL"
        }
        return JsonResponse(data)