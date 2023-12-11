from utils import get_signal_snippet, draw_ECG, Distr, HtmlLogger

import numpy as np
from numpy import dot
from numpy.linalg import norm
import matplotlib.pyplot as plt
from statistics import mean


def experiment(inertia):
    signal = get_signal_snippet(lead_name='i', start_coord=340, end_coord=435)
    device = Device(signal=signal, k=-6, inertia=inertia)

    As = []
    for x in range(44, len(signal) - inertia):
        a = device.A_meank(x)
        As.append(a)

    fig, ax = plt.subplots()
    # draw_ECG(ax, signal)
    # ax.plot(As, 'red')
    ax.hist(As)

    As = []
    for x in range(11, 43 - inertia):
        a = device.A_meank(x)
        As.append(a)
    ax.hist(As, label='positive')
    ax.legend()
    return fig

class Device:
    def __init__(self, signal, k, inertia):
        self.signal = signal
        self.k = k
        self.inertia = inertia

    def A_meank(self, x):
        ys = self.signal[x:x+self.inertia]
        ks = self.get_sements_ks(ys)
        real = mean(ks)
        predicted = self.k
        err = abs(predicted - real)
        return err


    def get_sements_ks(self, ys):
        ks = []
        for i in range( len(ys)-1):
            y=ys[i]
            ynext = ys[i+1]
            k = ynext - y
            ks.append(k)
        return ks




if __name__ == '__main__':
    log = HtmlLogger("D1_LOG")
    for inertia in range(2,16,4):
        fig = experiment(inertia)
        log.add_text("Инерция = " + str(inertia) + " :")
        log.add_fig(fig)



