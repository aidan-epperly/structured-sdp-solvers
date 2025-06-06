import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
matplotlib.use('Qt5Agg') #IGNORE DEPENDING ON YOUR SET UP

sns.set_theme(style = "whitegrid")

# import data
# I WAS PLANNING ON AUTOREPLACING SPACES WITH COMMAS AND SUCH LATER
# DO AS YOU WILL
n = 10
d = 5
dvalues = range(n)
rs = np.random.default_rng()

vals_scgal = rs.random((n, d)) #JUST TAKE THE TRANSPOSE IF THE ACTUAL DIMENSIONS DONT ALIGN THIS WAY
vals_lp = rs.random((n, d))
vals_lmi = rs.random((n, d))
times_scgal = rs.random((n, d))
times_lp = rs.random((n, d))
times_lmi = rs.random((n, d))

# averaging and relative error
errors_lp = np.abs(vals_lp - vals_lmi) / vals_lmi
errors_scgal = np.abs(vals_scgal - vals_lmi) / vals_lmi

errors_lp = np.mean(errors_lp, axis=1)
errors_scgal = np.mean(errors_scgal, axis=1)

A = np.array([vals_scgal, vals_lp])
differences = abs(vals_scgal - vals_lp) / np.max(A, axis=0)

times_scgal = np.mean(times_scgal, axis=1)
times_lp = np.mean(times_lp, axis=1)
times_lmi = np.mean(times_lmi, axis=1)

differences = np.mean(differences, axis=1)

# format data
time_array = np.column_stack((times_lp, times_scgal, times_lmi))
error_array = np.column_stack((errors_lp, errors_scgal))

time_data = pd.DataFrame(time_array, dvalues, columns=["LP", "SCGAL", "LMI"])
error_data = pd.DataFrame(error_array, dvalues, columns=["LP", "SCGAL"])
difference_data = pd.DataFrame(differences, dvalues)

# plot
#plt.plot(dvalues, times_lmi)
sns.set_theme(palette="Set2")
plt.figure(1)
sns.lineplot(data=time_data, linewidth=2.5)
plt.xlabel("d")
plt.ylabel("time (s)")
plt.title("Average Runtime")


plt.figure(2)
sns.lineplot(data=error_data, linewidth=2.5)
plt.xlabel("d")
plt.ylabel("error")
plt.title("Average Relative Error Comparison")

plt.figure(3)
sns.lineplot(data=difference_data, linewidth=2.5)
plt.xlabel("d")
plt.ylabel("error")
plt.title("Scaled Difference Between LP and SCGAL")

plt.show()
