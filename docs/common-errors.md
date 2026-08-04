# Common Errors

This document collects the most common issues encountered while installing, compiling, running, and visualizing FLASH simulations.

Whenever a new problem is solved, it should be documented here for future reference.

---

## 1. `module: command not found`

### Error

```bash
module: command not found
```

### Cause

The system does not use an Environment Modules installation.

### Solution

Install all dependencies manually using the system package manager.

Example:

```bash
sudo apt install openmpi-bin libopenmpi-dev
sudo apt install libhdf5-openmpi-dev
sudo apt install gfortran
```

---

## 2. FLASH Python setup warnings

### Message

```text
SyntaxWarning:
```

during

```bash
./setup Sedov -auto
```

### Cause

FLASH 4.8 contains legacy Python scripts written before recent Python versions.

### Solution

These warnings are generally harmless.

If setup completes successfully, they can be ignored.

---

## 3. Compilation fails

### Possible causes

- Missing MPI
- Missing HDF5
- Incorrect Makefile.h
- Compiler mismatch

### Useful commands

```bash
which mpif90
```

```bash
mpif90 --version
```

```bash
h5pcc -showconfig
```

---

## 4. FLASH executable not created

### Symptom

After

```bash
make
```

no executable named

```text
flash4
```

appears.

### Possible causes

- Build failure
- Compilation stopped earlier
- Missing dependency

### Solution

Inspect the first compiler error rather than the final one.

---

## 5. No plot files generated

### Symptom

Simulation runs successfully but no

```text
hdf5_plt_cnt
```

files are written.

### Cause

Output intervals are disabled.

Example:

```text
plotFileIntervalStep = 0
```

or

```text
plotFileIntervalTime = 0
```

### Solution

Enable one of the output intervals.

Example

```text
plotFileIntervalStep = 10
```

or

```text
plotFileIntervalTime = 0.005
```

---

## 6. No checkpoint files generated

### Cause

Checkpoint interval disabled.

Example

```text
checkpointFileIntervalStep = 0
```

### Solution

Set

```text
checkpointFileIntervalStep = 10
```

or use

```text
checkpointFileIntervalTime
```

---

## 7. yt cannot find the FLASH file

### Error

```text
FileNotFoundError
```

### Cause

Incorrect path.

Common mistake:

```python
filename = "sedov_hdf5_plt_cnt_0001"
```

while the file is actually located elsewhere.

### Solution

Always provide the absolute path.

Example

```python
filename = "/home/user/FLASH4.8/object/sedov_hdf5_plt_cnt_0010"
```

---

## 8. yt reports "No such file or directory"

### Cause

The simulation never produced that plot file.

### Solution

Verify the available files.

```bash
ls object | grep plt
```

---

## 9. ParaView only shows a thin slice

### Symptom

The simulation appears on one face of the cube rather than occupying the full volume.

### Cause

FLASH was compiled as a two-dimensional simulation.

Example

```text
DN_DIM = 2
NZB = 1
```

### Verification

```bash
cat object/setup_flags
```

Look for

```text
-DN_DIM=2
```

or

```text
-DN_DIM=3
```

---

## 10. ParaView opens but nothing is visible

### Possible causes

- Forgot to press **Apply**
- Camera outside the domain
- Wrong scalar selected
- Data range not rescaled

### Solution

1. Click **Apply**
2. Reset Camera
3. Select a scalar field
4. Rescale to Data Range

---

## 11. Simulation is unexpectedly 2D

### Symptom

Output contains

```text
domain_dimensions = [8 8 1]
```

or

```text
Grid dimensions : [256 256 32]
```

with only one physical layer.

### Diagnosis

Check

```bash
cat object/setup_call
```

and

```bash
cat object/setup_flags
```

If

```text
DN_DIM = 2
```

appears, the executable was built in two dimensions.

### Solution

Rebuild FLASH with

```bash
./setup Sedov -3d -auto
```

followed by

```bash
make clean
make -j
```

---

## 12. Changes to flash.par have no effect

### Cause

Editing the wrong parameter file.

FLASH copies runtime files into the object directory during setup.

### Solution

Always verify which parameter file is being used.

---

## Useful Diagnostic Commands

List plot files

```bash
ls object | grep plt
```

List checkpoint files

```bash
ls object | grep chk
```

Check build dimensions

```bash
cat object/setup_flags
```

Check setup command

```bash
cat object/setup_call
```

Check runtime parameters

```bash
grep plot flash.par
```

Locate simulation files

```bash
find source/Simulation/SimulationMain/Sedov
```

---

## General Advice

When something fails,

1. Read the **first** error message, not the last.
2. Verify file paths before debugging code.
3. Confirm whether the issue originates from FLASH, yt, or ParaView.
4. Record every solution in this document to build a reusable troubleshooting guide.

---
