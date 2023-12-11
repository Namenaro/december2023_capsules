from utils import get_signal_snippet, draw_ECG, Distr, HtmlLogger

import numpy as np
from numpy import dot
from numpy.linalg import norm
import matplotlib.pyplot as plt
from statistics import mean

# TODO считаем что регион информативности это весь сигнал ситуации
# величина r(k, inertia|region, info_region)
# TODO до полноценного замера r законоемрномти не хватает еще оценщика предстаказий о концах
# TODO еще пока висит вопрос о вхожддении процента устраненной ошибки в r законоемрномти. Там есть варианты:
#     1) в apply уже должно это быть учтено (например, веротяность, что именно такая доля ошибки устранеится из одного сегмента
#     2) замер разделить на два процесса: сначала релаксация с максимизацией неслучайности. А когда отрелаксировано
#     к большой несоучайности (если это удалось!), то вот в этот момент мы считаем "известными" все реальные значения
#     предсказанных параметров и только тут их мерим их "длину редакции". Делим выигрыш в ошибке на длину редакции. И
#     это и есть ответ... При таком подходе длина редакции и уровень неслучайности это разные вещи

class Region:
    def __init__(self, x1, x2):
        self.x1 = x1
        self.x2 = x2

    def is_in(self, x):
        if self.x2 >= x >= self.x1:
            return True
        return False

    def get_prediction_for_y2(self, v0, x, k):
        y2 = v0 + (x - self.x1 + 1) * k
        return y2


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
        self.inertia = 5


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


    def draw(self):
        fig, ax = plt.subplots()
        draw_ECG(ax, self.signal)
        ax.vlines(x=self.region.x1, ymin=0, ymax=max(self.signal), colors='red', lw=2, alpha=0.5)
        ax.vlines(x=self.region.x2, ymin=0, ymax=max(self.signal), colors='red', lw=2, alpha=0.5)

        ax.vlines(x=self.info_region.x1, ymin=0, ymax=max(self.signal), colors='blue', lw=2, alpha=0.5)
        ax.vlines(x=self.info_region.x2, ymin=0, ymax=max(self.signal), colors='blue', lw=2, alpha=0.5)
        plt.show()

    def get_e_sample_random(self):
        for i in range(len(self.signal) - self.i)

    def get_e_smaple_fixed(self):
        pass

    def get_e_sample_fixed_positive(self):
        pass

    def get_e_sample_nevative(self):
        pass





if __name__ == "__main__":
    log = HtmlLogger("VAR3_LOG")
    task = Task(k=None)
    task.draw()

