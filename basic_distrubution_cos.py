from basik_distribution_k import KDistr

import numpy
from numpy.linalg import norm
from random import choice


def get_err(k_predicted, k_real):
    from numpy.linalg import norm
    v1 = numpy.array([1, k_real])
    v2 = numpy.array([1, k_predicted])
    return 1 - numpy.dot(v1, v2) / (norm(v1) * norm(v2))



def get_cos_err_sample(all_k_real, sample_size):
    errs_sample = []
    for _ in range(sample_size):
        k_real = choice(all_k_real)
        k_predicted = choice(all_k_real)
        err = get_err(k_predicted, k_real)
        errs_sample.append(err)
    return errs_sample


def get_real_errs(k_real_list, k_predicted):
    errs = []
    for k in k_real_list:
        err = get_err(k_predicted, k)
        errs.append(err)
    return errs

def VAR_1(all, poss, negs, k_predicted):
    pos_errs = get_real_errs(k_real_list=poss, k_predicted=k_predicted)
    neg_errs = get_real_errs(k_real_list=poss, k_predicted=k_predicted)
    pos_profit = 0.5 - sum(pos_errs)/len(poss)
    neg_profit = sum(neg_errs)/len(negs) - 0.5
    profit = pos_profit + neg_profit
    return profit


if __name__ == '__main__':
    k = 1/2

    print(get_err(k_predicted=0, k_real=1))
