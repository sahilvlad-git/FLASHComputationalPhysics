# Installing and Building FLASH 4.8

This document records the complete process followed to install, configure, compile, and verify **FLASH 4.8** on a modern Ubuntu workstation. Rather than providing a generic installation guide, it documents the actual steps taken during this project, the issues encountered, and the reasoning behind each decision.

The primary objective was to produce a working FLASH executable capable of running the standard **Sedov Blast Wave** benchmark without modifying the scientific source code itself. All modifications were restricted to the machine-specific build configuration, ensuring that the original FLASH source remained untouched.

The document also serves as a reference for reproducing the build environment on similar Linux systems in the future.

---

# System Environment

The installation was performed on the following workstation.

| Component        | Version              |
| ---------------- | -------------------- |
| Operating System | Ubuntu 25.x (64-bit) |
| Architecture     | x86-64               |
| Processor        | Intel Core i7-13700  |
| Logical CPUs     | 24                   |
| Physical Cores   | 16                   |
| Installed Memory | 30 GiB               |
| GCC              | 15.2.0               |
| GNU Fortran      | 15.2.0               |
| GNU Make         | 4.4.1                |
| Python           | 3.13.7               |
| Git              | 2.51                 |
| OpenMPI          | 5.0.8                |
| Parallel HDF5    | 1.14.5               |
| FLASH            | 4.8                  |

Unlike many HPC clusters, this workstation did **not** use an Environment Modules system. Therefore, all required software was installed directly through Ubuntu's package manager and made available globally.

---

# Objectives

The goals of this stage of the project were:

* Prepare a complete scientific computing environment.
* Install every dependency required by FLASH.
* Configure FLASH for the local workstation.
* Successfully compile the FLASH executable.
* Run the Sedov Blast Wave verification problem.
* Generate valid HDF5 output files for visualization.

Completing these steps would establish a functioning computational physics environment before beginning any custom research simulations.

---

# 1. Inspecting the Existing Software Environment

Before installing any software, the existing environment was inspected to determine which development tools were already available.

The following commands were executed.

```bash
uname -a
lscpu
free -h

gcc --version
g++ --version
gfortran --version
make --version
python3 --version
git --version
mpirun --version
```

This inspection revealed that several essential components required by FLASH were either missing or incomplete.

Among them were:

* GNU Fortran
* Git
* OpenMPI
* Parallel HDF5 development libraries

Establishing the software environment first prevented later configuration problems and allowed every dependency to be verified individually.

---

# Why this step matters

FLASH is a large multiphysics simulation framework written primarily in **Fortran**, with portions written in **C** and **C++**. Building the software therefore requires considerably more than a standard C compiler.

Each component has a specific purpose.

| Software      | Purpose                                          |
| ------------- | ------------------------------------------------ |
| GCC           | Compiles C source files                          |
| G++           | Compiles C++ source files                        |
| GNU Fortran   | Compiles the numerical solver written in Fortran |
| Make          | Coordinates the build process                    |
| Git           | Version control                                  |
| OpenMPI       | Enables distributed-memory parallel computation  |
| Parallel HDF5 | High-performance scientific data storage         |

Without any one of these components, the FLASH build would eventually fail.

---

# 2. Installing the Required Development Tools

The Ubuntu package database was first updated.

```bash
sudo apt update
```

GNU Fortran and Git were then installed.

```bash
sudo apt install git gfortran
```

The MPI implementation and HDF5 libraries were installed afterwards.

```bash
sudo apt install \
    openmpi-bin \
    libopenmpi-dev \
    libhdf5-openmpi-dev \
    hdf5-tools
```

This installation supplied several important utilities, including:

* mpicc
* mpicxx
* mpif90
* mpifort
* mpiexec
* mpirun
* h5pcc
* h5pfc
* h5dump

These programs form the backbone of the FLASH build system.

---

# Verifying the HDF5 Installation

After installation, the HDF5 configuration was verified.

```bash
h5pcc -showconfig
```

The installed version was also confirmed.

```bash
h5dump --version
```

The configuration output confirmed that the installed HDF5 library supported:

* Parallel I/O
* MPI
* High-level HDF5 APIs
* C interface
* Fortran interface

This was important because FLASH performs all checkpointing and visualization output through HDF5.

---

# Insight

Ubuntu provides both **serial** and **parallel** versions of HDF5.

Installing only `libhdf5-dev` would produce a serial HDF5 installation that cannot be used efficiently by MPI programs.

Installing

```text
libhdf5-openmpi-dev
```

ensures that every HDF5 library has been compiled against OpenMPI, allowing FLASH to perform parallel file output during distributed simulations.

Understanding this distinction is useful because many scientific codes silently link against the wrong HDF5 installation when multiple versions exist on the same system.

