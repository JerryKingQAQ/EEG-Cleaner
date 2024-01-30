# -*- coding = utf-8 -*-
# @File : find_bad_channels.py
# @Software : PyCharm
import mne
import numpy as np
import autoreject

def detect_bad_channels_avg_diff(raw_data, threshold=10.0):
    data = raw_data.get_data()
    avg_diff = np.mean(np.abs(np.diff(data, axis=1)), axis=1)
    bad_channels = np.where(avg_diff > threshold)[0]
    return bad_channels


def detect_bad_channels_variance(raw_data, threshold=1e-6):
    data = raw_data.get_data()
    variances = np.var(data, axis=1)
    bad_channels = np.where(variances < threshold)[0]
    return bad_channels


def detect_bad_channels_power_spectrum(raw_data, threshold=10.0):
    data = raw_data.get_data()
    freqs, psd = mne.time_frequency.psd_welch(data, fmin=1, fmax=50)
    psd_mean = np.mean(psd, axis=2)
    bad_channels = np.where(psd_mean > threshold)[0]
    return bad_channels

def find_bad_channels(raw_data):
    ar = autoreject.AutoReject()
    # 检测坏道
    raw_clean, reject_log = ar.fit_transform(raw_data, return_log=True)
    # 获取被拒绝的时间段
    rejected_segments = autoreject.get_rejection_threshold(reject_log)

    print(raw_clean, reject_log)
    print(rejected_segments)



if __name__ == "__main__":
    # 使用示例
    raw = mne.io.read_raw_eeglab('your_data.eeg')
    bad_channels = detect_bad_channels_power_spectrum(raw, threshold=10.0)
    print("Bad channels:", bad_channels)
