from utils import get_signal_snippet, draw_ECG, Distr, HtmlLogger

import numpy as np
from numpy import dot
from numpy.linalg import norm
import matplotlib.pyplot as plt
from statistics import mean


def experiment_FIX_ALL_EXEPT_INERTIA(inertia, log):

    signal = get_signal_snippet(lead_name='i', start_coord=340, end_coord=435)
    device = Device(signal=signal, k=-6, inertia=inertia)

    An = []
    for x in range(44, len(signal) - inertia):
        a = device.A_meank(x)
        An.append(a)

    fig, ax = plt.subplots()
    # draw_ECG(ax, signal)
    # ax.plot(As, 'red')
    ax.hist(An)

    Ap = []
    for x in range(11, 43 - inertia):
        a = device.A_meank(x)
        Ap.append(a)
    ax.hist(Ap, label='positive')
    ax.legend()


    normer = ErProbNormer(Ap=Ap, An=An)
    r = normer.get()
    log.add_text("Инерция = " + str(inertia) + ", r = " + format(r, '.2f') +  " :")
    log.add_fig(fig)


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


class ErProbNormer:
    def __init__(self, Ap, An):
        self.Ap = Ap
        self.An = An
        A = self.Ap + self.An
        self.distr = Distr(A)

    def get_positive(self):
        pp = []
        for er in self.Ap:
            p_of_so_good = 0.5 - self.distr.get_p_of_event(0, er)
            pp.append(p_of_so_good)

        p_positive = sum(pp)
        normer = 0.5 * len(self.Ap)
        return p_positive/normer

    def get_negative(self):
        pp = []
        for er in self.An:
            p_of_so_good = 0.5 - self.distr.get_p_of_event(0, er)
            pp.append(-p_of_so_good)

        p = sum(pp)
        normer = 0.5 * len(self.An)
        return p/normer

    def get(self):
        pos = self.get_positive()
        neg = self.get_negative()
        r = pos + neg
        return r


if __name__ == '__main__':
    log = HtmlLogger("D1_LOG_INERTIA_EFFECT")
    for inertia in range(2, 16, 2):
        experiment_FIX_ALL_EXEPT_INERTIA(inertia, log)




