import pandas
import pandas as pd
import numpy as np
import scipy as sp
import MCMC_random_degree as rd
import MCMC_barrier_effect as be
import MCMC_transmission_bias as tb
import MCMC_transmission_barrier_combined as tbc
import matplotlib.pyplot as plt


if __name__ == "__main__":
    print(np.round(np.linspace(51, 50 + 100, 100)))

    """data = {}
    df = pd.read_csv("/Users/tomas/Downloads/aids.csv")
    data["known"] = np.array(*df[(df["Country"]=="Uganda") & (df["Year"] == 2020)].iloc[:,19:].values)
    data["unknown"] = np.array(*df[(df["Country"]=="Uganda") & (df["Year"] == 2020)].iloc[:,18:19].values)
    data["N"] = np.array([46000000])
    y, d = tb.simulate_trans(data, 100)
    print(tb.mcmc_trans(y, data, 100, 50)[0])"""




