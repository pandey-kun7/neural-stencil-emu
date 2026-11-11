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

def pca_sampling():

    short_traj_samples = []

    with open("./short_traj.json","r", encoding='utf-8') as f:
        short_traj_samples = json.load(f)

    short_traj_stencils = []
    for i in short_traj_samples:
        short_traj_stencils.append(i['stencil'])

    steps = 1
    r = 0.2
    timestep = 0

    json_data_list = []
    stencil_id = 0

    while(timestep != steps):
        
        X = np.asarray(short_traj_stencils, dtype = np.float16)
        pca = PCA(n_components = 5)
        Z = pca.fit_transform(X)

        lower = 0
        upper = Z.max(axis = 0)
        
        sampler = qmc.Sobol(d=5, scramble = True)
        points = sampler.random(n=len(short_traj_stencils))
        
        Z_new = qmc.scale(points, lower, upper)
        X_new = pca.inverse_transform(Z_new)
        
        for l in X_new:

            center = l[0]
            stencil_dict = dict()
            stencil = []
            change = 0.0
            
            right = l[1]
            change += (- center + right)
            
            left = l[2]
            change += (- center + left) 
            
            down = l[3]
            change += (- center + down) 
            
            up = l[4]
            change += (- center + up) 

            target = center + r * change
            
            stencil.extend([center, right, left , down , up])
            stencil_id += 1

            stencil_dict['stencil_id'] = stencil_id
            stencil_dict['stencil'] = stencil
            stencil_dict['target'] = target

            json_data_list.append(stencil_dict)

        timestep += 1

    with open("./pca_sampling.json","a") as f:
        json.dump(json_data_list, f, indent=4)

    lk = 0
    for i in json_data_list:
        lk = max(lk,i['target'])

    print(lk)
if __name__ == "__main__":
    pca_sampling()