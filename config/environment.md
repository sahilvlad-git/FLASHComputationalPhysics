# Software Environment

This document records the software environment used throughout this project. Recording version information is essential for reproducibility, especially when working with large scientific software packages such as FLASH.

## Operating System

| Component        | Version               |
| ---------------- | --------------------- |
| Operating System | Ubuntu 25.xx (64-bit) |

> **Note:** Ubuntu 25 was used throughout this project. Some third-party scientific software (e.g., VisIt) officially provided binaries only for Ubuntu 24, leading to compatibility issues discussed later in the documentation.

---

## Compiler Toolchain

| Software    | Version |
| ----------- | ------- |
| GCC         | 15.2.0  |
| GNU Fortran | 15.2.0  |

Compiler compatibility required additional configuration because newer GNU Fortran releases perform stricter argument checking than versions commonly used when FLASH 4.8 was developed.

---

## Parallel Computing

| Software | Version |
| -------- | ------- |
| OpenMPI  | 5.0.8   |

FLASH was compiled and executed using MPI support.

---

## Data Format Libraries

| Library | Version                               |
| ------- | ------------------------------------- |
| HDF5    | Installed through Ubuntu repositories |

Parallel HDF5 output was enabled during setup using

```bash
+parallelIO
```

---

## Python

| Software | Version                         |
| -------- | ------------------------------- |
| Python   | System installation (Ubuntu 25) |

Python is used internally by the FLASH setup system.

---

## Scientific Software

| Software | Version |
| -------- | ------- |
| FLASH    | 4.8     |
| VisIt    | 3.5.0   |

---

## Hardware

Development and testing were performed on an institutional HPC workstation.

| Component        | Details                      |
| ---------------- | ---------------------------- |
| Architecture     | x86_64                       |
| Memory           | ~30 GB RAM                   |
| Operating System | Ubuntu Linux                 |
| MPI Execution    | Local multi-core workstation |

---

## Repository Notes

As the project evolves, this document will be updated whenever major software versions change.

Future additions may include:

- ParaView
- yt
- Python visualization libraries
- Additional compiler versions
- Performance benchmarks
