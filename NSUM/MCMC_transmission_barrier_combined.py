import numpy as np
import scipy as sp
import killworth as kw
def simulate_comb(data_dict, n, mu = 5, sigma =1):
    if "mu" in data_dict:
        if len(data_dict["mu"]) > 0:
            mu = data_dict["mu"][0]
    if "sigma" in data_dict:
        if len(data_dict["sigma"]) > 0:
            sigma = data_dict["sigma"][0]

    known_all = np.concatenate((data_dict['known'], data_dict['unknown']))
    known_all_len = len(known_all)

    if len(data_dict["rho"]) > 0:
        rho = data_dict["rho"]
    else:
        rho = np.repeat(0.1, known_all_len)

    tauK = np.repeat(1, len(data_dict["unknown"]))

    N = data_dict["N"]
    d = np.random.lognormal(mu,sigma, n)

    proportions = np.empty((n, known_all_len))

    for i in range(known_all_len):
        a = (known_all[i] / N) * (1 / rho[i] - 1)
        b = (1 - known_all[i] / N) * (1 / rho[i] - 1)

        proportions[:, i] = np.random.beta(a, b, n)

    tau = np.concatenate((np.repeat(1, len(data_dict["known"])), tauK))
    y = np.empty((n, known_all_len))

    for i in range(n):
        di = d[i]
        for j in range(known_all_len):
            y[i, j] = np.random.binomial(di, tau[j]*proportions[i,j], 1)

    return y, d

def loglik_mK_comb(data, index_k, n, d, mK, rhoK, q):
    
    q_relevant = q[:, index_k]

    rhoK_term = 1 / rhoK - 1  
    
    mK_rhoK_term = mK * rhoK_term

    sum_qik = (mK_rhoK_term - 1) * sum(np.log(q_relevant))
    sum_minusqik = (rhoK_term - mK_rhoK_term - 1) * sum(np.log(1 - q_relevant))

    beta_term = sp.special.betaln(mK_rhoK_term, rhoK_term - mK_rhoK_term)

    loglik = sum_qik + sum_minusqik - n * beta_term - np.log(mK)

    return loglik

def loglik_rhok_comb(data, index_k, n, d, mk, rhok, q):
    q_relevant = q[:, index_k]

    rhok_term = 1 / rhok - 1
    mk_rhok_term = mk * rhok_term

    sum_qik = (mk_rhok_term - 1) * sum(np.log(q_relevant))
    sum_minusqik = (rhok_term - mk_rhok_term - 1) * sum(np.log(1 - q_relevant))
    beta_term = sp.special.betaln(mk_rhok_term, rhok_term - mk_rhok_term)

    loglik = sum_qik + sum_minusqik - n * beta_term
    
    return loglik

def loglik_qik_comb(data_mat, d, index_i, index_k, mk_all, tauk_all, rhok, qik):
    data_relevant = data_mat[index_i, index_k]
    d_relevant = d[index_i]
    mk_relevant = mk_all[index_k]
    rhok_relevant = rhok[index_k]
    tauk_relevant = tauk_all[index_k]

    rhok_term = 1 / rhok_relevant - 1
    mk_rhok_term = mk_relevant * rhok_term

    qik_term = (data_relevant + mk_rhok_term - 1) * np.log(qik)
    qik_tauk_term = (d_relevant - data_relevant) * np.log(1 - tauk_relevant * qik)
    qik_minus_term = (rhok_term - mk_rhok_term - 1) * np.log(1 - qik)

    loglik = qik_term + qik_tauk_term + qik_minus_term

    return loglik

def loglik_tauk_comb(data_mat, index_k, n, d, q, tauK, tauK_prior):
    aK = tauK_prior[0]
    bK = tauK_prior[1]

    q_relevant = q[:, index_k]
    data_relevant = data_mat[:, index_k]

    tauk_term = sum(data_relevant + aK - 1) * np.log(tauK)
    minus_tauk_qik_term = sum((d - data_relevant) * np.log(1 - tauK * q_relevant))
    minus_tauk_term = n * (bK - 1) * np.log(1 - tauK)

    loglik = tauk_term + minus_tauk_qik_term + minus_tauk_term

    return loglik

def loglik_di_comb(data_mat, mu, sigma, di, qik, tauk_all):
    sum_binom = sum(np.log(sp.special.binom(di, data_mat)))

    tau_qik_term = di * sum(np.log(1 - qik * tauk_all))

    loglik = -np.log(di) - (np.log(di) - mu)**2 / (2 * sigma**2) + sum_binom + tau_qik_term

    return loglik

