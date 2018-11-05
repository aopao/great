#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Jason
# @Email   : Admin@wujinyu.com
# @Time    : 2018/11/2 下午8:59
import json
from application import db
from model.BtXiaBaModel import BtXiaBaModel


class BtXiaBaService(object):
    @classmethod
    def find_by_btxiaba_id(cls, btxiaba_id):
        return db.session.query(BtXiaBaModel).filter_by(btxiaba_id=btxiaba_id).first()

    @classmethod
    def get_no_send_movie(cls):
        return db.session.query(BtXiaBaModel).filter_by(discuz_id=0).all()

    @classmethod
    def add(cls, data):
        db.session.add(
            BtXiaBaModel(
                btxiaba_id=data["btxiaba_id"],
                name=data["name"],
                thumb=data["thumb"],
                imgs=data["imgs"],
                direct=data["direct"],
                actor=data["actor"],
                type=data["type"],
                area=data["area"],
                language=data["language"],
                year=data["year"],
                description=data["description"],
                download=json.dumps(data["download"]),
                created_time=data["created_time"],
            )
        )
        db.session.commit()

    @classmethod
    def update_discuz_done(cls, btxiaba_id, discuz_id):
        db.session.query(BtXiaBaModel).filter_by(btxiaba_id=btxiaba_id).update(
            {"discuz_id": discuz_id}
        )
        db.session.commit()
