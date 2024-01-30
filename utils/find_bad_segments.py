# -*- coding = utf-8 -*-
# @File : find_bad_segments.py
# @Software : PyCharm
import numpy as np


def detect_bad_segments(data, sfreq, threshold_uv, duration):
    """Detects bad segments in EEG data based on thresholding.

    Args:
        data (ndarray): EEG data of shape (n_channels, n_samples).
        sfreq (float): Sampling frequency of the data.
        threshold (float): Threshold value for segment rejection.
        duration (float): Minimum duration (in seconds) for a segment to be considered bad.

    Returns:
        bad_segments (list): List of bad segment indices.
    """

    # Calculate the minimum number of samples for a bad segment
    min_samples = int(duration * sfreq)

    # Compute the root mean square (RMS) of the data along channels
    rms = np.sqrt(np.mean(data ** 2, axis=0))

    # Identify segments where RMS exceeds the threshold
    exceed_threshold = np.where(rms > threshold_uv)[0]

    # Find contiguous segments with duration greater than min_samples
    bad_segments = []
    segment_start = None
    for i, idx in enumerate(exceed_threshold):
        if segment_start is None:
            segment_start = idx
        if i == len(exceed_threshold) - 1 or exceed_threshold[i + 1] != idx + 1:
            segment_duration = idx - segment_start + 1
            if segment_duration >= min_samples:
                bad_segments.append((segment_start, idx + 1))
            segment_start = None

    return bad_segments

if __name__ == '__main__':
    # 创建空的numpy数组来存储坏段的起始时间、持续时间和描述
    onsets = np.array([])
    durations = np.array([])
    descriptions = np.array([])

    drop_bad_seg_raw = raw.copy()
    bad_segments = detect_bad_segments(raw.get_data(), sfreq=2000, threshold_uv=2, duration=2)
    for bad_seg in bad_segments:
        onset = bad_seg[0]
        duration = bad_seg[1] - onset
        onsets = np.concatenate((onsets, np.array([onset])), axis=0)
        durations = np.concatenate((durations, np.array([duration])), axis=0)
    descriptions = np.concatenate((descriptions, np.array(['bad segment'])), axis=0)
    annotations = mne.Annotations(onset=onsets, duration=durations, description=descriptions)
    drop_bad_seg_raw.set_annotations(annotations)
    drop_bad_seg_raw.drop_bad()