def mcmc_comb(data_mat, data_dict, iterations, burnin, size = None, mu_prior = (0,8), sigma_prior = (0,4), rho_prior = (0,3), NK_tuning=None, d_tuning=None, rho_tuning = None, tauK_tuning = None, q_tuning = None ):
    NK_start, d_start, mu_start, sigma_start = kw.killworth_start(data_mat, data_dict)
    known = data_dict["known"]
    known_len = len(known)
    N = data_dict["N"]
    indices_k = range(known_len, data_mat.shape[1])

    tauK_start = np.repeat(0.5, len(indices_k))
    rho_start = np.repeat(0.1, data_mat.shape[1])
    q_start = np.resize(np.concatenate((known, NK_start)) / N, data_mat.shape[0]*data_mat.shape[1]).reshape((data_mat.shape[0], data_mat.shape[1]), order="F")
    np.concatenate((known,NK_start))/N

    if size is None:
        size = iterations
    if NK_tuning is None:
        NK_tuning = 0.25 * NK_start
    if d_tuning is None:
        d_tuning = 0.25 * d_start
    if rho_tuning is None:
        rho_tuning = 0.25 * rho_start
    if tauK_tuning is None:
        tauK_tuning = 0.25 * tauK_start
    if q_tuning is None:
        q_tuning = 0.25 * q_start

    n = data_mat.shape[0]
    num_known = data_mat.shape[1] - len(indices_k)
    mu_values = np.empty(size)
    sigma_values = np.empty(size)
    mK_values = np.empty((len(indices_k), size))
    d_values = np.empty((n, size))
    rho_values = np.empty((data_mat.shape[1], size))
    tauK_values = np.empty((len(indices_k), size))
    q_values = np.empty((size, n, data_mat.shape[1]))

    mknown = known / N
    mK_start = NK_start / N
    mK_tuning = NK_tuning / N

    tauK_priors = np.repeat((1,1), len(indices_k)).reshape((len(indices_k), 2))

    mK_curr = mK_start
    rho_curr = rho_start
    tauK_curr = tauK_start
    q_curr = q_start
    d_curr = d_start
    mu_curr = mu_start
    sigma_curr = sigma_start

    keep = np.round(np.linspace(burnin + 1, burnin + iterations, size))
    keep_index = 0

    for i in range(burnin + iterations):
        if i % 10 == 0:
            print("Now on iteration ", i, "\n")

        d = d_curr
        mK = mK_curr
        rho = rho_curr
        tauK = tauK_curr
        q = q_curr
        mu = mu_curr
        sigma = sigma_curr

        tauK_all = np.concatenate((np.repeat(1, num_known), tauK))

        for j in range(n):
            di_old = d[j]
            di_new = np.random.normal(di_old, d_tuning[j], 1)

            if di_new < max(data_mat[j, :]):
                d_curr[j] = di_old
            else:
                ratio = loglik_di_comb(data_mat[j,:], mu, sigma, di_new, q[j,:], tauK_all) - loglik_di_comb(data_mat[j,:], mu, sigma, di_old, q[j,:], tauK_all)
                if np.isnan(ratio):
                    print("I broke for di for j = ", j, " where di.new was ", di_new, "\n")
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
            while (mK_new >= 1 or mK_new <= max(data_mat[:, index_this_k]) / N):
                distance_moved = mK_new - mK_old
                if distance_moved > 0:
                    max_distance_to_move = 1 - mK_old
                    mK_new = 1 - (abs(distance_moved) - max_distance_to_move)
                else:
                    max_distance_to_move = mK_old - max(data_mat[:, index_this_k]) / N
                    mK_new = max(data_mat[:, index_this_k]) / N + (abs(distance_moved) - max_distance_to_move)

            ratio = loglik_mK_comb(data_mat, index_this_k, n, d, mK_new, rho[index_this_k], q) - loglik_mK_comb(data_mat, index_this_k, n, d, mK_old, rho[index_this_k], q)
            if np.isnan(ratio):
                print("I broke on mK where my K was ", index_this_k, " and my new.mK was ", mK_new, "\n")

            accept = min(0, ratio)

            logu = np.log(np.random.uniform(0, 1, 1))

            if logu < accept:
                mK_curr[j] = mK_new
            else:
                mK_curr[j] = mK_old

        mK = mK_curr

        mk_all = np.concatenate((mknown, mK))

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
            ratio = loglik_rhok_comb(data_mat, j, n, d, mk_all[j], rhok_new, q) - loglik_rhok_comb(data_mat, j, n, d, mk_all[j], rhok_old, q)

            if np.isnan(ratio):
                print("I broke on rhok where my k was ", j, " and my new.rhok was ", rhok_new, "\n")
            accept = min(0, ratio)

            logu = np.log(np.random.uniform(0, 1, 1))

            if logu < accept:
                rho_curr[j] = rhok_new
            else:
                rho_curr[j] = rhok_old

        rho = rho_curr

        for j in range(len(indices_k)):
            index_this_k = indices_k[j]
            tauK_old = tauK[j]
            tauK_new = np.random.normal(tauK_old, tauK_tuning[j], 1)
            while (tauK_new >= 1 or tauK_new <= 0):
                distance_moved = tauK_new - tauK_old
                if (distance_moved > 0):
                    max_distance_to_move = 1 - tauK_old
                    tauK_new = 1 - (abs(distance_moved) - max_distance_to_move)
                else:
                    max_distance_to_move = tauK_old
                    tauK_new = (abs(distance_moved) - max_distance_to_move)
            ratio = loglik_tauk_comb(data_mat, index_this_k, n, d, q, tauK_new, tauK_priors[j,]) - loglik_tauk_comb(data_mat, index_this_k, n, d, q, tauK_old, tauK_priors[j,])
            if np.isnan(ratio):
                print("I broke on tauK where my K was ", index_this_k, " and my new.tauK was ", tauK.new, "\n")
            accept = min(0, ratio)

            logu = np.log(np.random.uniform(0, 1, 1))

            if logu < accept:
                tauK_curr[j] = tauK_new
            else:
                tauK_curr[j] = tauK_old
        tauK = tauK_curr

        tauk_all = np.concatenate((np.repeat(1, num_known), tauK))

        for j in range(n):

            for k in range(data_mat.shape[1]):
                qik_old = q[j, k]
                qik_new = np.random.normal(qik_old, q_tuning[j, k], 1)
                while (qik_new >= 1 or qik_new <= 0):
                    distance_moved = qik_new - qik_old
                    if distance_moved > 0:
                        max_distance_to_move = 1 - qik_old
                        qik_new = 1 - (abs(distance_moved) - max_distance_to_move)
                    else:
                        max_distance_to_move = qik_old
                        qik_new = (abs(distance_moved) - max_distance_to_move)
                ratio = loglik_qik_comb(data_mat, d, j, k, mk_all, tauk_all, rho, qik_new) - loglik_qik_comb(data_mat, d, j, k, mk_all, tauk_all, rho, qik_old)
                if np.isnan(ratio):
                    print("I broke on qik for j ", j, " and k ", k, " where my new qik was ", qik_new, "\n")
                accept = min(0, ratio)

                logu = np.log(np.random.uniform(0, 1, 1))

                if logu < accept:
                    q_curr[j,k] = qik_new
                else:
                    q_curr[j,k] = qik_old

        q = q_curr

        mu_new = np.random.normal(sum(np.log(d)) / n, sigma / np.sqrt(n), 1)
        while (mu_new < mu_prior[0] or mu_new > mu_prior[1]):
            mu_new = np.random.normal(sum(np.log(d)) / n, sigma / np.sqrt(n), 1)

        mu_curr = mu_new
        mu = mu_curr

        sigma_new = 1 / np.sqrt(np.random.gamma((n - 1) / 2,  2 / sum((np.log(d) - mu) ** 2), 1))
        while (sigma_new < sigma_prior[0] or sigma_new > sigma_prior[1]):
            sigma_new = 1 / np.sqrt(np.random.gamma((n - 1) / 2, 2 / sum((np.log(d) - mu) ** 2), 1))
        sigma_curr = sigma_new

        if i == keep[keep_index]-1:
            mu_values[keep_index] = mu_curr
            sigma_values[keep_index] = sigma_curr
            mK_values[:, keep_index] = mK_curr
            d_values[:, keep_index] = d_curr
            rho_values[:, keep_index] = rho_curr
            tauK_values[:, keep_index] = tauK_curr
            q_values[keep_index,:, :] = q_curr
            keep_index = keep_index + 1
    NK_values = N * mK_values

    return NK_values, d_values, mu_values, sigma_values, rho_values, tauK_values, q_values, iterations, burnin



if __name__ == "__main__":
    data = {}
    with open('/Users/tomas/Downloads/McCarty.txt') as f:
        for line in f:
            y = line.split()
            if len(y) > 0:
                data[y[0]] = np.array([float(i) for i in y[1:]])
    y, d = simulate_comb(data, 100)
    print(mcmc_comb(y, data, 100,50)[0])
    print(np.mean(mcmc_comb(y, data, 100,50)[0]))