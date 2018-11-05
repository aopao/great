#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Jason
# @Email   : Admin@wujinyu.com
# @Time    : 2018/11/2 下午7:10

from application import db


class BtXiaBaModel(db.Model):
    __tablename__ = "btxiaba"

    id = db.Column(db.BigInteger, primary_key=True)
    btxiaba_id = db.Column(
        db.String(255), nullable=False, server_default="", comment="BT吧ID"
    )
    discuz_id = db.Column(
        db.String(255), nullable=False, server_default="", comment="论坛ID"
    )
    name = db.Column(db.String(255), nullable=False, server_default="", comment="电影名称")
    thumb = db.Column(db.String(255), nullable=True, server_default="", comment="电影缩略图")
    imgs = db.Column(db.Text(), nullable=True, server_default="", comment="电影截图")
    direct = db.Column(db.String(255), nullable=True, server_default="", comment="电影导演")
    actor = db.Column(db.String(255), nullable=True, server_default="", comment="电影主演")
    type = db.Column(db.String(100), nullable=True, server_default="", comment="电影类型")
    area = db.Column(db.String(255), nullable=True, server_default="", comment="电影地区")
    language = db.Column(db.String(255), nullable=True, server_default="", comment="语言")
    year = db.Column(db.String(255), nullable=True, server_default="", comment="电影年份")
    description = db.Column(db.Text(), nullable=True, server_default="", comment="电影名称")
    download = db.Column(db.Text(), nullable=True, server_default="", comment="电影下载地址")
    created_time = db.Column(db.String(255), nullable=True, server_default="")

    def __str__(self):
        return self.name
