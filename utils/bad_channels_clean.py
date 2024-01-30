# -*- coding = utf-8 -*-
# @File : bad_channels_clean.py
# @Software : PyCharm
import mne
import numpy as np
from autoreject import AutoReject
from mne.io import RawArray


def bad_channels_clean(raw, info, ch_names):
    # 定义时间段的长度和重叠（根据需求进行调整）
    duration = 10.0  # 时间段的长度（单位：秒）
    overlap = 0.0  # 重叠部分的比例

    # 获取原始数据的采样频率
    sfreq = raw.info['sfreq']
    # 计算时间段的采样点数和重叠的采样点数
    n_samples = int(duration * sfreq)
    n_overlap = int(n_samples * overlap)

    # 创建虚拟事件，基于时间段的分割
    events = mne.make_fixed_length_events(raw, duration=duration, overlap=n_overlap)
    epochs = mne.Epochs(raw, events, tmin=0, tmax=duration, baseline=None, preload=True)

    # 坏道插值重建
    ar = AutoReject()
    epochs_clean = ar.fit_transform(epochs)  # doctest: +SKIP

    epochs_data = epochs_clean.get_data().transpose((1, 0, 2))
    new_raw_data = []
    for lead in range(epochs_data.shape[0]):
        new_lead_data = []
        for epoch in range(epochs_data.shape[1]):
            new_lead_data.extend(epochs_data[lead, epoch, :])
        new_raw_data.append(new_lead_data)
    new_raw_data = np.array(new_raw_data)
    raw = RawArray(new_raw_data, info)
    picks = mne.pick_types(
        info, meg=False, eeg=True, stim=False,
        include=ch_names
    )
    raw.save("raw.fif", picks=picks, overwrite=True)
    raw = mne.io.read_raw_fif("raw.fif", preload=True, verbose='ERROR')
    return raw