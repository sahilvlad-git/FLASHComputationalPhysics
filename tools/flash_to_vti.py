import yt
import numpy as np
import pyvista as pv

# ============================================================
# FLASH -> VTI Converter
# ============================================================

# FLASH plot file
filename = "/home/hpc-08/FLASHphysics/FLASH4.8/object/sedov_hdf5_plt_cnt_0010"
print(filename)

# ------------------------------------------------------------
# Load dataset
# ------------------------------------------------------------
ds = yt.load(filename)

# Finest AMR level
level = ds.index.max_level

# Uniform grid dimensions
dims = ds.domain_dimensions * (2 ** level)

print("=" * 60)
print("FLASH Dataset")
print("=" * 60)
print(f"Input file      : {filename}")
print(f"Max AMR level   : {level}")
print(f"Grid dimensions : {dims}")
print()

# ------------------------------------------------------------
# Create uniform covering grid
# ------------------------------------------------------------
cg = ds.covering_grid(
    level=level,
    left_edge=ds.domain_left_edge,
    dims=dims
)

# ------------------------------------------------------------
# Extract fields
# ------------------------------------------------------------
density = np.array(cg[("flash", "dens")])
pressure = np.array(cg[("flash", "pres")])
temperature = np.array(cg[("flash", "temp")])

nx, ny, nz = density.shape

# ------------------------------------------------------------
# Create PyVista ImageData
# ------------------------------------------------------------
grid = pv.ImageData()

grid.dimensions = (nx + 1, ny + 1, nz + 1)

spacing = (ds.domain_right_edge - ds.domain_left_edge) / dims

grid.origin = tuple(ds.domain_left_edge)
grid.spacing = tuple(spacing)

# ------------------------------------------------------------
# Add fields
# ------------------------------------------------------------
grid.cell_data["density"] = density.ravel(order="F")
grid.cell_data["pressure"] = pressure.ravel(order="F")
grid.cell_data["temperature"] = temperature.ravel(order="F")

# ------------------------------------------------------------
# Save VTI
# ------------------------------------------------------------
outfile = filename + ".vti"

grid.save(outfile)

print("=" * 60)
print("Conversion complete")
print("=" * 60)
print(f"Output file : {outfile}")
print("Fields exported:")
print("  • density")
print("  • pressure")
print("  • temperature")
print("=" * 60)