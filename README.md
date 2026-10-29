# Heat Diffusion Simulation

This project simulates a 2D heat diffusion process on a rectangular grid and stores the simulation output in an HDF5 file. It also renders a live matplotlib heatmap while the simulation runs.

## Features

- Interactive setup for grid size, number of hotspots, time steps, and diffusion coefficient
- 2D diffusion update using a finite-difference style stencil
- Live visual output of temperature distribution
- HDF5 export of simulation data for later inspection or processing

## Project Files

- `main.py` — runs the interactive heat diffusion simulation
- `synthetic_data.py` — intended for synthetic data generation / related utilities
- `check.py` — quick validation script to inspect HDF5 stencil data
- `heat_diffusion.hdf5` — generated simulation output file

## Requirements

Install the required Python dependencies:

```bash
pip install numpy matplotlib h5py
```

## Running the Simulation

From the project root, run:

```bash
python main.py
```

You will be prompted to enter:

- grid size as `rows cols`
- number of hotspots
- number of time steps
- diffusion coefficient
- hotspot coordinates and temperature values

Example:

```text
Enter grid (rows cols): 10 10
Enter no. of hotspots : 2
Enter number of time steps: 50
Enter diffusion coefficient: 0.1
Enter hotspot coordinates: 2 2
Enter temperature of hotspot at 2 - 2 coord. : 100
Enter hotspot coordinates: 7 7
Enter temperature of hotspot at 7 - 7 coord. : 80
```

## Output

The simulation saves its results in `heat_diffusion.hdf5` using a versioned structure, for example:

```text
simulation__1/
  metadata/
    rows
    cols
    time_steps
    alpha
  temp
  stencils
```

- `temp` stores the full temperature field for each time step
- `stencils` stores sampled diffusion stencil information per step

## Inspecting Data

A quick check can be performed with:

```bash
python check.py
```

This script opens the HDF5 file and prints the shape and a few non-zero stencil samples.

## Notes

- The simulation currently expects valid grid coordinates for all hotspots.
- The figure is displayed with `matplotlib` and updates over time while the simulation runs.
- The HDF5 file is appended to with a new versioned group each time the simulation is executed.
