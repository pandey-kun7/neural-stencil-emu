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

def heat_diffusion():

    n , m = map(int,input("Enter grid (rows cols): ").split())
    max_norm_temp = float(input("Enter the max variable temp across the grid: "))
    l = np.array([ [ random.uniform(0,max_norm_temp) for i in range (m) ] for i in range (n) ])
    k = int(input("Enter no. of hotspots : "))
    i = 0
    steps = int(input("Enter number of time steps: "))
    r = float(input("Enter diffusion coefficient: "))        

    global t_max ;

    t_max = 0

    while i!=k :
        x , y = map(int, input("Enter hotspot coordinates: ").split())
        if(is_valid(x,y,n,m) == False):
           print("Invalid coordinates. Enter valid combination.\n")
           continue
        temp = float(input(f"Enter temperature of hotspot at {x} - {y} coord. : "))
        l[x][y] += temp
        t_max = max(t_max, l[x][y])
        i += 1
        
    timestep = 0

    fig , ax = plt.subplots()
    im = ax.imshow(l , cmap = "hot", interpolation = "nearest", norm = PowerNorm(gamma = 0.2 , vmin = 1 , vmax = t_max))
    fig.colorbar(im, ax=ax,label = "Temp.")
    plt.show(block = False)

    json_data_list = []

    stencil_id = 0


    while(timestep != steps):

        l_ = l.copy()
        
        for i in range (n-1):
            for j in range (m-1):

                stencil_dict = dict()
                
                stencil = []
                change = 0.0
                
                change += (- l[i][j] + l[i+1][j]) 
                right = l[i+1][j]

                change += (-l[i][j] + l[i-1][j]) 
                left = l[i-1][j]

                change += (-l[i][j] + l[i][j+1]) 
                down = l[i][j+1]
                
                change += (-l[i][j] + l[i][j-1])
                up = l[i][j-1]

                l_[i][j] = l[i][j] + r * change

                stencil.extend([l[i][j], right, left , down , up])
                target = l_[i][j]
                stencil_id += 1

                stencil_dict['stencil_id'] = stencil_id
                stencil_dict['stencil'] = stencil
                stencil_dict['target'] = target

                json_data_list.append(stencil_dict)

        l = l_

        # print(f"\nTime step {timestep + 1}:")
        # for row in l:
        #     print(["{:.2f}".format(x) for x in row])
            
        im.set_data(l)
        ax.set_title(f"Heat Diffusion - Time step {timestep + 1}:")
        fig.canvas.draw_idle()
        plt.pause(0.2)

        timestep += 1

    with open("./short_traj.json","a") as st_file:
        json.dump(json_data_list, st_file, indent=4)

    lk = 0
    for i in json_data_list:
        lk = max(lk,i['target'])

    print(lk)
if __name__ == "__main__":
    heat_diffusion()