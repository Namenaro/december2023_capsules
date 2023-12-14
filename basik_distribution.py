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
        max_x = len(self.signal) - self.inertia-1
        for x in range(max_x):
            a = self._get_one_element(x)
            sample.append(a)
        return sample

    def _get_one_element(self, x):
        ys = self.signal[x:x + self.inertia+1]
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

class Samples:
    def __init__(self, signal, inertia):
        self.all = KDistr(signal[11:-1], inertia).get_sample()

        positive_reg = signal[11:43]
        self.poss = KDistr(positive_reg, inertia).get_sample()

        negative_reg = signal[44:-1]
        self.negs = KDistr(negative_reg, inertia).get_sample()


    def get_all_pos_neg(self):
        return self.all, self.poss, self.negs

if __name__ == '__main__':
    signal = get_signal_snippet(lead_name='i', start_coord=340, end_coord=435)
    log = HtmlLogger("K_LOG")
    log.add_text("Гистограммы реальных К-интерционного (по всему сигналу, в позитивном регионе, в негативном)")

    for inertia in range(2, 16, 2):
        samples_obj = Samples(signal, inertia)
        all, poss, negs = samples_obj.get_all_pos_neg()
        fig, ax = plt.subplots()
        ax.hist(all, color='gray', alpha=0.3)
        ax.hist(poss, label="+", color='green', alpha=0.5)
        ax.hist(negs, label="-", color='red', alpha=0.5)
        ax.legend()
        log.add_text("Инерция = " + str(inertia) + " :")
        log.add_fig(fig)
