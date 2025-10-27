# Command Line Interface for converting OpenFOAM created 2.5D meshes into ANSYS Fluent 2D meshes:

## Command:
foamFluent2D

## Getting Started

1. Download the repository
2. Use Python 3.12 or above.
3. Run following command
```
pip install -e .
```

4. Run this command after creating a psuedo-2D blockMesh

```
ff2 --dir "."
```

# Version History

## Version 1.3
Refactored writer module completely to reduce the lines of code while maintaining similar speed.

## Version 1.1 
Find the list of two Z automatically and filter the first alone (Z1 and Z2 can be any two values)


## Version 1.0
Basic Foam To Fluent 2D for Cartesian 2D grids with a single cell thickness with multiple blocks but for single domain 
(Z1 = 0 and Z2 > 0)




