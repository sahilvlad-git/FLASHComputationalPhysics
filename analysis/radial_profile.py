import yt

ds = yt.load(
    "/home/hpc-08/FLASHComputationalPhysics/FLASH4.8/object/sedov_hdf5_plt_cnt_0000"
)

sp = ds.sphere("c", (0.5, "unitary"))

profile = yt.create_profile(
    sp,
    ("index", "radius"),
    ("flash", "dens"),
)

print(profile)
