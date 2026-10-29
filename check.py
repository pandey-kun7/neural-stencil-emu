import h5py
import numpy as np

with h5py.File("heat_diffusion.hdf5", "r") as f:
    stencils = f["simulation__5/stencils"]

    print("Shape:", stencils.shape)
    for i in range(len(stencils)):
        if np.all(stencils[i, :5] != 0):
            print(i, stencils[i])

    print("Any non-zero:", np.sum(np.any(stencils[:, :5] != 0, axis=1)))
