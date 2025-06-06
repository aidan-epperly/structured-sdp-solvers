import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import json
# matplotlib.use('Qt5Agg') #IGNORE DEPENDING ON YOUR SET UP

sns.set_theme(style = "whitegrid")

# # import data
# # I WAS PLANNING ON AUTOREPLACING SPACES WITH COMMAS AND SUCH LATER
# # DO AS YOU WILL
# n = 10
# d = 5
# dvalues = range(n)
# rs = np.random.default_rng()

# vals_scgal = rs.random((n, d)) #JUST TAKE THE TRANSPOSE IF THE ACTUAL DIMENSIONS DONT ALIGN THIS WAY
# vals_lp = rs.random((n, d))
# vals_lmi = rs.random((n, d))
# times_scgal = rs.random((n, d))
# times_lp = rs.random((n, d))
# times_lmi = rs.random((n, d))
# Updated code concatenate data

# Import Data
start_idx = [1, 6, 11, 16, 21]
end_idx = [5, 10, 15, 20, 25]

for i in range(len(start_idx)):
    file_name = 'ds' + str(start_idx[i]) + 'to' + str(end_idx[i]) + '.json'

    with open(file_name, 'r') as f:
        loaded_dict = json.load(f)

    if i == 0:
        ds_loaded = np.array(loaded_dict['ds'])
        circ_emb_obj_loaded = np.array(loaded_dict['circ_emb_obj'])
        circ_emb_time_loaded = np.array(loaded_dict['circ_emb_time'])
        LMI_obj_loaded = np.array(loaded_dict['LMI_obj'])
        LMI_time_loaded = np.array(loaded_dict['LMI_time'])
        SCGAL_obj_loaded = np.array(loaded_dict['SCGAL_obj'])
        SCGAL_time_loaded = np.array(loaded_dict['SCGAL_time'])
    else:
        ds_loaded = np.concatenate((ds_loaded, np.array(loaded_dict['ds'])), axis=0)
        circ_emb_obj_loaded = np.concatenate((circ_emb_obj_loaded, np.array(loaded_dict['circ_emb_obj'])), axis=1)
        circ_emb_time_loaded = np.concatenate((circ_emb_time_loaded, np.array(loaded_dict['circ_emb_time'])), axis=1)
        LMI_obj_loaded = np.concatenate((LMI_obj_loaded, np.array(loaded_dict['LMI_obj'])), axis=1)
        LMI_time_loaded = np.concatenate((LMI_time_loaded, np.array(loaded_dict['LMI_time'])), axis=1)
        SCGAL_obj_loaded = np.concatenate((SCGAL_obj_loaded, np.array(loaded_dict['SCGAL_obj'])), axis=1)
        SCGAL_time_loaded = np.concatenate((SCGAL_time_loaded, np.array(loaded_dict['SCGAL_time'])), axis=1)


final_index = 21
dvalues = ds_loaded[:final_index]
vals_lp = circ_emb_obj_loaded[:, :final_index]
times_lp = circ_emb_time_loaded[:, :final_index]
vals_lmi = LMI_obj_loaded[:, :final_index]
times_lmi = LMI_time_loaded[:, :final_index]
vals_scgal = SCGAL_obj_loaded[:, :final_index]
times_scgal = SCGAL_time_loaded[:, :final_index]

print(vals_scgal)

# averaging and relative error
errors_lp = np.abs(vals_lp - vals_lmi) / np.abs(vals_lmi)
errors_scgal = np.abs(vals_scgal - vals_lmi) / np.abs(vals_lmi)

errors_lp = np.mean(errors_lp, axis=0, where=((vals_lp!=0)&(vals_lmi!=0)))
errors_scgal = np.mean(errors_scgal, axis=0, where=((vals_scgal!=0)&(vals_lmi!=0)))

A = np.array([vals_scgal, vals_lp])
differences = abs(vals_scgal - vals_lp) / np.max(A, axis=0)

times_scgal = np.mean(times_scgal, axis=0, where=times_scgal>0)
times_lp = np.mean(times_lp, axis=0, where=times_lp>0)
times_lmi = np.mean(times_lmi, axis=0, where=times_lmi>0)

# differences = np.mean(differences, axis=0)

# format data
time_array = np.column_stack((times_lp, times_scgal, times_lmi))
error_array = np.column_stack((errors_lp, errors_scgal))

time_data = pd.DataFrame(time_array, dvalues, columns=["LP", "SCGAL", "LMI"])
error_data = pd.DataFrame(error_array, dvalues, columns=["LP", "SCGAL"])
# difference_data = pd.DataFrame(differences, dvalues)

# plot
#plt.plot(dvalues, times_lmi)
sns.set_theme(palette="Set2")
plt.figure(1)
sns.lineplot(data=time_data, linewidth=2.5)
plt.yscale('log')
plt.xlabel("d")
plt.ylabel("time (s)")
plt.title("Log Average Runtime")


plt.figure(2)
sns.lineplot(data=error_data, linewidth=2.5)
plt.yscale('log')
plt.xlabel("d")
plt.ylabel("error")
plt.title("Log Average Relative Error Comparison")

# plt.figure(3)
# sns.lineplot(data=difference_data, linewidth=2.5)
# plt.xlabel("d")
# plt.ylabel("error")
# plt.title("Scaled Difference Between LP and SCGAL")

plt.show()
