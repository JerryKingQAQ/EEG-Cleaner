# -*- coding = utf-8 -*-
# @File : bad_seg_clean.py
# @Software : PyCharm
import mne
from mne.preprocessing import find_eog_events, find_ecg_events


def bad_seg_clean(raw,thresh):
    raw_copy = raw.copy()
    eog_events = find_eog_events(raw_copy, ch_name=raw.info['ch_names'][0], thresh=thresh)
    eog_onsets = eog_events[:, 0] / raw.info['sfreq'] - 0.25
    eog_durations = [0.5] * len(eog_events)
    descriptions = ['BAD_'] * len(eog_events)
    eog_annot = mne.Annotations(eog_onsets, eog_durations, descriptions, orig_time=raw.info['meas_date'])
    raw.set_annotations(eog_annot)
    # eeg_picks = mne.pick_types(raw_copy.info, meg=False, eeg=True)
    # raw.plot(events=eog_events, order=eeg_picks,duration=10, scalings=dict(eeg=50))


    # ecg_events = find_ecg_events(raw_copy, ch_name=raw.info['ch_names'][0])[0]
    # ecg_onsets = ecg_events[:, 0] / raw.info['sfreq'] - 0.25
    # ecg_durations = [0.5] * len(ecg_events)
    # descriptions = ['bad_ecg_events'] * len(ecg_events)
    # ecg_annot = mne.Annotations(ecg_onsets, ecg_durations, descriptions, orig_time=raw.info['meas_date'])
    # raw.set_annotations(ecg_annot)

    # 自动标记坏道
    # bad_channels = mne.preprocessing.find_bad_channels_maxwell(raw)
    # print(bad_channels)

    # 去坏段 插值重建
    # fig = raw.plot(duration=50, n_channels=25, scalings=dict(eeg=50))
    # fig.canvas.key_press_event('a')


    return raw
