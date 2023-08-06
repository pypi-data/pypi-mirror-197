# -*- coding: utf-8 -*-
# @Time: 2023/3/2 9:50
# @Author: zyq
# @File: exception_utils.py
# @Software: PyCharm


# """
# Description: 错误处理
# :param code: 错误码
# :return: res: 错误码、错误提示
# """
def error_handle(code):
    res = {'code': code}
    if code == 60101:
        res['msg'] = '模型识别错误'
    elif code == 60201:
        res['msg'] = '结构化错误'
    elif code == 60401:
        res['msg'] = '远程路径请求失败'
    elif code == 40309:
        res['msg'] = 'pdf格式仅支持单页识别'
    elif code == 40203:
        res['msg'] = '暂不支持该文件类型'
    elif code == 40101:
        res['msg'] = 'file参数为空'
    elif code == 40103:
        res['msg'] = '请上传图片'
    elif code == 40310:
        res['msg'] = '当前图片不存在'
    elif code == 50701:
        res['msg'] = '系统内部异常'
    return res
