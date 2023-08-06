# -*- coding: utf-8 -*-
# @Time: 2023/3/15 14:14
# @Author: zyq
# @File: coordinate.py
# @Software: PyCharm


"""
Description: 坐标处理
:param      item: 需要处理的结构化数据
:param      is_return_location: 是否返回坐标信息，True为返回
:param      is_return_verification: 是否返回校验状态，True为返回
:param      exclusion_list: item内不需要处理的字段（会包含字段的子结构），默认[]。

"""
def handle_coordinate(item, is_return_location, is_return_verification, exclusion_list=[]):
    for k, v in item.items():
        if isinstance(v, dict):
            if k in exclusion_list:
                is_return_location = True
            coordinate_recursion(v, is_return_location, is_return_verification)
            handle_coordinate(v, is_return_location, is_return_verification, exclusion_list)
        elif isinstance(v, list):
            for i in v:
                handle_coordinate(i, is_return_location, is_return_verification, exclusion_list)

def coordinate_recursion(item, is_return_location, is_return_verification):
    if is_return_location is False:
        if 'coordinate' in item:
            del item['coordinate']
    if is_return_verification is False:
        if 'credible' in item:
            del item['credible']
        if 'state' in item:
            del item['state']
