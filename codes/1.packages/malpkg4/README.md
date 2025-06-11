# Malicious Package

This package is used to demonstrate common tricks by threat actor to masquerade malicious code.

## Malicious Build Hook

Python shift toward a more declarative and standardized build system (see PEP 517/518). Code execution during installation is not entirely eliminated, but just relocated into more complex.

Build backends, such as `Hatch`, `PDM`, and `poetry`, provide build hooks for modifying the inputs and outputs of source and built dsitribution creation. Malicious code then insert as hook for the build process.

## Usage

We have multiple examples which are specifically created for different build backend.

- Hatch
- PDM
- Poetry

See the instruction on each sample.
