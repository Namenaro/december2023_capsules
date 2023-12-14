from utils import get_signal_snippet, draw_ECG, Distr, HtmlLogger

import numpy as np
from numpy import dot
from numpy.linalg import norm
import matplotlib.pyplot as plt
from statistics import mean



class KDistr:
    def __init__(self, signal, inertia):
        self.signal = signal
        self.inertia = inertia

    def get_sample(self):
        sample = []
        for x in range(len(signal) - inertia):
            a = self._get_one_element(x)
            sample.append(a)
        return sample

    def _get_one_element(self, x):
        ys = self.signal[x:x + self.inertia]
        ks = self._get_segments_ks(ys)
        k = mean(ks)
        return k

    def _get_segments_ks(self, ys):
        ks = []
        for i in range( len(ys)-1):
            y = ys[i]
            ynext = ys[i+1]
            k = ynext - y
            ks.append(k)
        return ks



if __name__ == '__main__':
    signal = get_signal_snippet(lead_name='i', start_coord=340, end_coord=435)
    log = HtmlLogger("K_LOG")

    for inertia in range(2, 16, 2):
        sample = KDistr(signal, inertia).get_sample()
        fig, ax = plt.subplots()
        ax.hist(sample)
        log.add_text("Инерция = " + str(inertia) + " :")
        log.add_fig(fig)
