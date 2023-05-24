import numpy as np
import scipy as sp
import killworth as kw


def simulate_rd(data_dict, n, mu = 5, sigma = 1):
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

    p_pops = known_all / N

    y = np.empty((n, known_all_len))

    for i in range(n):
        di = d[i]
        for j in range(known_all_len):
            y[i, j] = np.random.binomial(di, p_pops[j], 1)

    return y, d


def loglik_NK_rd(data_mat, indices_k, N, d, NK):
    sum_di = sum(d)

    sum_yik = sum(data_mat[:, indices_k])

    loglik = sum_yik * np.log(NK / (N - NK)) + sum_di * np.log(1 - NK / N) - np.log(NK)

    return loglik


def loglik_di_rd(data_mat, mu, sigma, di, N, known, NK):
    sum_binom = sum(np.log(sp.special.binom(di, data_mat)))

    sum_log_nk = sum(np.log(1 - known / N)) + sum(np.log(1 - NK / N))

    loglik = -np.log(di) - ((np.log(di) - mu) ** 2) / (2 * sigma ** 2) + sum_binom + di * sum_log_nk

    return loglik


def mcmc_rd(data_mat, data_dict, iterations, burnin, size=None, mu_prior=(3, 8), sigma_prior=(0, 2), NK_tuning=None, d_tuning=None):

    known = data_dict["known"]
    known_len = len(known)
    N = data_dict["N"]
    n = data_mat.shape[0]

    indices_k = range(known_len, data_mat.shape[1])

    if size is None:
        size = iterations

    NK_start, d_start, mu_start, sigma_start = kw.killworth_start(data_mat, data_dict)

    if NK_tuning is None:
        NK_tuning = 0.25 * NK_start

    if d_tuning is None:
        d_tuning = 0.25 * d_start

    mu_values = np.empty(size)
    sigma_values = np.empty(size)
    NK_values = np.empty((len(indices_k), size))
    d_values = np.empty((data_mat.shape[0], size))

    NK_curr = NK_start
    d_curr = d_start
    mu_curr = mu_start
    sigma_curr = sigma_start
    keep = np.round(np.linspace(burnin + 1, burnin + iterations, size))
    keep_index = 1

    for i in range(burnin + iterations):
        if i % 10 == 0:
            print("Now on iteration ", i, "\n")

        d = d_curr
        NK = NK_curr
        mu = mu_curr
        sigma = sigma_curr

        for j in range(n):
            di_old = d[j]
            di_new = np.random.normal(di_old, d_tuning[j], 1)

            if di_new < max(data_mat[j, :]):
                d_curr[j] = di_old
            else:
                ratio = loglik_di_rd(data_mat[j, :], mu, sigma, di_new, N, known, NK) - loglik_di_rd(data_mat[j, :], mu,
                                                                                                     sigma, di_old, N,
                                                                                                     known, NK)
                if np.isnan(ratio):
                    print("I broke for di for i = ", j, " where di_new was ", di_new, "\n")

                accept = min(0, ratio)
                logu = np.log(np.random.uniform(0, 1, 1))
                if logu < accept:
                    d_curr[j] = di_new
                else:
                    d_curr[j] = di_old

        d = d_curr

        for j in range(len(indices_k)):

            index_this_k = indices_k[j]
            NK_old = NK[j]
            NK_new = np.random.normal(NK_old, NK_tuning[j], 1)

            if (NK_new >= N or NK_new <= max(data_mat[:, index_this_k])):
                NK_curr[j] = NK_old
            else:
                ratio = loglik_NK_rd(data_mat, index_this_k, N, d, NK_new) - loglik_NK_rd(data_mat, index_this_k, N, d,
                                                                                          NK_old)
                accept = min(0, ratio)
                logu = np.random.uniform(0, 1, 1)

                if logu < accept:
                    NK_curr[j] = NK_new
                else:
                    NK_curr[j] = NK_old
        NK = NK_curr

        mu_new = np.random.normal(sum(np.log(d)) / n, sigma / np.sqrt(n), 1)

        while (mu_new < mu_prior[0] or mu_new > mu_prior[1]):
            mu_new = np.random.normal(sum(np.log(d)) / n, sigma / np.sqrt(n), 1)

        mu_curr = mu_new
        mu = mu_curr

        sigma_new = 1/np.sqrt(np.random.gamma((n - 1)/2, 1/2*sum((np.log(d)-mu)**2), 1))
        while (sigma_new < sigma_prior[0] or sigma_new > sigma_prior[1]):
            sigma_new = 1/np.sqrt(np.random.gamma((n - 1)/2, 1/2*sum((np.log(d)-mu)**2), 1))
        sigma_curr = sigma_new
        if i == keep[keep_index]:
            mu_values[keep_index] = mu_curr
            sigma_values[keep_index] = sigma_curr
            NK_values[:, keep_index] = NK_curr
            d_values[:, keep_index] = d_curr
            keep_index = keep_index + 1

    return NK_values, d_values, mu_values, sigma_values, iterations, burnin


if __name__ == "__main__":
    data = {}
    with open('/Users/tomas/Downloads/McCarty.txt') as f:
        for line in f:
            y = line.split()
            if len(y) > 0:
                data[y[0]] = np.array([float(i) for i in y[1:]])
    y, d = simulate_rd(data, 10)
    print(mcmc_rd(y, data, 10, 5))
