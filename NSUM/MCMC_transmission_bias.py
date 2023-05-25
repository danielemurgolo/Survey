import numpy as np
import pandas as pd
import scipy as sp
import killworth as kw


def simulate_trans(data_dict, n, mu=5, sigma=1):
    if "mu" in data_dict:
        if len(data_dict["mu"]) > 0:
            mu = data_dict["mu"][0]
    if "sigma" in data_dict:
        if len(data_dict["sigma"]) > 0:
            sigma = data_dict["sigma"][0]

    N = data_dict["N"][0]
    d = np.random.lognormal(mu, sigma, n)

    known_all = np.concatenate((data_dict['known'], data_dict['unknown']))
    known_all_len = len(known_all)

    tauK = np.repeat(1, len(data_dict["unknown"]))
    tau = np.concatenate((np.repeat(1, len(data_dict["known"])), tauK))

    p_pops = tau * known_all / N

    y = np.empty((n, known_all_len))

    for i in range(n):
        di = d[i]
        for j in range(known_all_len):
            y[i, j] = np.random.binomial(di, p_pops[j], 1)

    return y, d


def loglik_di_trans(data_mat, mu, sigma, di, N, known, wK):
    sum_binom = sum(np.log(sp.special.binom(di, data_mat)))

    sum_log_nk = sum(np.log(1 - known / N)) + sum(np.log(1 - wK / N))

    loglik = -np.log(di) - (np.log(di) - mu) ** 2 / (2 * sigma ** 2) + sum_binom + di * sum_log_nk

    return loglik


def loglik_wK_trans(data_mat, indices_k, N, d, wK, zK, tauK_prior):
    aK = tauK_prior[0]
    bK = tauK_prior[1]

    sum_di = sum(d)

    sum_yik = sum(data_mat[:, indices_k])

    loglik = sum_yik * np.log(wK / (N - wK)) + sum_di * np.log(1 - wK / N) + (aK - 2) / 2 * np.log(wK) + (bK - 1) \
             * np.log(1 - np.sqrt(wK / zK))

    return loglik


def loglik_zK_trans(wK, zK, tauK_prior):
    aK = tauK_prior[0]

    bK = tauK_prior[1]

    loglik = -(aK + 2) / 2 * np.log(zK) + (bK - 1) * np.log(1 - np.sqrt(wK / zK))

    return loglik


