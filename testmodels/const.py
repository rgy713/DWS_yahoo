# -*- coding: utf-8 -*-
# TODO
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 템프홀더
TMP_DIR_PATH = os.path.join(BASE_DIR_PATH, 'tmp')
# 결과홀더
RESULT_DIR_PATH = os.path.join(BASE_DIR_PATH, 'result')

# 자료기지 명
SQLITE_DB_NAME = os.path.join(BASE_DIR_PATH, 'db.sqlite3')
# 상품정보보관 화일 명
CSV_ITEMS_PRE_NAME = os.path.join(TMP_DIR_PATH, 'items')
CSV_ITEMS_TMP_PRE_NAME = os.path.join(TMP_DIR_PATH, 'tmp_items.csv')
# 변환부분 홀더
CNV_DIR_PATH = os.path.join(os.path.join(BASE_DIR_PATH, 'convert'),'trans_csv')
# 변환에 필요한 csv화일명
CSV_BRAND = os.path.join(CNV_DIR_PATH, 'brand.csv')
CSV_CAT = os.path.join(CNV_DIR_PATH, 'cat.csv')
CSV_COLOR = os.path.join(CNV_DIR_PATH, 'color.csv')
CSV_PROD_TRANS = os.path.join(CNV_DIR_PATH, 'prod_trans.csv')
# 결과 csv화일명
CSV_ITEM_TRANS = os.path.join(TMP_DIR_PATH, 'items_trans.csv')
CSV_ITEM_CAT = os.path.join(RESULT_DIR_PATH, 'item_cat.csv')
CSV_ITEM = os.path.join(RESULT_DIR_PATH, 'item.csv')
CSV_SELECT = os.path.join(RESULT_DIR_PATH, "select.csv")
CSV_SELECT_BASE = os.path.join(TMP_DIR_PATH, "select_base.csv")
CSV_TMP_SELECT = os.path.join(TMP_DIR_PATH, "tmp_select.csv")

# scrapy 상태코드
STATUS_INIT = 0
# 켜있는 상태
STATUS_ON = 1
# 꺼진 상태
STATUS_OFF = 2

# 상품정보 수집결과상태코드
# 초기상태
FIND_INIT = 0
# 진행중 상태
FIND_PROGRESS = 1
# 성공 상태
FIND_SUCCESS = 2
# 실패 상태
FIND_ERROR = 3

SCRAPY_START = 0
SCRAPY_PROGRESS = 1
SCRAPY_RESTART = 2
SCRAPY_STOP = 3
# No touch!
SENDER_EMAIL_ADDR = 'root@tk2-245-32333.vs.sakura.ne.jp'
CC_MAIL = ['info@applink.co.jp']
# 이미지다운경로
IMAGE_PATH = os.path.join(RESULT_DIR_PATH, "img")
# 락텐의 이미지업로드경로
IMAGE_UPLOAD_PATH = ""
