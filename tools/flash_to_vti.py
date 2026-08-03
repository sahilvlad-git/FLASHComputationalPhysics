import yt
import numpy as np
import pyvista as pv

# Load the FLASH dataset
ds = yt.load(
    "/home/hpc-08/FLASHComputationalPhysics/FLASH4.8/object/sedov_hdf5_plt_cnt_0000"
)

# Finest AMR resolution
level = ds.index.max_level

dims = ds.domain_dimensions * (2 ** level)

print("Sampling to:", dims)

cg = ds.covering_grid(
    level=level,
    left_edge=ds.domain_left_edge,
    dims=dims
)

density = np.array(cg[("flash", "dens")])

nx, ny, nz = density.shape

grid = pv.ImageData()

grid.dimensions = (nx + 1, ny + 1, nz + 1)

spacing = (
    (ds.domain_right_edge[0]-ds.domain_left_edge[0])/nx,
    (ds.domain_right_edge[1]-ds.domain_left_edge[1])/ny,
    (ds.domain_right_edge[2]-ds.domain_left_edge[2])/max(nz,1)
)

grid.origin = tuple(ds.domain_left_edge)

grid.spacing = spacing

grid.cell_data["density"] = density.ravel(order="F")

grid.save("sedov_uniform.vti")

print("Saved sedov_uniform.vti")