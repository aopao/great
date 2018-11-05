#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Jason
# @Email   : Admin@wujinyu.com
# @Time    : 2018/11/2 下午9:05
"""Code"""

import oss2
import requests
from application import app


class Oss(object):
    @classmethod
    def upload(cls, filename, url):
        filename = filename[1:]
        auth = oss2.Auth(app.config.get('ACCESS_KEY_ID'), app.config.get('ACCESS_KEY_SECRET'))
        bucket = oss2.Bucket(auth, app.config.get('CNAME'), app.config.get('BUCKET'), is_cname=True, connect_timeout=30)
        content = requests.get(url)
        if content.status_code == 200:
            exist = bucket.object_exists(filename)
            # 返回值为true表示文件存在，false表示文件不存在。
            if not exist:
                bucket.put_object(filename, content)
            return 200
        else:
            return 404
