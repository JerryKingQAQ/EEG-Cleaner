# -*- coding = utf-8 -*-
# @File : show_img.py
# @Software : PyCharm
from matplotlib import pyplot as plt


def show_img(raw, scaling):
    raw.plot(duration=50, scalings={'eeg':scaling})
    plt.show()