# -*- coding: utf-8 -*-
# @Time: 2023/3/2 9:50
# @Author: zyq
# @File: exception_utils.py
# @Software: PyCharm


"""
Description: 错误处理
:param code: 错误码
:return: res: 错误码、错误提示
"""
def error_handle(code):
    code_msg_list = {
        60101: '模型识别错误',
        60201: '结构化错误',
        60401: '远程路径请求失败',
        40309: 'pdf格式仅支持单页识别',
        40203: '暂不支持该文件类型',
        40101: 'file参数为空',
        40103: '请上传图片',
        40310: '当前图片不存在',
        50701: '系统内部异常'
    }
    res = {'code': code, 'msg': code_msg_list.get(code)}
    return res
