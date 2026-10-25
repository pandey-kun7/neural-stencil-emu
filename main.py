import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import PowerNorm

def is_valid(i , j , n , m):
    if (i >= 0 and i < n and j >= 0 and j < m ):
        return True
    return False

def heat_diffusion():
    temp = float(input("Enter initial temperature: "))
    n , m = map(int,input("Enter grid (rows cols): ").split())
    steps = int(input("Enter number of time steps: "))
    r = float(input("Enter diffusion coefficient: "))

    l = np.array([ [ 0.0 for i in range (m) ] for i in range (n) ])
    print(l)
    l[n//2][m//2] = temp;

    timestep = 0

    fig , ax = plt.subplots()
    im = ax.imshow(l , cmap = "hot", interpolation = "nearest", norm = PowerNorm(gamma = 0.3 , vmin = 0 , vmax = temp))
    fig.colorbar(im, ax=ax,label = "Temp.")
    plt.show(block = False)

    while(timestep != steps):
        l_ = l.copy()
        for i in range (n):
            for j in range (m):
                change = 0.0
                if (is_valid(i+1,j,n,m)):
                    change += (- l[i][j] + l[i+1][j]) 

                if (is_valid(i-1,j,n,m)):
                    change += (-l[i][j] + l[i-1][j]) 

                if (is_valid(i,j+1,n,m)):
                    change += (-l[i][j] + l[i][j+1]) 
                
                if (is_valid(i,j-1, n, m)):
                    change += (-l[i][j] + l[i][j-1]) 

                l_[i][j] = l[i][j] + r * change
        l = l_

        print(f"\nTime step {timestep + 1}:")
        for row in l:
            print(["{:.2f}".format(x) for x in row])
            # for l_ in l:
            #     print(l_)
            # print("\n")
        im.set_data(l)
        ax.set_title(f"Heat Diffusion - Time step {timestep + 1}:")
        fig.canvas.draw_idle()
        plt.pause(0.2)
                
        # if(no_temp == 1):
        timestep += 1
        # print("\n")

if __name__ == "__main__":
    heat_diffusion()