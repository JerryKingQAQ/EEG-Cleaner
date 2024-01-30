# -*- coding = utf-8 -*-
# @File : ica_clean.py
# @Software : PyCharm
import os

import matplotlib.pyplot as plt
from mne.preprocessing import ICA


def ica_clean(raw):

    # ICA分析
    ica = ICA(max_iter='auto', n_components=30)
    raw_for_ica = raw.copy()
    ica.fit(raw_for_ica, reject_by_annotation=False)
    n_components = ica.n_components
    print(raw_for_ica.info)

    ica.plot_components(nrows=6, ncols=5, show=False)
    plt.savefig("./img/ICA/plot_components.jpg")

    for i in range(n_components):
        ica.plot_properties(raw, picks=[i], show=False)
        plt.savefig(f"./img/ICA/ICA_{i}.jpg")

    # 自动排除伪迹成分
    ecg_indices, ecg_scores = ica.find_bads_ecg(raw_for_ica, ch_name=raw_for_ica.info['ch_names'][0]
                                                , reject_by_annotation=False)
    eog_indices, eog_scores = ica.find_bads_eog(raw_for_ica, ch_name=raw_for_ica.info['ch_names'][0]
                                                , reject_by_annotation=False)
    mus_indices, mus_scores = ica.find_bads_muscle(raw_for_ica)
    artifacts_indices = ecg_indices + eog_indices + mus_indices
    ica.exclude = artifacts_indices
    cleaned_raw = ica.apply(raw_for_ica)

    # 各成分时序信号图
    # ica.plot_sources(raw_for_ica)

    # 绘制各成分地形图
    # ica.plot_components()

    # 单独可视化每个成分
    # ica.plot_properties(raw, picks=[0, 1, 5, 10, 16, 24])

    # 画图
    # raw.plot_psd(average=True)
    # raw.plot(duration=100, scalings=dict(eeg=50))
    # cleaned_raw.plot(duration=100, scalings=dict(eeg=50))
    # plt.show()
    return cleaned_raw
