#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Jason
# @Email   : Admin@wujinyu.com
# @Time    : 2018/11/2 下午7:54
# ------------------------------------
#       BtXiaBa网站电影资源采集处理类
# ------------------------------------
import re
import time
from lxml import etree
from utils.Oss import Oss
from utils.Http import Http
from service.BtXiaBa.BtXiaBaService import BtXiaBaService


class BtXiaBaSpider(object):
    # 定义页面所需变量
    spider = object
    all_page_num = 0
    base_url = "http://www.btxiaba.com"
    list_url = "http://www.btxiaba.com/vod-type-id-1-pg-{page}.html"
    movie_url = "http://www.btxiaba.com/vod-detail-id-{page}.html"

    @classmethod  # 总调度方法
    def run_spider(cls, params=None):

        if params is not None:
            # 指定页数采集
            cls.all_page_num = int(params)
        else:
            # 获取所有页数
            cls.get_all_page_num()

        # 生成所有列表页面连接
        cls.generate_all_list_url()

    @classmethod  # 获取页面总页数
    def get_all_page_num(cls):
        content = Http.get(cls.list_url.format(page=1))
        if content.status_code == 200:
            # 解析页面
            doc = etree.HTML(content.text)
            last_page_url = doc.xpath('//div[@class="paginator"]/a[last()]/@href')
            print(last_page_url)
            if len(last_page_url) > 0:
                cls.all_page_num = int(''.join(last_page_url)[18:-5])
        else:
            exit("页数获取失败,请检查")

    @classmethod  # 生成所有列表页面连接
    def generate_all_list_url(cls):
        for num in range(1, cls.all_page_num + 1):
            url = cls.list_url.format(page=num)
            # 对页面进行解析,然后分析出电影页面
            cls.parse_list_url(url)

    @classmethod
    def parse_list_url(cls, url):
        # try:
        content = Http.get(url)
        if content.status_code == 200:
            doc = etree.HTML(content.text)
            items = doc.xpath('//div[@id="content"]//div[@class="indent"]//table')
            for item in items:
                url = item.xpath('.//a[@class="nbg"]/@href')
                if len(url) > 0:
                    url = cls.base_url + url[0]
                    btxiaba_id = url[37:len(url) - 5]
                    if BtXiaBaService.find_by_btxiaba_id(btxiaba_id):
                        print("已经采集过了")
                        break
                    cls.parse_movie_url(url)
        # except:
        #     print("发生错误啦:%s" % url)

    @classmethod
    def parse_movie_url(cls, url):
        """解析电影页面"""
        content = Http.get(url)
        if content.status_code == 200:
            data = {}
            doc = etree.HTML(content.text)
            name = doc.xpath('//div[@id="content"]/h1/span[1]/text()')
            year = doc.xpath('//div[@id="content"]/h1/span[2]/text()')
            sign = doc.xpath('//div[@id="content"]/h1/span[3]/text()')
            thumb = doc.xpath('//div[@id="mainpic"]/a/img/@src')
            direct = doc.xpath('//div[@id="info"]/span[1]/span[@class="attrs"]/a/text()')
            actor = doc.xpath('//div[@id="info"]/span[2]/span[@class="attrs"]/a/text()')
            type = doc.xpath('//div[@id="info"]/span[3]/following-sibling::a[1]/text()')
            area = doc.xpath('//div[@id="info"]/span[4]/following-sibling::a[1]/text()')
            language = doc.xpath('//div[@id="info"]/span[6]/a/text()')
            description = doc.xpath('//div[@id="link-report"]/span/text()')
            imgs = doc.xpath('//ul[@class="related-pic-bd narrow"]/li/img/@src')
            mat = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})", content.text)
            if len(mat.groups()) > 0:
                data['created_time'] = mat.groups()[0]
            else:
                data['created_time'] = time.time()

            year = ''.join(year).replace("(", "").replace(")", "")
            data['btxiaba_id'] = content.url[37:len(content.url) - 5]
            data['name'] = '[' + year + '年' + ''.join(area) + '最新' + ''.join(type) + '][' + ''.join(name) + ']-[' + ''.join(sign) + ']'
            data['thumb'] = ''.join(thumb)
            if "未知" in data['name']:
                data['name'] = data['name'].replace("未知年", "")

            if "upload" in data['thumb'] and "vod" in data['thumb']:
                url = cls.base_url + data['thumb']
                Oss.upload(data['thumb'], url)
                data['thumb'] = "http://static.68os.com" + data['thumb']

            data['year'] = ''.join(year)
            data['direct'] = '  '.join(direct)
            data['actor'] = '  '.join(actor)
            data['type'] = ''.join(type)
            data['area'] = ''.join(area)
            data['language'] = ''.join(language)
            data['description'] = ''.join(description).replace("\u3000\u3000", "")
            data['imgs'] = '|'.join(imgs)
            # 开始处理下载地址
            downloads_arr = []
            downloads = doc.xpath('//div[@id = "askmatrix"]/div[@class="p_list_down"]/li/a/@href')
            for download in downloads:
                download_url = cls.base_url + download
                download = cls.parse_download_movie_url(download_url)
                downloads_arr.append(download)
            data['download'] = downloads_arr
            cls.insert_movie_db(data)

    @classmethod
    def parse_download_movie_url(cls, download_url):
        """解析下载地址页面"""
        download = {}
        content = Http.get(download_url)
        if content.status_code == 200:
            doc = etree.HTML(content.text)
            name = doc.xpath('//div[@class="p_list"]/div[2]/span/text()')
            download['name'] = ''.join(name)
            src = doc.xpath('//div[@class="p_list"]/div[3]/span/text()')
            download['src'] = ''.join(src)
            return download

    @classmethod
    def insert_movie_db(cls, data):
        BtXiaBaService.add(data)
