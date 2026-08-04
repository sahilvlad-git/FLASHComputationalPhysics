# 04 — Post-processing FLASH Data with yt

This document describes the workflow used to convert FLASH HDF5 output into a format suitable for scientific visualization using **ParaView**.

The conversion was performed using the Python analysis package **yt**, which provides native support for FLASH AMR datasets.

---

## Objective

The primary goals of post-processing are

- Read FLASH HDF5 plot files
- Extract physical variables from the AMR hierarchy
- Convert adaptive mesh data into a uniform Cartesian grid
- Export the dataset in VTK ImageData (`.vti`) format
- Visualize the simulation using ParaView

---

## Why yt?

FLASH stores simulation data using **Adaptive Mesh Refinement (AMR)**.

Unlike a regular Cartesian grid, AMR consists of many blocks at different refinement levels.

Most visualization software expects structured datasets.

The **yt** library

- understands FLASH HDF5 files directly
- reconstructs the AMR hierarchy
- provides access to physical fields
- allows resampling onto uniform grids
- supports export to other visualization formats

---

## Installing yt

A dedicated Python virtual environment was created.

```bash
python3 -m venv yt-env
```

Activate it

```bash
source yt-env/bin/activate
```

Install the required packages

```bash
pip install yt
pip install pyvista
pip install vtk
pip install numpy
```

---

## Loading a FLASH Dataset

A FLASH plot file can be loaded directly.

```python
import yt

ds = yt.load(
    "/path/to/sedov_hdf5_plt_cnt_0010"
)
```

After loading, yt automatically reports

- simulation time
- domain dimensions
- domain boundaries
- refinement hierarchy

Example output

```text
current_time = 0.05016
domain_dimensions = [8 8 1]
domain_left_edge = [0. 0. 0.]
domain_right_edge = [1. 1. 1.]
```

---

## Determining the Finest Resolution

FLASH stores data adaptively.

To obtain a uniform dataset suitable for ParaView, the finest AMR level is sampled.

```python
level = ds.index.max_level

dims = ds.domain_dimensions * (2 ** level)
```

Example

```text
Max AMR level : 5
Grid dimensions : [256 256 32]
```

---

## Constructing a Covering Grid

The adaptive mesh is converted into a single uniform grid.

```python
cg = ds.covering_grid(
    level=level,
    left_edge=ds.domain_left_edge,
    dims=dims
)
```

The resulting object behaves like a regular three-dimensional NumPy array.

---

## Extracting Physical Fields

Individual variables can be accessed directly.

Example

```python
density = np.array(cg[("flash", "dens")])

pressure = np.array(cg[("flash", "pres")])

temperature = np.array(cg[("flash", "temp")])
```

The exported fields used in this project were

- Density
- Pressure
- Temperature

Additional FLASH variables can be extracted in the same way.

---

## Creating a VTK ImageData Object

PyVista was used to construct a VTK ImageData object.

```python
grid = pv.ImageData()
```

Grid dimensions

```python
grid.dimensions = (nx + 1, ny + 1, nz + 1)
```

Grid origin

```python
grid.origin = tuple(ds.domain_left_edge)
```

Grid spacing

```python
grid.spacing = spacing
```

---

## Adding Simulation Fields

Physical variables are attached as cell-centered data.

Example

```python
grid.cell_data["density"] = density.ravel(order="F")

grid.cell_data["pressure"] = pressure.ravel(order="F")

grid.cell_data["temperature"] = temperature.ravel(order="F")
```

The use of

```python
order="F"
```

ensures compatibility between NumPy memory layout and VTK's expected storage order.

---

## Exporting to VTI

The processed dataset is saved as

```python
grid.save("sedov_hdf5_plt_cnt_0010.vti")
```

Result

```text
Conversion complete

Output file:
sedov_hdf5_plt_cnt_0010.vti

Fields exported

• density
• pressure
• temperature
```

---

## Verification

The exported VTI file was opened in ParaView.

Successful verification included

- dataset loaded without errors
- density visualized correctly
- pressure visualized correctly
- temperature visualized correctly
- radial Sedov shock clearly visible
- animation across plot files worked as expected

---

## Important Observation

Although the VTI conversion worked correctly, the visualization revealed that the blast wave evolved only on a single plane.

Inspection of the dataset showed

```text
domain_dimensions = [8 8 1]
```

and

```text
Grid dimensions = [256 256 32]
```

The simulation had been compiled in **2D**, with only one computational cell along the z-direction.

As a result,

- yt produced a valid VTI file
- ParaView displayed the correct solution
- the visualization appeared as a thin planar slice instead of a true volumetric explosion

The issue originated from the FLASH build configuration rather than the post-processing workflow.

---

## Overall Workflow

```text
FLASH HDF5 Plot File
          │
          ▼
      yt.load()
          │
          ▼
  Adaptive Mesh (AMR)
          │
          ▼
   covering_grid()
          │
          ▼
 Uniform Cartesian Grid
          │
          ▼
      NumPy Arrays
          │
          ▼
     PyVista ImageData
          │
          ▼
       Export (.vti)
          │
          ▼
        ParaView
```

---
