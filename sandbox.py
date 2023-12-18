from utils import get_signal_snippet, draw_ECG, Distr, HtmlLogger
from basik_distribution_k import SamplesK
from basic_distrubution_cos import VAR_1

import numpy as np
from numpy import dot
from numpy.linalg import norm
import matplotlib.pyplot as plt
from statistics import mean

def draw(all, poss, negs, log):
    fig, ax = plt.subplots()
    ax.hist(all, color='gray', alpha=0.3)
    ax.hist(poss, label="+", color='green', alpha=0.5)
    ax.hist(negs, label="-", color='red', alpha=0.5)
    ax.legend()
    #log.add_text("Инерция = " + str(inertia) + " :")
    log.add_fig(fig)

def experiment(inertia, log, k_predicted):
    signal = get_signal_snippet(lead_name='i', start_coord=340, end_coord=435)
    k_sample_pbj = SamplesK(signal, inertia)
    all, poss, negs = k_sample_pbj.get_all_pos_neg()
    profit = VAR_1(all, poss, negs, k_predicted)
    log.add_text("{:.2f}".format(profit))
    draw(all, poss, negs, log)



if __name__ == '__main__':
    k_predicted = 6
    log = HtmlLogger("COS_LOG")
    for inertia in range(2, 16, 5):
        experiment(inertia, log, k_predicted=k_predicted)