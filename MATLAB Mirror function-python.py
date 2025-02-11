#####################################################
#  PYTHON CONVERTED MATLAB FUNCTION (AS AN EXAMPLE) # 
#####################################################

import numpy as np
import pandas as pd

# Here Im loading an example data file (should be the bulk of errors)
data = pd.read_csv("your_file.csv")

key_var = data['key_var']
treatment = data['Treatment']


treat1 = 0
treat2 = 1
upper = 24

# Here Im just doing the counts for each treatment preemptivly 
N = (treatment == treat1).sum()
M = (treatment == treat2).sum()

G = np.zeros(upper)
F = np.zeros(upper)
GmF = np.zeros(upper)

# Im doing inital var(just part one)
for j in range(upper):
    counter = -0.3 + (j - 1) * 0.1
    F[j] = ((key_var <= counter) & (treatment == treat1)).sum() / N
    G[j] = ((key_var <= counter) & (treatment == treat2)).sum() / M
    GmF[j] = G[j] - F[j]

# Here S1 is computed based upon previous variables
S1 = np.sqrt(N * M / (N + M)) * np.max(GmF)


#End of the the preemptive cleaning/orgnaizing for making the bootstrap work properly

#(BM_bs equivalent) This is the bootstrap(also maybe a main source of error fixing)
def bootstrap(key_var, treatment, treat1, treat2, reps, upper):
    Sr = np.zeros(reps)
    for i in range(reps):
        # Sample with replacement
        resample = data.sample(frac=1, replace=True)
        key_var_res = resample['key_var']
        treatment_res = resample['Treatment']

        G_boot = np.zeros(upper)
        F_boot = np.zeros(upper)
        GmF_boot = np.zeros(upper)
        
        for j in range(upper):
            counter = -0.3 + (j - 1) * 0.1
            F_boot[j] = ((key_var_res <= counter) & (treatment_res == treat1)).sum() / N
            G_boot[j] = ((key_var_res <= counter) & (treatment_res == treat2)).sum() / M
            GmF_boot[j] = G_boot[j] - F_boot[j]

        Sr[i] = np.sqrt(N * M / (N + M)) * np.max(GmF_boot)
    return Sr

#You guys know what this is (just running the function)
reps = 1000
Sr = bootstrap(key_var, treatment, treat1, treat2, reps, upper)

# p-value
p = (Sr > S1).sum() / reps
print("p-value:", p)4