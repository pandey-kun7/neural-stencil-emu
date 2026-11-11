import numpy as np
import matplotlib.pyplot as plt
import h5py
from matplotlib.colors import PowerNorm
import json
import random

def is_valid(i , j , n , m):
    if (i >= 0 and i < n and j >= 0 and j < m ):
        return True
    return False

def down_sampled_sobol():

    n = 32
    m = 32
    max_norm_temp = float(input("Enter the max temp across the grid: "))
    
    steps = 10
    r = 0.2     

    timestep = 0

    json_data_list = []
    stencil_id = 0

    while(timestep != steps):
        
        for i in range (n-1):
            for j in range (m-1):

                l = np.array( [ random.uniform(0, max_norm_temp) for i in range (5) ] )
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

    with open("./down_sampled_sobol.json","a") as sobol_file:
        json.dump(json_data_list, sobol_file, indent=4)

    lk = 0
    for i in json_data_list:
        lk = max(lk,i['target'])

    print(lk)
if __name__ == "__main__":
    down_sampled_sobol()