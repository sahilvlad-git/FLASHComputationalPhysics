import yt
import numpy as np

ds = yt.load(
"/home/hpc-08/FLASHComputationalPhysics/FLASH4.8/object/sedov_hdf5_plt_cnt_0000"
)

level = ds.index.max_level

dims = ds.domain_dimensions * (2**level)

cg = ds.covering_grid(
    level,
    ds.domain_left_edge,
    dims=dims,
)

rho = np.array(cg[("flash","dens")])

print("shape =", rho.shape)

print("min =", rho.min())
print("max =", rho.max())
print("mean =", rho.mean())

print("unique values (first 20):")
print(np.unique(rho)[:20])

print("number unique =", len(np.unique(rho)))