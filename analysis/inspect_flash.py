import yt

ds = yt.load(
    "/home/hpc-08/FLASHComputationalPhysics/FLASH4.8/object/sedov_hdf5_plt_cnt_0000"
)

print("=" * 60)
print("Dataset type:", type(ds))
print("Dataset:", ds)
print()

print("Fields:")
for f in ds.field_list:
    print(" ", f)

print()

print("Max level:", ds.index.max_level)
print("Number of grids:", ds.index.num_grids)

print()

print("Domain dimensions:", ds.domain_dimensions)
print("Domain left edge:", ds.domain_left_edge)
print("Domain right edge:", ds.domain_right_edge)

print()

print("Grid summary")
for g in ds.index.grids[:10]:
    print(
        f"Grid {g.id:3d} | "
        f"Level {g.Level} | "
        f"Dims {g.ActiveDimensions}"
    )