---

# 3. Creating the FLASH Workspace

A dedicated project directory was created.

```bash
mkdir -p ~/FLASHComputationalPhysics
cd ~/FLASHComputationalPhysics
```

The FLASH archive was copied into this directory and extracted.

```bash
tar -xzf FLASH4.8.tar.gz
```

The extracted directory contained the complete FLASH source tree.

```text
FLASH4.8/
├── bin/
├── docs/
├── lib/
├── sites/
├── source/
├── tools/
├── setup
├── RELEASE
└── RELEASE-NOTES
```

Keeping the project inside its own workspace made it easier to maintain auxiliary software such as visualization tools, generated simulation output, and project documentation without interfering with the FLASH source tree.

---

# 4. Inspecting the FLASH Setup Utility

Before attempting any compilation, the setup script was tested.

```bash
cd FLASH4.8
./setup -h
```

The command successfully displayed the FLASH setup options but produced several Python warnings similar to:

```text
SyntaxWarning: invalid escape sequence
```

These warnings originated from legacy Python regular-expression syntax inside the FLASH setup scripts.

Despite the warnings, the setup utility executed correctly and displayed the expected help message.

---

# Insight

One of the most important lessons learned during installation was distinguishing **warnings** from **errors**.

A warning indicates that the interpreter has detected something that may be outdated or potentially problematic but is still able to continue execution.

An error, on the other hand, prevents the program from continuing.

Although the Python warnings initially appeared alarming, they did not affect the setup process because the script completed successfully.

Learning to identify harmless warnings avoids spending unnecessary time attempting to fix problems that do not actually impact the build.

---

# 5. Exploring the Available Simulation Problems

Before compiling FLASH, the available applications supplied with the distribution were inspected.

```bash
ls source/Simulation/SimulationMain
```

The source tree contained numerous benchmark and validation problems, including:

* Sedov Blast Wave
* Sod Shock Tube
* Double Mach Reflection
* Kelvin–Helmholtz Instability
* Rayleigh–Taylor Instability
* Jeans Collapse
* Wind Tunnel
* Magnetohydrodynamic examples
* Plasma simulations

Among these, the **Sedov Blast Wave** problem was selected as the first benchmark.

This problem is widely used for validating hydrodynamics codes because it exercises several core FLASH capabilities simultaneously:

* Hydrodynamic solver
* Adaptive Mesh Refinement (AMR)
* Equation of State
* HDF5 output
* Checkpoint generation

Successfully running the Sedov benchmark provides strong evidence that the installation has been completed correctly.

---

# 6. Creating a Machine-Specific Build Configuration

FLASH separates machine-dependent compiler settings from the scientific source code through **site configurations** stored inside the `sites` directory.

Rather than modifying the supplied GNU/OpenMPI configuration directly, a dedicated site directory was created.

```bash
mkdir -p sites/hpc-08
cp sites/gnu-ompi/Makefile.h sites/hpc-08/Makefile.h
```

All subsequent modifications were performed inside this copied `Makefile.h`.

This approach preserved the original FLASH configuration while allowing the workstation-specific configuration to evolve independently.

---

# Insight

Separating machine configuration from scientific source code is one of FLASH's strongest design choices.

Instead of editing dozens of build scripts scattered throughout the project, every compiler path, library location, optimization flag, and dependency is centralized inside a single configuration file.

This makes the build process significantly easier to understand, reproduce, and maintain.

It also means that upgrading FLASH in the future can often be done simply by copying the custom site configuration into a newer release without modifying the solver source code itself.

Yes. The next section is the heart of the installation process—the actual compilation, the compiler issues we encountered with GCC 15, how we fixed them, and finally producing the `flash4` executable. This is probably the most valuable part of the document because it records the real problems encountered on a modern Linux system.

---

# 7. Configuring the Sedov Blast Wave Simulation

With the build environment prepared, the FLASH setup utility was used to configure the standard Sedov Blast Wave verification problem.

The setup command generates a customized build tree by selecting only the source files required for the chosen simulation.

The following command was executed from the FLASH root directory.

```bash
./setup Sedov -auto +parallelIO -site=hpc-08
```

Each option has a specific purpose.

| Option         | Purpose                                                         |
| -------------- | --------------------------------------------------------------- |
| `Sedov`        | Selects the Sedov Blast Wave problem                            |
| `-auto`        | Automatically resolves required software units and dependencies |
| `+parallelIO`  | Enables parallel HDF5 output                                    |
| `-site=hpc-08` | Uses the workstation-specific compiler configuration            |

Unlike traditional software compilation, FLASH does not build directly from the source tree.

Instead, the setup utility constructs a completely new directory named `object/`, containing only the files necessary for the selected simulation.

