#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Jason
# @Email   : Admin@wujinyu.com
# @Time    : 2018/11/2 下午7:40
import json
import time
import random
from random import choice
from application import app
from service.Discuz.DiscuzService import DiscuzService
from spider.BtXiaBa.BtXiaBaSpider import BtXiaBaSpider
from service.BtXiaBa.BtXiaBaService import BtXiaBaService


# BtXiaBa电影采集程序
class JobTask(object):

    # 采集主入口
    def run(self, params):
        act = params['act'] if 'act' in params else ''
        page_num = params['param'][0] if params['param'] and len(params['param']) else None
        if act.upper() == 'MOVIE':
            if page_num is not None:
                BtXiaBaSpider.run_spider(page_num)
            else:
                BtXiaBaSpider.run_spider()
        elif act.upper() == 'POST':
            self.insert_discuz_db()

    @classmethod
    def insert_discuz_db(cls):
        all_movies = BtXiaBaService.get_no_send_movie()
        for movie in all_movies:
            # 准备插入的数据
            data = dict()
            data['htmlon'] = 0  # 不开启html代码
            data['uid'] = choice(app.config["BTXIABA_USER"])
            data['fid'] = app.config["BTXIABA_FID"]
            data['view'] = random.randint(20, 500)
            data['subject'] = movie.name
            data['typeId'] = cls.tranform_type(movie.type)
            data['created_time'] = cls.tranform_time(movie.created_time)
            message = """
[img]{thumb}[/img]

◎片　　名:　{name}
◎年　　代:　{year}
◎产　　地:　{area}
◎类　　别:　{type}
◎语　　言:　{language}
◎导　　演:　{direct}
◎主　　演:　{actor}

◎简   介

{description}

◎截   图
{imgs}

[hide]

{download}

[/hide]
                    """
            message = message.replace("{thumb}", movie.thumb). \
                replace("{name}", movie.name). \
                replace("{year}", movie.year). \
                replace("{area}", movie.area). \
                replace("{type}", movie.type). \
                replace("{language}", movie.language). \
                replace("{direct}", movie.direct). \
                replace("{actor}", movie.actor). \
                replace("{description}", movie.description)

            str_imgs = ""
            if movie.imgs:
                img_arr = movie.imgs.split("|")
                if len(img_arr) > 0:
                    for img in img_arr:
                        str_imgs = str_imgs + "\n" + "[img]" + img + "[/img]"

            if len(str_imgs) > 40:
                message = message.replace("{imgs}", str_imgs)
            else:
                message = message.replace("◎截   图", "")
                message = message.replace("{imgs}", "")

            str_downloads = ""
            if movie.download:
                downloads = json.loads(movie.download)
                if len(downloads) > 0:
                    for download in downloads:
                        down_src = download['src']
                        if "baidu" in down_src:
                            continue
                        if down_src.endswith("torrent"):
                            str_downloads = str_downloads + "[bt]" + down_src + "[/bt]"
                        if down_src.startswith("magnet"):
                            str_downloads = str_downloads + "[magnet]" + down_src + "[/magnet]"

            data['message'] = message.replace("{download}", str_downloads)
            tid = DiscuzService.run(data)
            if tid > 0:
                BtXiaBaService.update_discuz_done(movie.btxiaba_id, tid)
            print("[%s]论坛发布成功" % movie.name)

    @classmethod
    def tranform_time(cls, str_time):
        # 将其转换为时间数组
        time_struct = time.strptime(str_time, "%Y-%m-%d %H:%M")
        # 转换为时间戳:
        time_stamp = str(time.mktime(time_struct))
        if "." in time_stamp:
            time_stamp = time_stamp[:-2]
        return time_stamp

    @classmethod
    def tranform_type(cls, leixing):
        movie = app.config["MOVIETYPERELATION"]
        return movie.get(leixing, 13)
