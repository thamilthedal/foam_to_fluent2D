import os
from modules.create_blockmesh_dict import make_copy
from modules.foam_to_fluent2D import main as fmp
import modules.add_database as ad
import datetime

R = "1e-3"
L = "1"

# fmp()

# R L Nl Nr bf Lent Lexit
mesh_settings = [
        [R, L, "1000", "140", "0.01", "40", "10"],
        ]


ID = "thamil"

start = datetime.datetime.now()
print(f"ENGINE STARTS: {start}")
ad.check_dir(ID)
for n, i in enumerate(mesh_settings):
    mesh_name = f"M{n+1}-{ID}"
    make_copy(i)
    os.system("mv ./test ./mesh_ground/system/blockMeshDict")
    os.system("cd ./mesh_ground && blockMesh")
    fmp()
    os.system(f"mv ./mesh_ground/fluentInterface/mesh_ground_converted.msh ./mesh/{ID}/{mesh_name}.msh")
    # ad.add_database([mesh_name, ID, "2D", i[0], i[1], i[2], i[3], i[4], i[5], i[6]])

print(f"ENGINE HALTS: {datetime.datetime.now()-start}")