This significantly reduces compilation time while keeping the original source tree untouched.

---

# The Generated Object Directory

After setup completed successfully, the generated directory contained files similar to:

```text
object/
├── Makefile
├── Simulation.h
├── setup_call
├── flash.par
├── buildstamp_gen.txt
├── *.F90
├── *.o
└── ...
```

The `object` directory serves as an isolated build environment.

All compilation, linking, executable generation, and simulation output occur inside this directory.

This design allows multiple FLASH simulations to coexist simultaneously without interfering with one another.

---

# Insight

One of the design philosophies of FLASH is that **simulation setup and code compilation are separate processes.**

Running `setup` does **not** compile the code.

Instead, it assembles a custom source tree tailored to a specific simulation.

Compilation begins only after entering the generated `object` directory and invoking `make`.

This separation provides tremendous flexibility, allowing entirely different physics problems to be compiled independently from the same FLASH source installation.

---

# 8. Beginning the Compilation

Compilation was started from inside the generated build directory.

```bash
cd object
make -j8
```

The `-j8` option allows GNU Make to compile multiple source files simultaneously, reducing build time by utilizing multiple processor cores.

Compilation proceeded normally for several minutes before eventually terminating with numerous Fortran compiler errors.

The failures were not related to missing software packages but rather to changes introduced in newer versions of GNU Fortran.

---

# Compiler Errors with GCC 15

The workstation used GCC and GNU Fortran version **15.2**, considerably newer than the compiler versions commonly used when FLASH 4.8 was originally developed.

Several compilation failures originated from stricter argument checking introduced in recent GNU Fortran releases.

Typical error messages reported argument mismatches between procedure calls and their corresponding interfaces.

Although these constructs had historically been accepted by older compilers, GNU Fortran now treats many of them as fatal compilation errors.

---

# Investigating the Compiler

Rather than immediately modifying FLASH source code, the compiler capabilities were investigated.

The following command was used.

```bash
gfortran --help=fortran | grep argument-mismatch
```

The compiler reported support for the following option.

```text
-fallow-argument-mismatch
```

This compiler flag restores the more permissive argument checking behavior expected by older scientific software.

---

# Why This Option Exists

Large scientific software packages often remain under active development for decades.

Compiler standards, however, evolve continuously.

As newer compilers become stricter, legacy code that previously compiled successfully may begin producing errors despite remaining scientifically correct.

GNU Fortran therefore provides compatibility flags that preserve support for older coding practices while developers gradually modernize the source code.

In this case, the issue arose from compiler compatibility rather than an error in the underlying numerical algorithms.

---

# 9. Updating the Build Configuration

Instead of modifying FLASH source files, the workstation-specific compiler configuration was updated.

Inside the custom site configuration (`sites/hpc-08/Makefile.h`), the Fortran compiler flags were extended to include:

```text
-fallow-argument-mismatch
```

This ensured that the compatibility option would automatically be applied whenever FLASH was compiled on this workstation.

Keeping the modification confined to the machine configuration preserved the integrity of the original FLASH source tree.

---

# Insight

A key principle followed throughout this project was to avoid altering scientific source code whenever possible.

If a problem could be solved by adjusting compiler flags, library paths, or build configuration, those solutions were preferred over editing the numerical implementation itself.

Maintaining a clean source tree greatly simplifies future updates and allows the installation procedure to remain reproducible.

---

# 10. Successful Compilation

After updating the compiler configuration, the build process was repeated.

```bash
make clean
make -j8
```

This time the compilation completed successfully.

Although numerous compiler warnings were still displayed, the build continued to completion and terminated with the message:

```text
SUCCESS
```

Unlike the previous attempt, no fatal compiler errors remained.

The generated executable was written inside the build directory as

```text
flash4
```

This marked the first successful compilation of FLASH on the workstation.

---

# Verifying the Executable

The executable was inspected using standard Linux utilities.

```bash
ls -lh flash4
file flash4
```

The resulting output confirmed that the executable had been generated correctly.

```text
-rwxrwxr-x ... flash4
ELF 64-bit LSB pie executable
```

The reported executable size was approximately **6 MB**, indicating that the linking stage had completed successfully.

The `file` utility further confirmed that the binary was a valid **64-bit ELF executable** for Linux.

---

# Insight

One lesson learned during compilation was that a large number of warnings does **not** necessarily indicate failure.

Modern scientific software often produces many compiler warnings because it must remain compatible with multiple compiler versions, operating systems, and architectures.

The decisive indicator is the final build status.

In this case, despite hundreds of warning messages appearing throughout compilation, the presence of the final **SUCCESS** message confirmed that the executable had been built correctly.

Consequently, it is important to distinguish between informational compiler warnings and errors that actually terminate the build process.
