# foam_to_fluent2D

- Converts fluent 3D mesh generated in OpenFoam for 2D geometries into 2D Fluent Mesh to used in ANSYS Fluent
- Mesh format that is handled is *.msh
- Should work for most of structured meshes.
- Automate meshing in batches.
- Saves Mesh info in a database.
- foamMeshToFluent3D takes more time than conversion from 2.5D to 2D. So, a direct approach to convert from blockMesh to Fluent 2D is DONE.

## Workflow
- First blockMesh is generated
- This script will convert that into Fluent 2D mesh removing extra single cell.

## Improvements to make:
- Conversion for other grid shapes like tet, poly, etc.

## Dependencies:
- Pandas
- Numpy
