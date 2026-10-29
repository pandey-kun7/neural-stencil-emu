import numpy as np
import matplotlib.pyplot as plt
import h5py
from matplotlib.colors import PowerNorm

def is_valid(i , j , n , m):
    if (i >= 0 and i < n and j >= 0 and j < m ):
        return True
    return False

def heat_diffusion():

    n , m = map(int,input("Enter grid (rows cols): ").split())
    l = np.array([ [ 0.0 for i in range (m) ] for i in range (n) ])
    k = int(input("Enter no. of hotspots : "))
    i = 0
    steps = int(input("Enter number of time steps: "))
    r = float(input("Enter diffusion coefficient: "))

    f = h5py.File('heat_diffusion.hdf5',"a")
    version = f.attrs.get('version', 0) + 1
    f.attrs['version'] = version
    simulation_data = f.create_group(f"simulation__{version}")
    metadata = simulation_data.create_group("metadata")
    temperatures =  simulation_data.create_dataset(
        "temp",
        shape = ( steps+1, n , m),
        dtype = "float32"
    )
    stencils = simulation_data.create_dataset(
        "stencils",
        shape = (0,9),
        maxshape=(None, 9),
        dtype="float32",
        chunks=True,
        compression="gzip"
    )
    

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


    metadata.attrs["rows"] = n
    metadata.attrs["cols"] = m
    metadata.attrs["time_steps"] = steps
    metadata.attrs["alpha"] = r

    # print(l)
    # l[n//2][m//2] = temp;
    # l[1][m//2] = temp;
    # l[n//2][1] = temp;

    timestep = 0

    fig , ax = plt.subplots()
    im = ax.imshow(l , cmap = "hot", interpolation = "nearest", norm = PowerNorm(gamma = 0.3 , vmin = 0 , vmax = t_max))
    fig.colorbar(im, ax=ax,label = "Temp.")
    plt.show(block = False)

    temperatures[0] = l

    while(timestep != steps):

        samples = []

        

        l_ = l.copy()
        


        for i in range (n-1):
            for j in range (m-1):
                sample = []
                sample.append(l[i][j])
                change = 0.0
                
                change += (- l[i][j] + l[i+1][j]) 
                right = l[i+1][j]
                sample.append(right)

                # if (is_valid(i-1,j,n,m)):
                change += (-l[i][j] + l[i-1][j]) 
                left = l[i-1][j]
                sample.append(left)

                # if (is_valid(i,j+1,n,m)):
                change += (-l[i][j] + l[i][j+1]) 
                down = l[i][j+1]
                sample.append(down)
                
                # if (is_valid(i,j-1, n, m)):
                change += (-l[i][j] + l[i][j-1])
                up = l[i][j-1]
                sample.append(up)

                l_[i][j] = l[i][j] + r * change

                sample.extend([l_[i][j], timestep, i, j])

                samples.append(sample)
        old_size = stencils.shape[0]
        stencils.resize(old_size + len(samples) , axis = 0)
        stencils[old_size:] = np.asarray(samples, dtype = np.float32)

        l = l_

        temperatures[timestep + 1] = l

        # print(f"\nTime step {timestep + 1}:")
        # for row in l:
        #     print(["{:.2f}".format(x) for x in row])
            
        im.set_data(l)
        ax.set_title(f"Heat Diffusion - Time step {timestep + 1}:")
        fig.canvas.draw_idle()
        plt.pause(0.2)

                
        timestep += 1


    f.close()

if __name__ == "__main__":
    heat_diffusion()