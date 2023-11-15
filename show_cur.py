import matplotlib.pyplot as plt
import matplotlib
import numpy as np

def show_cur(cur_, idx=''):
    cmap = matplotlib.colors.ListedColormap(
    ['#000000', '#0074D9','#FF4136','#2ECC40','#FFDC00',
     '#AAAAAA', '#F012BE', '#FF851B', '#7FDBFF', '#870C25'])
    cur = cur_['train']
    fig, ax = plt.subplots(2,len(cur) + 1)
    fig.suptitle(f'{idx}')
    for j in range(len(cur)):
        ax[0,j].imshow(cur[j]['input'], cmap=cmap, vmin=0, vmax=9)
        ax[1,j].imshow(cur[j]['output'], cmap=cmap, vmin=0, vmax=9)
        ax[0,j].axis('off')
        ax[1,j].axis('off')
        ax[0,j].set_title(f'{np.array(cur[j]["input"]).shape}', fontsize=5)
        ax[1,j].set_title(f'{np.array(cur[j]["output"]).shape}', fontsize=5)
    ax[0,-1].imshow(cur_['test'][0]['input'], cmap=cmap, vmin=0, vmax=9)
    ax[1,-1].imshow(cur_['test'][0]['output'], cmap=cmap, vmin=0, vmax=9)
    ax[0,-1].set_title(f'{np.array(cur_["test"][0]["input"]).shape}', fontsize=5)
    ax[1,-1].set_title(f'{np.array(cur_["test"][0]["output"]).shape}', fontsize=5)
    ax[0,-1].axis('off')
    ax[1,-1].axis('off')