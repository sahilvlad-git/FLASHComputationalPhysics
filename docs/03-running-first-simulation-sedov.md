# Running the First FLASH Simulation

This document describes the complete workflow used to configure, build, and execute the **Sedov blast wave** example using **FLASH 4.8**, as well as the generation of simulation output for post-processing and visualization.

---

## Objective

The objective of this simulation is to verify that the FLASH installation functions correctly by running one of the standard verification problems included with the codebase.

The **Sedov blast wave** is a classical hydrodynamics test involving an instantaneous release of energy into a uniform medium, producing a spherically expanding shock wave.

---

## Prerequisites

Before running the simulation, ensure the following have been completed:

- Linux environment configured
- MPI installed
- HDF5 installed
- FLASH successfully built

Refer to:

- `01-linux-and-hpc-environment.md`
- `02-installing-and-building-flash.md`

---

## Configuring the Simulation

From the FLASH root directory,

```bash
cd FLASH4.8
```

Configure the Sedov problem using

```bash
./setup Sedov -auto
```

The `-auto` option automatically selects the required units and dependencies for the simulation.

The generated executable and object files are placed inside

```text
FLASH4.8/object/
```

---

## Building FLASH

Move into the object directory

```bash
cd object
```

Compile using

```bash
make -j8
```

where

- `-j8` instructs `make` to use eight parallel compilation jobs.

If compilation succeeds, the executable

```text
flash4
```

will be produced.

---

## Runtime Parameters

Simulation parameters are controlled by

```text
flash.par
```

Typical parameters include

- domain size
- initial density
- explosion energy
- simulation end time
- output frequency
- AMR refinement
- boundary conditions

Example:

```text
sim_expEnergy = 1.0
sim_rhoAmbient = 1.0
tmax = 0.05
lrefine_max = 5
```

---

## Generating Plot Files

Initially, no plot files were generated because

```text
plotfileIntervalStep = 0
```

disables step-based output.

This was changed to

```text
plotfileIntervalStep = 1
```

allowing FLASH to write a plot file every timestep.

Checkpoint files remained enabled independently.

---

## Running the Simulation

Execute using MPI.

Example

```bash
mpirun -np 8 ./flash4
```

where

- `-np 8` launches eight MPI processes.

During execution, FLASH reports

- timestep
- simulation time
- timestep size
- refinement information
- output events

---

## Output Files

Several types of files are generated.

## Plot Files

```text
sedov_hdf5_plt_cnt_0000
sedov_hdf5_plt_cnt_0001
...
```

These contain the physical variables used for visualization and post-processing.

---

## Checkpoint Files

```text
sedov_hdf5_chk_0000
sedov_hdf5_chk_0001
...
```

Checkpoint files store the complete simulation state and allow restarting the simulation from intermediate times.

---

## Log File

FLASH also generates a runtime log containing

- compilation information
- runtime parameters
- timestep history
- performance statistics
- completion status

---

## Simulation Verification

The successful run produced

- multiple plot files
- multiple checkpoint files
- no runtime errors
- stable evolution of the Sedov blast wave

These outputs were later processed using **yt** and visualized in **ParaView**.

---

## Important Observation

Although the blast wave appeared physically correct, visualization revealed that the simulation evolved only in a single plane.

Investigation showed the FLASH executable had been compiled as a **2-dimensional simulation**.

Compilation flags confirmed

```text
DN_DIM = 2
NZB = 1
```

indicating

- two-dimensional computational domain
- only one computational cell along the z-direction

Consequently, ParaView displayed the blast wave on one face of the cube rather than throughout the volume.

The simulation itself was correct, but it represented a **2D Sedov blast**, not a true three-dimensional explosion.

Resolving this requires rebuilding FLASH with

- 3D configuration (`--3d`)
- non-unit z-block size (`NZB > 1`)

This investigation is documented further in `07-common-errors.md`.

---

## Workflow Summary

```text
FLASH Setup
      │
      ▼
./setup Sedov -auto
      │
      ▼
make -j8
      │
      ▼
flash4 executable
      │
      ▼
Edit flash.par
      │
      ▼
mpirun -np 8 ./flash4
      │
      ▼
HDF5 Plot Files
      │
      ▼
yt
      │
      ▼
VTI
      │
      ▼
ParaView Visualization
```

---
