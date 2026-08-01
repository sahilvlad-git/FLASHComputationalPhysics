# Build Notes

This document records build-specific observations, compatibility issues, and installation decisions made during the project.

It is intended as a quick reference for reproducing the installation without rereading the full documentation.

---

# Build Summary

| Component | Status |
|----------|--------|
| FLASH Setup | Successful |
| Compilation | Successful |
| MPI Support | Enabled |
| Parallel HDF5 | Enabled |
| Test Simulation - SedovBlast | Successful |

---

# Compiler Compatibility

FLASH 4.8 was compiled using

```
GNU Fortran 15.2
```

Compilation initially failed because modern GNU Fortran performs stricter argument checking than older releases.

The issue was resolved by adding the compiler flag

```text
-fallow-argument-mismatch
```

to the workstation-specific `Makefile.h`.

This preserved the original FLASH source code while restoring compatibility with the newer compiler.

---

# Build Configuration

Simulation setup command:

```bash
./setup Sedov -auto +parallelIO -site=hpc-08
```

Compilation command:

```bash
make -j8
```

Execution command:

```bash
mpirun -np 4 ./flash4
```

---

# Important Observations

- Numerous compiler warnings were produced during compilation.
- Despite the warnings, the build completed successfully.
- The final indicator of a successful build was the appearance of the `SUCCESS` message.
- A valid executable named `flash4` was generated.

---

# Output Verification

Successful execution produced:

- Runtime log (`sedov.log`)
- Diagnostic output (`sedov.dat`)
- Checkpoint files (`sedov_hdf5_chk_*`)
- Plot files (`sedov_hdf5_plt_cnt_*`)

These outputs confirmed that:

- MPI was functioning correctly.
- HDF5 output was working.
- FLASH reached the specified maximum simulation time.
- The installation was operational.

---

# Visualization Notes

VisIt 3.5.0 was selected as the primary visualization software because it is the package recommended throughout the FLASH User Guide.

Installation on Ubuntu 25 required additional troubleshooting due to shared library compatibility issues with the precompiled Ubuntu 24 binaries.

These issues are documented separately in the visualization documentation.

---

# Lessons Learned

- Prefer fixing build issues through compiler configuration rather than modifying FLASH source code.
- Keep machine-specific changes isolated inside the site configuration.
- Always verify both compilation **and** execution.
- Record software versions to ensure future reproducibility.
- Treat compiler warnings and compiler errors differently—warnings alone do not necessarily indicate an unsuccessful build.

---

_Last updated: August 2026_