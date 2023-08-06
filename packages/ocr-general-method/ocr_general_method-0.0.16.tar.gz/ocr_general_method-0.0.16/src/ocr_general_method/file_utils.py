# -*- coding: utf-8 -*-
# @Time: 2023/3/2 9:36
# @Author: zyq
# @File: file_utils.py
# @Software: PyCharm

import os
import time
import base64
from io import BytesIO
from .exception_utils import error_handle
from pdf2image import convert_from_bytes

# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['jpg', 'JPG', 'bmp', 'BMP', 'png', 'PNG', 'jpeg', 'JPEG'])
# 成功标识
RES = {'code': 200, 'msg': '成功'}

"""
Description: 处理上传文件
:param      files: 上传文件列表。文件支持pdf格式，图像支持jpg，jpeg，bmp，png
:param      debug: debug模式。是否为开发人员模式
:param      save_root: 图片保存根目录
:param      rotate_res_url: 图片请求路径
:param      number: 1. 单张图片或单页文件上传 2. 多张图片或多页文件上传
:param      pdf_path: pdf文件保存根目录
:return:    recognition_list: 识别内容列表
            image_list: 图片信息列表。包含图片base64编码img_base64，图片名称img_name，图片页码img_num，图片路径img_path

"""
def handle_file(files, debug, save_root, rotate_res_url, number, pdf_path):
    recognition_list = []
    image_list = []
    for i, file in enumerate(files):
        if not file or not file.filename:
            res = error_handle(40101)
            if number == 1:
                return res, None, None
            res['image_name'] = file.filename
            recognition_list.append(res)
            continue
        img_name = file.filename
        file_type = img_name.rsplit('.', 1)[1]
        image_path = None
        # 文件为pdf格式
        if file_type == 'pdf' or file_type == 'PDF':
            pdf_bytes = file.read()
            # 保存pdf文件(未用，先保留)
            # pdf_name = get_time_str() + '_' + file.filename
            # pdf_path = pdf_path + pdf_name
            # pdf_path = pdf_path.replace('\\', '/')
            # if debug:
            #     if not os.path.exists(pdf_path):
            #         os.makedirs(pdf_path)
            #     with open(pdf_path, 'wb') as pdf:
            #         pdf.write(pdf_bytes)
            # pdf文件转图片
            images = convert_from_bytes(pdf_bytes)
            if len(images) != 1 and number == 1:
                res = error_handle(40309)
                return res, None, None
            else:
                for n, image in enumerate(images):
                    img_io = BytesIO()
                    image.save(img_io, 'PNG')
                    img_types = img_io.getvalue()
                    img_base64 = base64.b64encode(img_types)
                    # debug为True时，保存图片到本地，返回图片路径
                    if debug:
                        img_url_name = get_time_str() + "_" + img_name.split('.')[0] + '_' + str(n) + '.png'
                        save_image2file(image, img_url_name, save_root)
                        time_dir = time.strftime('%Y-%m-%d')
                        image_path = rotate_res_url + '0/' + time_dir + '/' + img_url_name
                    image_info = {'image_name': img_name.split('.')[0] + '_' + str(n) + '.png', 'image_base64': img_base64,
                                  'image_path': image_path, 'image_num': n + 1}
                    image_list.append(image_info)
        else:
            if os.path.splitext(img_name)[-1].replace('.', '') not in ALLOWED_EXTENSIONS:
                res = error_handle(40203)
                if number == 1:
                    return res, None, None
                res['imageName'] = file.filename
                recognition_list.append(res)
                continue
            img_types = file.stream.read()
            img_base64 = base64.b64encode(img_types)
            img_url_name = get_time_str() + "_" + img_name
            # debug为True时，保存图片到本地，返回图片路径
            if debug:
                save_image2file(file, img_url_name, save_root)
                time_dir = time.strftime('%Y-%m-%d')
                image_path = rotate_res_url + '0/' + time_dir + '/' + img_url_name
            image_info = {'img_name': img_name, 'img_base64': img_base64, 'image_path': image_path, 'image_num': i + 1}
            image_list.append(image_info)
    return RES, recognition_list, image_list


"""
Description:    获取当前时间
:return:        当前时间%Y-%m-%d-%H-%M-%S
"""
def get_time_str():
    return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))


"""
Description: 保存图片，返回保存地址
:param file: 需要保存的图片
:param filename: 需要保存图片的名称
:param save_root: 图片保存根目录
:return: 
"""
def save_image2file(file, filename, save_root):
    time_dir = time.strftime("%Y-%m-%d")
    data_dir = os.path.join(save_root, time_dir)
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)
    if filename is None:
        filename = file.filename
    upload_path = os.path.join(data_dir, filename)
    file.save(upload_path)
    return upload_path
