import helper as ch
import pandas as pd
import new_converter as cc
import numpy as np
import writer as cw
pd.options.mode.chained_assignment = None

def point_work():
    # Reading Points
    n_points, point_file_list = ch.get_file_info('points')
    
    clean_data = [ch.clean_and_split(item) for item in point_file_list]
    points_df = pd.DataFrame(clean_data, columns=["X", "Y", "Z"])
    print(f"Before Conversion, Number of Points: {n_points}")

    # Converting to 2D
    points_df["ID"] = points_df.index
    remove_index = points_df[points_df['Z'] != '0'].index
    points_df = points_df.drop(index = remove_index)
    points_df = points_df.reset_index(drop=True)
    points_df['new_ID'] = points_df.index 
    points_df.pop('Z')

    # Saving to CSV or Returning Points DF
    return points_df

def face_work(points_df):

    # Face Reading
    face_file_list = ch.get_file_info('faces')[1][1:]

    clean_data = [ch.clean_and_split_face(item) for item in face_file_list]
    all_faces_df = pd.DataFrame(clean_data, columns=["A", "B", "C", "D"]).astype(int)

    # Neighbour Info Reading
    neighbour_file_list = ch.get_file_info('neighbour')[1][1:]
    clean_data = [item.strip() for item in neighbour_file_list]
    neighbours_df = pd.DataFrame(clean_data, columns=["N"]).astype(int)

    # Owner Info Reading
    owner_file_list = ch.get_file_info('owner')[1][1:]
    clean_data = [item.strip() for item in owner_file_list]
    owners_df = pd.DataFrame(clean_data, columns=["O"]).astype(int)

    # 4 A B C D Neighbor Owner
    # Face Data
    face_df = all_faces_df.iloc[0:len(neighbours_df)]
    face_df = face_df[['A', 'B', 'C', 'D']]
    face_df["N"] = neighbours_df.iloc[0:len(neighbours_df)]
    face_df["O"] = owners_df.iloc[0:len(neighbours_df)]
    
    # print(face_df.head)
    face_df = face_df.reset_index(drop=True)

    face_df[['A', 'B', 'C', 'D', 'N', 'O']] = face_df[['A', 'B', 'C', 'D', 'N', 'O']].astype(int) + 1

    print(f"Before Conversion, Number of Faces: {len(face_df)}")
    # Convert Face Data into 2D
    face_df = cc.convert_face_data(face_df, points_df)

    # All Faces DF
    all_faces_df["O"] = owners_df.iloc[0:len(all_faces_df)]
    # all_faces_df[['A', 'B', 'C', 'D', 'O']] = all_faces_df[['A', 'B', 'C', 'D', 'O']]

    print(f"Before Conversion, Total number of all faces: {len(all_faces_df)}")
    return all_faces_df, face_df

def boundary_work(all_faces_df, points_df):

    # Reading Boundary Information
    [n_boundaries, trimmed_file] = ch.get_file_info('boundary')
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
            'type': ch.get_boundary_info(info_list, 'type'),
            'start': int(ch.get_boundary_info(info_list, 'startFace')),
            'n_faces': int(ch.get_boundary_info(info_list, 'nFaces'))
        }

        trimmed_file = trimmed_file[end + 1:]
        if boundary_data['type'] != 'empty':
            boundary_info.append(boundary_data)

    print("Boundary Information:")
    for i in boundary_info:
        print(i)

    boundary_df = []

    # Using the Boundary Information, Boundary Data is obtained
    for n, i in enumerate(boundary_info):
        end = i['start'] + i['n_faces']
        boundary_data = all_faces_df[i['start']:end]
        boundary_data.columns = ["D", "C", "B", "A", "N"]
        boundary_data["O"] = np.zeros_like(boundary_data["A"].values)
        boundary_data = boundary_data[['A', 'B', 'C', 'D', 'N', 'O']]
        boundary_data = boundary_data.reset_index(drop=True)
        boundary_data[['A', 'B', 'C', 'D', 'N']] = boundary_data[['A', 'B', 'C', 'D', 'N']].astype(int) +1

        # Converting into 2D
        boundary_data = cc.convert_face_data(boundary_data, points_df)
        boundary_df.append(boundary_data)

    return boundary_info, boundary_df

def get_n_nodes():
    neighbour = ch.read_file("../mesh_ground/constant/polyMesh/neighbour")
    return int(neighbour[11].split()[4])



