from helper import read_file

A = read_file("./mesh_test.msh")

B = read_file("./mesh_ground_converted.msh")
count = 0
for n, i in enumerate(A):
    if i != B[n]:
        print(n, i, B[n])
        count += 1

print(count)