def mcmc_trans(data_mat, data_dict, iterations, burnin, size=None, mu_prior=(3, 8), sigma_prior=(0, 2), wK_tuning=None,
               zK_tuning=None, d_tuning=None):
    known = data_dict["known"]
    known_len = len(known)
    N = data_dict["N"]
    n = data_mat.shape[0]

    indices_k = range(known_len, data_mat.shape[1])

    if size is None:
        size = iterations

    NK_start, d_start, mu_start, sigma_start = kw.killworth_start(data_mat, data_dict)
    tauK_start = np.repeat(0.5, len(indices_k))
    tauK_priors = np.repeat((1, 1), len(indices_k)).reshape((len(indices_k), 2))

    if wK_tuning is None:
        wK_tuning = 0.25 * NK_start * tauK_start

    if d_tuning is None:
        d_tuning = 0.25 * d_start
    if zK_tuning is None:
        zK_tuning = 0.25 * NK_start / tauK_start

    wK_start = NK_start * tauK_start
    zK_start = NK_start / tauK_start

    mu_values = np.empty(size)
    sigma_values = np.empty(size)
    d_values = np.empty((data_mat.shape[0], size))
    wK_values = np.empty((len(indices_k), size))
    zK_values = np.empty((len(indices_k), size))

    d_curr = d_start
    wK_curr = wK_start
    zK_curr = zK_start
    mu_curr = mu_start
    sigma_curr = sigma_start
    keep = np.round(np.linspace(burnin + 1, burnin + iterations, size))
    keep_index = 1

    for i in range(burnin + iterations):
        if i % 10 == 0:
            print("Now on iteration ", i, "\n")

        d = d_curr
        wK = wK_curr
        zK = zK_curr
        mu = mu_curr
        sigma = sigma_curr

        for j in range(n):
            di_old = d[j]
            di_new = np.random.normal(di_old, d_tuning[j], 1)

            if di_new < max(data_mat[j, :]):
                d_curr[j] = di_old
            else:
                ratio = loglik_di_trans(data_mat[j, :], mu, sigma, di_new, N, known, wK) - loglik_di_trans(
                    data_mat[j, :], mu, sigma, di_old, N, known, wK)
                if np.isnan(ratio):
                    print("I broke for di for i = ", i, " where di.new was ", di_new, "\n")
                accept = min(0, ratio)
                logu = np.log(np.random.uniform(0, 1, 1))
                if logu < accept:
                    d_curr[j] = di_new
                else:
                    d_curr[j] = di_old

        d = d_curr

        for j in range(len(indices_k)):

            index_this_k = indices_k[j]
            wK_old = wK[j]
            wK_new = np.random.normal(wK_old, wK_tuning[j], 1)
            if (wK_new >= N or wK_new <= 0 or wK_new / zK[j] >= 1 or np.sqrt(wK_new * zK[j]) >= N):
                wK_curr[j] = wK_old
            else:
                ratio = loglik_wK_trans(data_mat, index_this_k, N, d, wK_new, zK[j], tauK_priors[j,]) - loglik_wK_trans(
                    data_mat, index_this_k, N, d, wK_old, zK[j], tauK_priors[j,])
                if np.isnan(ratio):
                    print("I broke on wK where my K was ", indices_k, " and my new.wK was ", wK.new, " and zK is ",
                          zK[j], "\n")

                accept = min(0, ratio)
                logu = np.random.uniform(0, 1, 1)

                if logu < accept:
                    wK_curr[j] = wK_new
                else:
                    wK_curr[j] = wK_old
        wK = wK_curr

        for j in range(len(indices_k)):
            zK_old = zK[j]
            zK_new = np.random.normal(zK_old, zK_tuning[j], 1)

            if (zK_new <= 0 or wK[j] / zK_new >= 1 or np.sqrt(wK[j] * zK_new) >= N):
                zK_curr[j] = zK_old
            else:
                ratio = loglik_zK_trans(wK[j], zK_new, tauK_priors[j, :]) - loglik_zK_trans(wK[j], zK_old,
                                                                                            tauK_priors[j, :])
                if np.isnan(ratio):
                    print("I broke on zK where my K was ", index_this_k, " and my new.zK was ", zK.new,
                          " and wK was currently ", wK[j], "\n")
                accept = min(0, ratio)
                logu = np.log(np.random.uniform(0, 1, 1))
                if logu < accept:
                    zK_curr[j] = zK_new
                else:
                    zK_curr[j] = zK_old

        zK = zK_curr
        mu_new = np.random.normal(sum(np.log(d)) / n, sigma / np.sqrt(n), 1)

        while (mu_new < mu_prior[0] or mu_new > mu_prior[1]):
            mu_new = np.random.normal(sum(np.log(d)) / n, sigma / np.sqrt(n), 1)

        mu_curr = mu_new
        mu = mu_curr

        sigma_new = 1 / np.sqrt(np.random.gamma((n - 1) / 2, 1 / 2 * sum((np.log(d) - mu) ** 2), 1))
        while (sigma_new < sigma_prior[0] or sigma_new > sigma_prior[1]):
            sigma_new = 1 / np.sqrt(np.random.gamma((n - 1) / 2, 1 / 2 * sum((np.log(d) - mu) ** 2), 1))
        sigma_curr = sigma_new
        if i == keep[keep_index]:
            d_values[:, keep_index] = d_curr
            wK_values[:, keep_index] = wK_curr
            zK_values[:, keep_index] = zK_curr
            mu_values[keep_index] = mu_curr
            sigma_values[keep_index] = sigma_curr
            keep_index = keep_index + 1

    NK_values = np.sqrt(wK_values * zK_values)
    tauK_values = np.sqrt(wK_values / zK_values)
    return NK_values, d_values, mu_values, sigma_values, tauK_values, iterations, burnin


if __name__ == "__main__":
    data = {}
    data["known"] = np.array([31000, 11000, 21000, 5300, 38000, 33000])
    data["unknown"] = np.array([1400000])
    data["N"] = np.array([46000000])
    y, d = simulate_trans(data, 100)
    print(y)
    print(mcmc_trans(y, data, 100, 50)[0])
