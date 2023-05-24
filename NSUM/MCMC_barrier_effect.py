import scipy as sp
import numpy as np
import killworth as kw

def simulate_bar(data_dict, n, mu = 5, sigma = 1):
    if "mu" in data_dict:
        if len(data_dict["mu"]) > 0:
            mu = data_dict["mu"][0]
    if "sigma" in data_dict:
        if len(data_dict["sigma"]) > 0:
            sigma = data_dict["sigma"][0]


    known_all = np.concatenate((data_dict['known'], data_dict['unknown']))
    known_all_len = len(known_all)
    N = data_dict["N"]

    if len(data_dict["rho"]) > 0:
        rho = data_dict["rho"]
    else:
        rho = np.repeat(0.1, known_all_len)

    d = np.random.lognormal(mu, sigma, n)
    proportions = np.empty((n, known_all_len))

    for i in range(known_all_len):
        a = (known_all[i]/N) * (1/rho[i]-1)
        b = (1 - known_all[i] / N) * (1 / rho[i] - 1)

        proportions[:,i] = np.random.beta(a,b,n)

    y = np.empty((n, known_all_len))

    for i in range(n):
        di = d[i]
        for j in range(known_all_len):
            y[i, j] = np.random.binomial(di, proportions[i,j], 1)
    return y, d

def loglik_rhok_bar(data_mat, index, n, d, mk, rhok):

    sum_lbeta1 = sum(sp.special.betaln(mk*(1/rhok - 1) + data_mat[:,index], d + (1-mk)*(1/rhok - 1) - data_mat[:,index]))
    
    sum_lbeta2 = n * sp.special.betaln(mk * (1 / rhok - 1), (1 - mk) * (1 / rhok - 1))

    loglik = sum_lbeta1 - sum_lbeta2

    return loglik

def loglik_mK_bar(data_mat, index_k, n, d, mK, rhoK):
    sum_lbeta1 = sum(sp.special.betaln(mK * (1 / rhoK - 1) + data_mat[:,index_k], d + (1 - mK) * (1 / rhoK - 1) - data_mat[:,index_k]))

    sum_lbeta2 = n * sp.special.betaln(mK * (1 / rhoK - 1), (1 - mK) * (1 / rhoK - 1))

    loglik = sum_lbeta1 - sum_lbeta2 - np.log(mK)
    
    return loglik

def loglik_di_bar(data_mat, mu, sigma, di, mknown, mK, rho):

    m_all = np.concatenate((mknown, mK))

    sum_binom = sum(np.log(sp.special.binom(di, data_mat)))

    sum_lgamma1 = sum(sp.special.gammaln(di + (1 - m_all) * (1 / rho - 1) - data_mat))

    sum_lgamma2 = sum(sp.special.gammaln(di + (1 / rho - 1)))

    loglik = -np.log(di) - (np.log(di) - mu)** 2 / (2 * sigma **2) + sum_binom + sum_lgamma1 - sum_lgamma2

    return loglik

