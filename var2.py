from utils import get_signal_snippet, draw_ECG, Distr, HtmlLogger

import numpy as np
from numpy import dot
from numpy.linalg import norm
import matplotlib.pyplot as plt


# величина r(k|region, info_region)

class Region:
    def __init__(self, x1, x2):
        self.x1 = x1
        self.x2 = x2

    def is_in(self, x):
        if self.x2 >= x >= self.x1:
            return True
        return False


class InfoRegion:
    def __init__(self, x1, x2):
        self.x1 = x1
        self.x2 = x2


class Task:
    def __init__(self, k=None):
        self.signals = self._get_signals()
        self.signal = get_signal_snippet(lead_name='i', start_coord=340, end_coord=435)
        self.region = Region(10, 50)
        self.info_region = InfoRegion(0, 91)
        if k is None:
            self.k = self._get_k_best()
        else:
            self.k = k


        self.cos_distr = self.get_cos_profits_distr()


    def _get_signals(self):
        signals = get_signal_snippet(lead_name='i', start_coord=0, end_coord=435)
        #signals = signals + get_signal_snippet(lead_name='ii', start_coord=0, end_coord=435)
        # signals = signals + get_signal_snippet(lead_name='iii', start_coord=0, end_coord=435)
        return signals

    def _get_k_best(self):
        x1 = 10
        y1 = self.signal[x1]
        x2 = 50
        y2 = self.signal[x2]
        dx = x2 - x1
        dy = y2 - y1
        k = dy / dx
        print ("k={0:0.2f}".format(k))
        return k

    def get_cos_profit_in_point(self, x, signal):
        y1 = signal[x]
        y2 = signal[x + 1]
        dy_real = y2 - y1

        predicted_vector = np.array([1, self.k])
        real_vector = np.array([1, dy_real])
        default_vector = np.array([1, 0])
        cos_try = dot(real_vector, predicted_vector) / (norm(real_vector) * norm(predicted_vector))
        cos_def = dot(real_vector, default_vector) / (norm(real_vector) * norm(default_vector))
        return cos_try-cos_def


    def draw(self):
        fig, ax = plt.subplots()
        draw_ECG(ax, self.signal)
        ax.vlines(x=self.region.x1, ymin=0, ymax=max(self.signal), colors='red', lw=2, alpha=0.5)
        ax.vlines(x=self.region.x2, ymin=0, ymax=max(self.signal), colors='red', lw=2, alpha=0.5)

        ax.vlines(x=self.info_region.x1, ymin=0, ymax=max(self.signal), colors='blue', lw=2, alpha=0.5)
        ax.vlines(x=self.info_region.x2, ymin=0, ymax=max(self.signal), colors='blue', lw=2, alpha=0.5)
        plt.show()


    def get_cos_profits_distr(self):
        res = []
        for x in range(0, len(self.signals) - 1):
            c = self.get_cos_profit_in_point(x, self.signals)
            res.append(c)
        return Distr(sample=res)

    def get_r_positive(self):
        result = []
        for x in range(self.region.x1, self.region.x2 - 1):
            real_cos_profit = self.get_cos_profit_in_point(x, self.signal)
            p = self.cos_distr.p_event_more_eq_than_val(real_cos_profit)
            r = 0.5 - p
            result.append(r)
        return sum(result)

    def get_r_negative(self):
        result = []
        for x in range(self.info_region.x1, self.info_region.x2 - 1):
            if self.region.is_in(x):
                continue
            real_cos = self.get_cos_profit_in_point(x, self.signal)
            p = self.cos_distr.p_event_more_eq_than_val(real_cos)
            r = p-0.5
            result.append(r)
        return sum(result)

    def get_r_in_task(self):
        r_pos = self.get_r_positive()
        r_neg = self.get_r_negative()

        r = r_pos + r_neg
        return r_pos, r_neg, r


if __name__ == "__main__":
    log = HtmlLogger("VAR2_LOG")
    task = Task(k=None)
    task.draw()
    r_pos, r_neg, r = task.get_r_in_task()
    log.add_text("best_k={0:0.2f}".format(task.k))
    log.add_text("r={0:0.2f}".format(r))

    log.add_line_little()

    ks = list(range(-9, 9, 2))
    rs = []
    r_ps = []
    r_ns = []
    for k in ks:
        task = Task(k=k)
        r_pos, r_neg, r = task.get_r_in_task()
        print(r)
        rs.append(r)
        r_ps.append(r_pos)
        r_ns.append(r_neg)

    fig, ax = plt.subplots()
    ax.plot(ks, rs)
    log.add_fig(fig)

    fig, ax = plt.subplots()
    ax.plot(ks, r_ns)
    log.add_fig(fig)

    fig, ax = plt.subplots()
    ax.plot(ks, r_ps)
    log.add_fig(fig)
