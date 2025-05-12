import datetime
from CLI.lib.run import obtain_data, convert_data, write_data
from CLI.helper import print_header
import os
import errno


def file_check():
    file_paths = [
                "./constant/polyMesh/points",
                "./constant/polyMesh/boundary",
                "./constant/polyMesh/faces",
                "./constant/polyMesh/neighbour",
                "./constant/polyMesh/owner"
            ]
    for file_path in file_paths:
        if os.path.isfile(file_path):
            continue
        else:
            print(file_path)
            return 1
    return 0

def foam_to_fluent_2D(current_working_directory: str):
    if file_check():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), " ")
        return None

    start = datetime.datetime.now()
    print(start)
    [header_info, points_data, face_data, boundary_data, boundary_info] = obtain_data(current_working_directory)
    print_header("Polymesh Data Gathered")
    print(datetime.datetime.now()-start)
    n_boundaries = len(boundary_info)-1
    [points_df, face_df, boundary_df, header_info] = convert_data(points_data,
                                                                  face_data,
                                                                  boundary_data, 
                                                                  n_boundaries,
                                                                  header_info)
    print("\nData Converted to 2D\n")
    # print(datetime.datetime.now()-start)
    if not os.path.exists(f"./{current_working_directory}/mesh"):
        os.mkdir(f"./{current_working_directory}/mesh")
    write_data(points_df,
               face_df,
               boundary_df,
               header_info,
               f"./{current_working_directory}/mesh/fluent_converted.msh",
               n_boundaries)
    print_header("Mesh Converted to 2D")
    print_header(datetime.datetime.now()-start)
