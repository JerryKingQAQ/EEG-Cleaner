# -*- coding = utf-8 -*-
# @File : load_data.py
# @Software : PyCharm
import os

import mne
import numpy as np
import scipy.io as sio
from mne import create_info
from mne.io import RawArray

from utils.bad_channels_clean import bad_channels_clean


def traverse_folder(folder_path):
    mat_files = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and file_name.endswith('.mat'):
            mat_files.append(file_path)
        elif os.path.isdir(file_path):
            mat_files.extend(traverse_folder(file_path))  # 递归调用遍历子文件夹
    return mat_files


def transpose_list(lst):
    return np.array(list(map(list, zip(*lst))))


def read_matdata(filepath, key):
    label = filepath.split('_')[-1].split('.')[0]
    f = sio.loadmat(filepath)
    if f[key].shape[0] > 128: # 如果导联数不在第一维
        f[key] = transpose_list(f[key])
    return f[key], label


def load_data(file_path):
    # 创建信息对象
    rawdata, label = read_matdata(file_path, 'data')
    n_channels = rawdata.shape[0]
    print(rawdata.shape[1])
    ch_names = np.genfromtxt('./珠江医院_音乐治疗数据/_dot_MusicTherapy_51EEGECG_1Sync.txt', dtype=str, delimiter=',',
                             usecols=[3]).tolist()
    ch_exclude = []
    # 通过判断电极数量，选择使用哪种电极配置文件
    if n_channels == 62:
        ch_62_name = np.genfromtxt('./珠江医院_音乐治疗数据/_dot_MusicTherapy_62EEG_1ECG_1Sync.txt', dtype=str, delimiter=',',
                                   usecols=[3]).tolist()
        for ch in ch_62_name:
            if ch not in ch_names:
                ch_exclude.append(ch_62_name.index(ch))
    # 将多余的电极剔除
    rawdata = np.delete(rawdata, ch_exclude, axis=0)

    # 加载配准后的头表模板文件
    montage = mne.channels.make_standard_montage('standard_1005')

    sfreq = 2000
    highpass_freq = 0.5
    lowpass_freq = 100
    info = create_info(ch_names, sfreq, ch_types='eeg')
    info.set_montage(montage)

    # 创建原始对象 滤波
    raw = RawArray(rawdata, info)
    raw = raw.notch_filter(freqs=(60))
    raw = raw.notch_filter(freqs=(50))
    raw = raw.filter(l_freq=highpass_freq, h_freq=lowpass_freq)
    print(raw.info)

    return raw
