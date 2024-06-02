import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'


# Define the file path
def get_points():
    points_df.to_csv("./points_data.csv", sep="\t")

    with open("./header.txt", "w") as f:
        f.write(f'(0 "FOAM to Fluent Mesh File")\n\n')
        f.write(f'(0 "Dimension:")\n')
        f.write(f'(2 3)\n\n')
        f.write(f'(0 "Grid dimensions:")\n')
        f.write(f'(10 (0 1 {hex(n_points).split('x')[-1]} 0 3))\n')

    return points_df


def get_faces():
    
    # Face Header
    with open("./face_header.txt", "w") as f:
        f.write(f"(13 (2 1 {hex(len(face_df)).split('x')[-1]} 2 0)\n")

    # Footer
    with open("./footer.txt", "w") as f:
        f.write(f"(39 (1 fluid fluid-1)())\n")
        f.write(f"(39 (2 interior interior-1)())\n")

    return all_faces_df, owners_df, face_df




def get_boundary_info():
    boundary_file = "../mesh_ground/constant/polyMesh/boundary"
    file_data = read_file(boundary_file)
    [n_boundaries, trimmed_file] = get_file_info(file_data)

    boundary_info = []
    for k in range(n_boundaries):
        for n, i in enumerate(trimmed_file):
            if '{' in i:
                start = n
            if '}' in i:
                end = n
                break
        info_list = trimmed_file[start - 1:end]

        boundary_data = {
            'name': info_list[0].strip(),
            'type': get_info(info_list, 'type'),
            'start': int(get_info(info_list, 'startFace')),
            'n_faces': int(get_info(info_list, 'nFaces'))
        }

        trimmed_file = trimmed_file[end + 1:]
        boundary_info.append(boundary_data)

    return boundary_info


def get_boundary_data(all_faces_data, owner_data, boundary_info):
    boundary_id = 10
    count = 0
    for n, i in enumerate(boundary_info):
        if i['type'] != 'empty':
            count += 1
            end = i['start'] + i['n_faces']
            # print(f"{i['name']} = {i['start']} to {end}")
            boundary_data = all_faces_data[i['start']:end]
            boundary_data.columns = ["D", "C", "B", "A"]
            boundary_data["X"] = np.ones_like(boundary_data["A"])*4
            boundary_data = boundary_data[['X', 'A', 'B', 'C', 'D']]
            boundary_data["N"] = owner_data[i['start']:end]
            boundary_data["O"] = np.zeros_like(boundary_data["A"].values)
            boundary_data = boundary_data.reset_index(drop=True)
            boundary_data[['A', 'B', 'C', 'D', 'N']] = boundary_data[['A', 'B', 'C', 'D', 'N']].astype(int) +1
            boundary_data.to_csv(f'./boundary_data_{count}.csv', sep='\t')
            if i['type'] == 'wall':
                type = 3
                bc = 'wall'
            else:
                type = 4
                if i['name'] == 'inlet':
                    bc = 'mass-flow-inlet'
                if i['name'] == 'axis':
                    bc = 'axis'
                if i['name'] == 'outlet':
                    bc = 'pressure-outlet'

            with open(f"./boundary_header_{count}.txt", "w") as f:
                f.write(
                    f"(13 ({hex(boundary_id).split('x')[-1]} {hex(i['start'] + 1).split('x')[-1]} {hex(end).split('x')[-1]} {type} 0)\n")
            boundary_id += 1

            with open("./footer.txt", "a") as f:
                f.write(f"(39 ({boundary_id - 1} {bc} {i['name']})())\n")


def get_n_nodes():
    neighbour = read_file("../mesh_ground/constant/polyMesh/neighbour")
    return int(neighbour[11].split()[4])

def obtain_data():
    points_data = get_points()
    all_faces_data, owner_data, face_data = get_faces()
    boundary_info = get_boundary_info()
    n_nodes = get_n_nodes()
    get_boundary_data(all_faces_data, owner_data, boundary_info)

    with open("./header.txt", "a") as f:
        f.write(f'(12 (0 1 {hex(n_nodes).split('x')[-1]} 0 0))\n')
        f.write(f'(13 (0 1 {hex(len(all_faces_data)).split('x')[-1]} 0 0))\n\n')
        f.write(f'(10 (1 1 {hex(len(points_data)).split('x')[-1]} 1 3)\n(\n')

    with open("./node_header.txt", "w") as f:
        f.write(f'(12 (1 1 {hex(n_nodes).split('x')[-1]} 1 0)(\n')

    return len(boundary_info)-1

