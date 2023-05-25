import numpy as np
import pandas as pd
import scipy as sp
import MCMC_barrier_effect


def killworth(data_mat, data_dict):
    known = data_dict["known"]
    known_len = len(known)
    N = data_dict["N"]
    n = data_mat.shape[0]

    indices = range(known_len)
    indices_k = range(known_len, data_mat.shape[1])

    NSUM_d_back = np.empty(n)
    for i in range(n):
        NSUM_d_back[i] = sum(data_mat[i, :]) * (N / sum(known))

    return N * data_mat[:, indices_k].sum(axis=0) / sum(NSUM_d_back), NSUM_d_back, n


def killworth_start(data_mat, data_dict):
    known = data_dict["known"]
    N = data_dict["N"]

    NK_start, NSUM_d_back, n = killworth(data_mat, data_dict)

    d_start = NSUM_d_back.copy()

    for i in range(n):
        maxi = max(data_mat[i, :])
        if d_start[i] < maxi:
            d_start[i] = maxi + 1

    if np.sort(NSUM_d_back)[0] == 0:
        zero_index = np.where(NSUM_d_back == 0)[0]
        d_start[zero_index] = 1
        NSUM_d_back = NSUM_d_back[-zero_index]

    l_norm_start = sp.stats.lognorm.fit(NSUM_d_back)
    mu_start = l_norm_start[1]
    sigma_start = l_norm_start[2]

    return NK_start, d_start, mu_start, sigma_start


if __name__ == "__main__":
    data = {}
    with open("/Users/tomas/Downloads/McCarty.txt") as f:
        for line in f:
            y = line.split()
            if len(y) > 0:
                data[y[0]] = np.array([float(i) for i in y[1:]])
    y, d = MCMC_barrier_effect.simulate_bar(data, 100)
    NK, d, mu, sigma = killworth_start(y, data)