def mcmc_bar(data_mat, data_dict, iterations, burnin, size=None, mu_prior=(2,8), sigma_prior= (0,2), rho_prior=(0,1), NK_tuning=None, d_tuning=None, rho_tuning = None):

    NK_start, d_start, mu_start, sigma_start = kw.killworth_start(data_mat, data_dict)
    rho_start = np.repeat(0.1, data_mat.shape[1])

    known = data_dict["known"]
    known_len = len(known)
    N = data_dict["N"]
    indices_k = range(known_len, data_mat.shape[1])
    if size is None:
        size = iterations

    if NK_tuning is None:
        NK_tuning = 0.25 * NK_start

    if d_tuning is None:
        d_tuning = 0.25 * d_start
    if rho_tuning is None:
        rho_tuning = 0.25*rho_start

    n = data_mat.shape[0]
    mknown = known / N
    mK_start = NK_start / N
    mK_tuning = NK_tuning / N

    mu_values = np.empty(size)
    sigma_values = np.empty(size)
    mK_values = np.empty((len(indices_k),size))
    d_values = np.empty((n, size))
    rho_values = np.empty((data_mat.shape[1],size))

    mK_curr = mK_start
    rho_curr = rho_start
    d_curr = d_start
    mu_curr = mu_start
    sigma_curr = sigma_start

    keep = np.round(np.linspace(burnin + 1, burnin + iterations, size))
    keep_index = 1

    for i in range(burnin + iterations):
        if i % 10 == 0:
            print("Now on iteration ", i, "\n")

        d = d_curr
        mK = mK_curr
        rho = rho_curr
        mu = mu_curr
        sigma = sigma_curr

        for j in range(n):
            di_old = d[j]
            di_new = np.random.normal(di_old, d_tuning[j], 1)

            if di_new < max(data_mat[j, :]):
                d_curr[j] = di_old
            else:
                ratio = loglik_di_bar(data_mat[j, :], mu, sigma, di_new, mknown, mK, rho) - loglik_di_bar(data_mat[j, :], mu, sigma, di_old, mknown, mK, rho)

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
            mK_old = mK[j]
            mK_new = np.random.normal(mK_old, mK_tuning[j], 1)
            while (mK_new >= 1 or mK_new <= max(data_mat[:,index_this_k]) / N):
                distance_moved = mK_new - mK_old
                if distance_moved > 0:
                    max_distance_to_move = 1 - mK_old
                    mK_new = 1 - (abs(distance_moved) - max_distance_to_move)
                else:
                    max_distance_to_move = mK_old - max(data_mat[:, index_this_k]) / N
                    mK_new = max(data_mat[:, index_this_k]) / N + (abs(distance_moved) - max_distance_to_move)

            ratio = loglik_mK_bar(data_mat, index_this_k, n, d, mK_new, rho[index_this_k]) - loglik_mK_bar(data_mat, index_this_k, n, d, mK_old, rho[index_this_k])
            if np.isnan(ratio):
                print("I broke on mK where my K was ", index_this_k, " and my new.mK was ", mK_new, "\n")

            accept = min(0, ratio)

            logu = np.random.uniform(0, 1, 1)

            if logu < accept:
                mK_curr[j] = mK_new
            else:
                mK_curr[j] = mK_old

        mK = mK_curr

        for j in range(data_mat.shape[1]):
            rhok_old = rho[j]
            rhok_new = np.random.normal(rhok_old, rho_tuning[j], 1)
            while (rhok_new >= rho_prior[1] or rhok_new <= rho_prior[0]):
                distance_moved = rhok_new - rhok_old
                if distance_moved > 0:
                    max_distance_to_move = rho_prior[1] - rhok_old
                    rhok_new = rho_prior[1] - (distance_moved - max_distance_to_move)
                else:
                    max_distance_to_move = rhok_old - rho_prior[0]
                    rhok_new = rho_prior[0] + (abs(distance_moved) - max_distance_to_move)

            mk_all = np.concatenate((mknown, mK))

            ratio = loglik_rhok_bar(data_mat,j, n, d, mk_all[j], rhok_new) - loglik_rhok_bar(data_mat,j, n, d, mk_all[j], rhok_old)

            if np.isnan(ratio):
                print("I broke on rhok where my k was ", j, " and my new.rhok was ", rhok_new, "\n")
            accept = min(0, ratio)

            logu = np.random.uniform(0, 1, 1)

            if logu < accept:
                rho_curr[j] = rhok_new
            else:
                rho_curr[j] = rhok_old

        rho = rho_curr

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
            mK_values[:, keep_index] = mK_curr
            rho_values[:, keep_index] = rho_curr
            d_values[:, keep_index] = d_curr
            mu_values[keep_index] = mu_curr
            sigma_values[keep_index] = sigma_curr
            keep_index = keep_index + 1

    NK_values = N * mK_values

    return NK_values, d_values, mu_values, sigma_values, rho_values, iterations, burnin


if __name__ == "__main__":
    data = {}
    with open('/Users/tomas/Downloads/McCarty.txt') as f:
        for line in f:
            y = line.split()
            if len(y) > 0:
                data[y[0]] = np.array([float(i) for i in y[1:]])
    y, d = simulate_bar(data, 50)
    print(mcmc_bar(y, data, 50, 10))
