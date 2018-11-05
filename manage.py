#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Jason
# @Email   : Admin@wujinyu.com
# @Time    : 2018/11/2 下午6:54
from jobs.launch import RunJob
from application import app, db
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from model.BtXiaBaModel import BtXiaBaModel

# 数据迁移
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

# 定时任务
manager.add_command("runJob", RunJob())

# 启动服务
manager.add_command(
    "runServer",
    Server(
        host=app.config["SERVER_URI"],
        port=app.config["SERVER_PORT"],
        use_debugger=app.config["DEBUG"],
        use_reloader=True,
    ),
)

if __name__ == "__main__":
    manager.run()
