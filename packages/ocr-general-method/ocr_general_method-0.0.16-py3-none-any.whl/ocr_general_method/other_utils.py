# -*- coding: utf-8 -*-
# @Time: 2023/3/15 15:52
# @Author: zyq
# @File: other_utils.py
# @Software: PyCharm
import json
import numpy as np


"""
Description: 路径处理
:param debug: True为debug模式，返url，否则返回base64
:param: is_return_img: 是否返回图片。True返回
:param image_path: 图片请求路径
:param img_base64: 图片base64编码
:param ocr_result: ocr模型请求结果
:return: result: 图片结果
"""
def url_handle(debug, is_return_img, image_path, img_base64, ocr_result=None):
    result = {}
    if debug:
        if is_return_img:
            result['img_original'] = image_path
            if ocr_result is not None:
                result['img'] = ocr_result['img_ocrrotated_url']
                result['img_visualization'] = ocr_result['img_ocrvis_url']
    else:
        if is_return_img:
            result['img_original'] = img_base64
            if ocr_result is not None:
                if 'img_ocrrotated_base64' in ocr_result:
                    result['img'] = ocr_result['img_ocrrotated_base64']
                # result['img_visualization'] = ocr_result['img_ocrvis_base64']
    return result


"""
Description: 数据转换类
"""
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        else:
            return super(NpEncoder, self).default(obj)
