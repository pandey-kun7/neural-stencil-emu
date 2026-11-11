import numpy as np
import matplotlib.pyplot as plt
import h5py
from matplotlib.colors import PowerNorm
import json
import random
from sklearn.decomposition import PCA
from scipy.stats import qmc

def is_valid(i , j , n , m):
    if (i >= 0 and i < n and j >= 0 and j < m ):
        return True
    return False

def down_sampled_diff_init():

    down_sampled_samples = []

    with open("./down_sampled.json.","r", encoding='utf-8') as f:
        down_sampled_samples = json.load(f)

    down_sampled_stencils = []
    for i in down_sampled_samples:
        down_sampled_stencils.append(i['stencil'])

    steps = 1
    r = 0.2
    timestep = 0

    json_data_list = []
    stencil_id = down_sampled_samples[-1]['stencil_id']+1

    while(timestep != steps):

        for l in down_sampled_samples:

            center = l['stencil'][0]
            stencil_dict = dict()
            stencil = []
            change = 0.0
            
            right = l['stencil'][1]
            change += (- center + right)
            
            left = l['stencil'][2]
            change += (- center + left) 
            
            down = l['stencil'][3]
            change += (- center + down) 
            
            up = l['stencil'][4]
            change += (- center + up) 

            target = center + r * change
            
            stencil.extend([center, right, left , down , up])
            stencil_id += 1

            stencil_dict['stencil_id'] = stencil_id
            stencil_dict['stencil'] = stencil
            stencil_dict['target'] = target

            json_data_list.append(stencil_dict)

        timestep += 1

    down_sampled_samples.extend(json_data_list)

    with open("./down_sampled_extend.json","a") as f:
        json.dump(down_sampled_samples, f, indent=4)

    lk = 0
    for i in down_sampled_samples:
        lk = max(lk,i['target'])

    print(lk)
if __name__ == "__main__":
    down_sampled_diff_init()