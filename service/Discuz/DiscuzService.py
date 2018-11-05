#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Jason
# @Email   : Admin@wujinyu.com
# @Time    : 2018/11/2 下午10:04
# ------------------------------------
#       Discuz 网站数据插入
# ------------------------------------
import random
import time

import pymysql


class DiscuzService(object):
    @classmethod
    def run(cls, data):
        try:
            conn = pymysql.connect("localhost", "root", "root", "new1")
            cursor = conn.cursor()

            sql = "SELECT username FROM pre_common_member WHERE uid = '%d'" % data['uid']
            cursor.execute(sql)
            author = cursor.fetchone()[0]  # 用户name

            # 第一步给pre_forum_post_tableid表插入空数据进行自增，然后获取自增pid
            cursor.execute('INSERT INTO pre_forum_post_tableid VALUES (NULL);')
            cursor.execute('SELECT max(pid) FROM pre_forum_post_tableid;')
            pid = cursor.fetchone()[0]

            # 第二步给pre_forum_thread表插入帖子标题数据，然后获取自增tid highlight
            highlight = random.randint(40, 47)
            sql_thread = "INSERT INTO pre_forum_thread SET fid=" + str(data['fid']) \
                         + ",author='" + author + "',authorid=" + str(data['uid']) \
                         + ",highlight=" + str(highlight) + ",typeid=" + str(data['typeId']) \
                         + ",subject='" + data['subject'] + "',dateline=" + data['created_time'] \
                         + ",lastposter='" + author + "',lastpost=" \
                         + str(time.time()) + ",views=" + str(random.randint(20, 500)) + ";"

            cursor.execute(sql_thread)
            cursor.execute('SELECT max(tid) FROM pre_forum_thread')
            tid = int(cursor.fetchone()[0])

            # 第三步给pre_forum_post表插入帖子的标题、内容等，pid、tid用上两步获得的数据  如要增加附件需修改attachment
            sql_post = "INSERT INTO pre_forum_post SET pid=" + str(pid) + ",fid=" \
                       + str(data['fid']) + ",tid=" + str(tid) + ",first=1,author='" \
                       + author + "', authorid=" + str(data['uid']) + ", subject='" \
                       + data['subject'] + "' ,dateline=" + data['created_time'] + ", message=\"" \
                       + conn.escape_string(str(data['message'])) \
                       + "\" , useip='35.201.200.63' , port=1688 , invisible = 0, anonymous = 0 , usesig = 1 , htmlon = " \
                       + str(data['htmlon']) + ", bbcodeoff =bbcodeoff , smileyoff =-1 , parseurloff =0 , attachment = 0 , tags='' , replycredit=0 , status=0;"
            cursor.execute(sql_post)

            # 第四步给pre_forum_forum版块表进行更新帖子数量
            sql_forum = 'UPDATE pre_forum_forum SET threads=threads+1, ' \
                        'posts=posts+1, todayposts=todayposts+1 , allowsmilies = 1,allowbbcode = 1,' \
                        ' allowimgcode =1 ,allowspecialonly = 0,allowglobalstick = 1,alloweditpost = 1 ,' \
                        'recyclebin =1 WHERE fid=' + str(data['fid']) + ';'
            cursor.execute(sql_forum)

            # 第五步给pre_common_member_count表更新用户帖子数量信息
            sql_count = 'UPDATE pre_common_member_count SET threads = threads+1 WHERE uid =' + str(data['uid']) + ';'
            cursor.execute(sql_count)  # 提交，不然无法保存新建或者修改的数据

            # X3之后新增的第六步给pre_forum_sofa表插入tid、fid
            sql_sofa = "INSERT INTO pre_forum_sofa SET tid=" + str(tid) + ",fid=" + str(data['fid']) + ";"
            cursor.execute(sql_sofa)
            conn.commit()
            return tid
        except:
            print("发声错误啦:%s" % data['subject'])
