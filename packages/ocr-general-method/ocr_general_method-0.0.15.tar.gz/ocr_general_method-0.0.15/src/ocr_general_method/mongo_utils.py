# -*- coding: utf-8 -*-
# @Time: 2023/3/15 14:11
# @Author: zyq
# @File: mongo_utils.py
# @Software: PyCharm
import time
import pymongo
import traceback
from bson import ObjectId


"""
Description: 存储数据到mongo
:param      document: 存储数据
:param      mongo_table_medical: 表名
:param      create_time: 数据创建时间,默认当前时间
:param      state: 校验状态，默认create
:param      mongo_host: 数据库ip地址
:param      mongo_user: 数据库用户名
:param      mongo_pass: 数据库密码
:param    mongo_db: 数据库名称
:param    mongo_port: 数据库端口，默认27017
:return:    document: 存储数据内容，添加存储唯一标识request_id

"""
def save_to_mongo(document, mongo_table_medical, mongo_host, mongo_user, mongo_pass, mongo_db, mongo_port=27017,
                  create_time=time.strftime('%Y%m%d%H%M%S', time.localtime()), state='create'):
    if mongo_host is None or mongo_user is None or mongo_pass is None or mongo_db is None:
        print("mongo未连接或不需要存mongo：mongo_host-{}, mongo_user-{}, mongo_pass-{}, mongo_db-{}".
              format(mongo_host, mongo_user, mongo_pass, mongo_db))
        return None
    try:
        document['result']['createTime'] = create_time
        document['result']['state'] = state
        save_mongo(mongo_host, mongo_user, mongo_pass, mongo_db, mongo_port, mongo_table_medical).insert(document)
        document['result']['request_id'] = str(ObjectId(document['_id']))
    except Exception as e:
        print('save_to_mongo Exception:{}'.format(traceback.format_exc()))
    finally:
        document.pop('_id')
    return document

#: 连接mongo
def save_mongo(mongo_host, mongo_user, mongo_pass, mongo_db, mongo_port, mongo_table_medical):
    if mongo_host is None or mongo_user is None or mongo_pass is None or mongo_db is None:
        print("mongo未连接或不需要存mongo：mongo_host-{}, mongo_user-{}, mongo_pass-{}, mongo_db-{}, type-{}".
              format(mongo_host, mongo_user, mongo_pass, mongo_db, type))
        return None
    client = pymongo.MongoClient(mongo_host, mongo_port)
    rent_info = client[mongo_db]  # 给数据库命名
    rent_info.authenticate(mongo_user, mongo_pass)
    sheet_table = rent_info[mongo_table_medical]  # 创建表单
    return sheet_table
