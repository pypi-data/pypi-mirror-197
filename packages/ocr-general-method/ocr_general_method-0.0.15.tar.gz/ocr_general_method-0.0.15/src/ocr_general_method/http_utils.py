# -*- coding: utf-8 -*-
# @Time: 2023/3/1 17:46
# @Author: zyq
# @File: http_utils.py
# @Software: PyCharm

import requests
import traceback
from .exception_utils import error_handle

"""
Description: 请求远程接口
:param method: 请求方法
:param url: 请求路径
:param headers: 请求头，默认{}
:param payload: 请求参数body，默认{}
:param files: 请求参数form-data，默认[]
:return: response
"""
def request_ocr(method, url, headers={}, payload={}, files=[]):
    # noinspection PyBroadException
    try:
        response = requests.request(method, url, headers=headers, data=payload, files=files)
        response = response.text
        response = eval(response)
        return response
    except:
        print(traceback.format_exc())
        res = error_handle(60401)
        return res
