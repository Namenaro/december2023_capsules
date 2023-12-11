from utils import get_signal_snippet, draw_ECG, Distr

import numpy as np
from numpy import dot
from numpy.linalg import norm
import matplotlib.pyplot as plt


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
            self.dy = self._get_dy_predicted()
        else:
            self.dy = k

        self.dot_distr = self.get_dot_distr()
        self.cos_distr = self.get_cos_distr()


    def _get_signals(self):
        signals = get_signal_snippet(lead_name='i', start_coord=0, end_coord=435)
        signals = signals + get_signal_snippet(lead_name='ii', start_coord=0, end_coord=435)
        # signals = signals + get_signal_snippet(lead_name='iii', start_coord=0, end_coord=435)
        return signals

    def _get_dy_predicted(self):
        x1 = 10
        y1 = self.signal[x1]
        x2 = 50
        y2 = self.signal[x2]
        dx = x2 - x1
        dy = y2 - y1
        k = dy / dx
        print ("k={0:0.2f}".format(k))
        return k

    def get_cos_in_point(self, x, signal):
        y1 = signal[x]
        y2 = signal[x + 1]
        dy_real = y2 - y1
        predicted_vector = np.array([1, self.dy])
        real_vector = np.array([1, dy_real])
        cos = dot(real_vector, predicted_vector) / (norm(real_vector) * norm(predicted_vector))
        return cos

    def get_dot_prod_in_point(self, x, signal):
        y1 = signal[x]
        y2 = signal[x + 1]
        dy_real = y2 - y1
        predicted_vector = np.array([1, self.dy])
        real_vector = np.array([1, dy_real])
        dot_prod = dot(real_vector, predicted_vector)
        return dot_prod

    def draw(self):
        fig, ax = plt.subplots()
        draw_ECG(ax, self.signal)
        ax.vlines(x=self.region.x1, ymin=0, ymax=max(self.signal), colors='red', lw=2, alpha=0.5)
        ax.vlines(x=self.region.x2, ymin=0, ymax=max(self.signal), colors='red', lw=2, alpha=0.5)

        ax.vlines(x=self.info_region.x1, ymin=0, ymax=max(self.signal), colors='blue', lw=2, alpha=0.5)
        ax.vlines(x=self.info_region.x2, ymin=0, ymax=max(self.signal), colors='blue', lw=2, alpha=0.5)
        plt.show()

    def get_dot_distr(self):
        dot_prods = []
        for x in range(0, len(self.signals) - 1):
            dot_prod = self.get_dot_prod_in_point(x, self.signals)
            dot_prods.append(dot_prod)
        return Distr(sample=dot_prods)

    def get_cos_distr(self):
        res = []
        for x in range(0, len(self.signals) - 1):
            c = self.get_cos_in_point(x, self.signals)
            res.append(c)
        return Distr(sample=res)

    def get_r_positive(self):
        result = []
        for x in range(self.region.x1, self.region.x2 - 1):
            real_cos = self.get_cos_in_point(x, self.signal)
            p = self.cos_distr.p_event_more_eq_than_val(real_cos)
            r = 1 - p
            result.append(r)
        return sum(result)

    def get_r_negative(self):
        result = []
        for x in range(self.info_region.x1, self.info_region.x2 - 1):
            if self.region.is_in(x):
                continue
            real_cos = self.get_cos_in_point(x, self.signal)
            p = self.cos_distr.p_event_more_eq_than_val(real_cos)
            r = -p
            result.append(r)
        return sum(result)

    def get_r_in_task(self):
        r_pos = self.get_r_positive()
        r_neg = self.get_r_negative()

        print(r_pos)
        print(r_neg)
        return r_pos #+ r_neg


if __name__ == "__main__":
    task = Task(k=None)
    r = task.get_r_in_task()
    print("r={0:0.2f}".format(r))

    task = Task(k=6)
    r = task.get_r_in_task()
    print("r={0:0.2f}".format(r))
