with open("./intern/mesh_ground_converted.msh", "r") as f:
    A = f.readlines()


with open("./mesh_ground/fluentInterface/mesh_ground_converted.msh", "r") as g:
    B = g.readlines()


for n, i in enumerate(A):
    if i != B[n]:
        print(i)
        print(B[n])


