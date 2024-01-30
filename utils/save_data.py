# -*- coding = utf-8 -*-
# @File : save_data.py
# @Software : PyCharm
import os

from scipy.io import savemat

from utils.show_img import show_img


def save_data(raw, tag, file_path):
    data = raw.get_data(reject_by_annotation='omit')
    # 获取文件夹名
    folder_path = os.path.dirname(file_path)
    save_folder_path = os.path.join('.', tag + "_" + folder_path)
    os.makedirs(save_folder_path, exist_ok=True)
    # 获取文件名
    save_file_name = os.path.basename(file_path)
    save_file_path = os.path.join(save_folder_path, save_file_name)
    savemat(save_file_path, {'data': data})  # 将数据保存为名为'data'的变量

