import pylab as plt
import numpy as np
import matplotlib.patches as mpatches

from .constant_ABM import *
# from ipywidgets import interact, IntSlider, FloatSlider
# from matplotlib.pyplot import rcParams, figure, subplot, show
# from matplotlib.pyplot import plot, quiver, streamplot, axhline, axvline, scatter
# from matplotlib.pyplot import xlabel, ylabel, title, grid, axis
# from numpy import array, zeros, diff, linspace, diag, meshgrid, real, imag, exp

# %matplotlib inline

def plotCurves_main(mo_list:list, line:str = '-', marker='.'):
    num_models = len(mo_list)
    # rows = num_models//num_cols + 1 if num_models < num_cols else num_models//num_cols
    # cols = num_cols
    # , sharex=True, sharey=True
    fig, axes = plt.subplots(num_models, dpi=150, figsize=(10, 10))
    label_list = [key for key in mo_list[0][1].keys()][:5]
    standard_model_added = False
    zombie_model_added = False
    lines, labels = [], []
    
    for i in range(num_models):
        ax = axes[i]
        mo = mo_list[i]
    
        ax.plot(mo[1]["Days"], mo[1]["Susceptible"], line, label=label_list[0], marker=marker, color="b")
        ax.plot(mo[1]["Days"], mo[1]["Exposed"], line, label=label_list[1], marker=marker, color=(1.0, 0.7, 0.0))
        ax.plot(mo[1]["Days"], mo[1]["Infected"], line, label=label_list[2], marker=marker, color="r")
        ax.plot(mo[1]["Days"], mo[1]["Recovered"], line, label=label_list[3], marker=marker, color=(0.0, 1.0, 0.0))
        if "Zombies" in mo[1].keys():
            ax.set_title(f"SEIRZ: {mo[0]}")
            ax.plot(mo[1]["Days"], mo[1]["Dead"], line, label=label_list[4], marker=marker, color=(0.5, 0, 0.5, 1), alpha=0)
            label_list = ["Susceptible", "Exposed", "Infected", "Recovered", "Dead", "Zombies"]
            ax.plot(mo[1]["Days"], mo[1]["Zombies"], line, label=label_list[5], marker=marker, color=(0, 0, 0, 1))
            if not zombie_model_added:
                lines_z, labels_z = ax.get_legend_handles_labels()
                zombie_model_added = True
                if not standard_model_added:
                    lines = lines_z[:4] + [lines_z[5]]
                    labels = labels_z[:4] + [labels_z[5]]
                else:
                    lines = lines + [lines_z[5]]
                    labels = labels + [labels_z[5]]
        else:
            ax.plot(mo[1]["Days"], mo[1]["Dead"], line, label=label_list[4], marker=marker, color=(0.5, 0, 0.5, 1))
            ax.set_title(f"SEIRD: {mo[0]}")
            if not standard_model_added:
                standard_model_added = True
                lines_s, labels_s = ax.get_legend_handles_labels()
                if not zombie_model_added:
                    lines, labels = lines_s, labels_s
                else:
                    lines = lines[:4] + [lines_s[4]] + [lines[4]]
                    labels = labels[:4] + [labels_s[4]] + [labels[4]]
            
        if (i == num_models - 1):
            fig.legend(lines, labels, loc="upper right")
    
    for ax in axes.flat:
        ax.set(xlabel='Days', ylabel='Number of People')
        ax.label_outer()
    
    plt.subplots_adjust(hspace=0.2)
    plt.tight_layout()
    plt.show()

"""
ABM constant parameter adjustment

INIT_INFECTED=0.005, INFECTION_RATE=0.5, EXPOSED_RATE=0.16, RECOVERY_RATE=0.1, \
    SUSCEPTIBLE_RATE=0.1, DEATH_RATE=0.02, WEAR_MASK=0.5, WEAR_MASK_POPULATION=0.5, \
        VACCINATED=0.1, VACCINATED_POPULATION=0.5, HOSPITALIZED=0.5
"""

# def printMatrix(model_output, days, size:tuple=(100,100), num_plots:int=4, model="SEIRD"):
#         mat_list = model_output[1]["People_States"]
#         fig, axes = plt.subplots(num_plots, dpi=150, figsize=(10, 10))
#         for i in range(num_plots):
#             index = i if i==0 else int((days/num_plots))*i-1
#             mat = mat_list[index]
#             print(mat)

#             arrayShow = np.array([[cmaps[model][i] for i in j] for j in mat])
#             patches = [mpatches.Patch(color=cmaps[model][i], label=labels[model][i])
#                     for i in cmaps[model]]
#             axes[i].imshow(arrayShow)
#             axes[i].legend(handles=patches, title="Status",
#                     loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
#             axes[i] = plt.gca()
#             axes[i].set_xticks(np.arange(-.5, size[0], 1))
#             axes[i].set_yticks(np.arange(-.5, size[1], 1))
#             axes[i].xaxis.set_ticklabels([])
#             axes[i].yaxis.set_ticklabels([])
#             axes[i].grid(which="major",color='k', ls="-",lw=(200/(size[0] * size[1])))
#             axes[i].title(f"Covid-19 Spread Situation - {model}\n Day: {index}")
#         plt.show()

# def run(a=0, b=1, c=-1, d=0, x0_0=1, x0_1=0, n_max=8):
#     A = array([[a, b], [c, d]])
#     x0 = array([x0_0, x0_1])
#     X, DX = sim(A, x0, n_max=n_max)
    
#     figure(figsize=(16, 9))
#     subplot(1, 2, 1)
#     plot_sim(X, DX, A, verbose=False)
#     axis('equal')
#     subplot(1, 2, 2)
#     axis('equal')
#     plot_vecfield(A)
#     show()
    
#     Lambda, V = eig(A)
#     display_eig(Lambda, V, A=A)    
    
# interact(run,
#          a=FloatSlider(value= 0, min=-1, max=1, step=0.25, continuous_update=False),
#          b=FloatSlider(value= 1, min=-1, max=1, step=0.25, continuous_update=False),
#          c=FloatSlider(value=-1, min=-1, max=1, step=0.25, continuous_update=False),
#          d=FloatSlider(value= 0, min=-1, max=1, step=0.25, continuous_update=False),
#          x0_0=FloatSlider(value=1, min=-1, max=1, step=0.25, continuous_update=False),
#          x0_1=FloatSlider(value=0, min=-1, max=1, step=0.25, continuous_update=False),
#          n_max=IntSlider(value=20, min=1, max=100, step=1, continuous_update=False)
#         )