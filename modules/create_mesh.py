import os
from modules.create_blockmesh_dict import make_copy
from modules.foam_to_fluent2D import main as fmp
import modules.add_database as ad

R = "2.5e-3"
L = "0.75"

mesh_settings = [
        [R, L, "180", "100"],
        [R, L, "375", "100"],
        [R, L, "750", "100"],
        [R, L, "375", "120"],
        [R, L, "375", "140"]
        ]

# mesh_settings = [[R, L, "100", "100"]]

ID = "F1"

for n, i in enumerate(mesh_settings):
    mesh_name = f"M{n+1}-{ID}"
    make_copy(i)
    os.system("cp ./test ./mesh_ground/system/blockMeshDict")
    os.system("cd ./mesh_ground && blockMesh && foamMeshToFluent")
    fmp()
    os.system(f"mv ./mesh_ground/fluentInterface/mesh_ground_converted.msh ./mesh/{mesh_name}.msh")
    ad.add_database([mesh_name, ID, "2D", i[0], i[1], i[3], i[2]])

