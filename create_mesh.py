import os
from modules.create_blockmesh_dict import make_copy
from modules.foam_to_fluent2D import main as fmp
import modules.add_database as ad

R = "5e-3"
L = "2.5"

mesh_settings = [
        [R, L, "500", "80", "0.01", "30", "40"],
        # [R, L, "500", "100", "0.01", "30", "40"],
        # [R, L, "500", "120", "0.01", "30", "40"]
        ]

ID = "Z1"

for n, i in enumerate(mesh_settings):
    mesh_name = f"M{n+1}-{ID}"
    make_copy(i)
    os.system("mv ./test ./mesh_ground/system/blockMeshDict")
    os.system("cd ./mesh_ground && blockMesh")
    fmp()
    os.system(f"mv ./mesh_ground/fluentInterface/mesh_ground_converted.msh ./mesh/{mesh_name}.msh")
    ad.add_database([mesh_name, ID, "2D", i[0], i[1], i[2], i[3], i[4], i[5], i[6]])

