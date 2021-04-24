import pylab as plt
import numpy as np
import matplotlib.patches as mpatches

from .constant_CA import *

def printMatrix_CA(mat, cmap, labels, model, day):
    arrayShow = np.array([[cmap[i] for i in j] for j in mat])
    patches = [mpatches.Patch(color=cmap[i], label=labels[i])
                for i in cmap]
    plt.imshow(arrayShow)
    plt.legend(handles=patches, title="Status",
                loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    ax = plt.gca()
    ax.set_xticks(np.arange(-.5, len(mat), 1))
    ax.set_yticks(np.arange(-.5, len(mat), 1))
    ax.xaxis.set_ticklabels([])
    ax.yaxis.set_ticklabels([])
    plt.grid(which="major",color='k', ls="-",lw=(200/(len(mat)**2)))
    plt.title(f"{model}\n Day: {day}")
    
    
def printMatrix_multi_CA(mat_arr:list, model:str, day:list):
    fig, axes = plt.subplots(1, len(mat_arr), dpi=150, figsize=(10, 10))
    for i in range(len(mat_arr)):
        # index = i if (i==0) else int((int(day[i])/len(mat_arr)))*i
        mat = mat_arr[i]

        arrayShow = np.array([[cmaps[model][i] for i in j] for j in mat])
        patches = [mpatches.Patch(color=cmaps[model][i], label=labels[model][i])
                for i in cmaps[model]]
        axes[i].imshow(arrayShow)
        
        axes[i].set_title(f"{model}\n Day: {day[i] + 1}")
        axes[i].xaxis.set_ticklabels([])
        axes[i].yaxis.set_ticklabels([])

        if i == len(mat_arr) - 1:
            axes[i].legend(handles=patches, title="Status",
            loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))