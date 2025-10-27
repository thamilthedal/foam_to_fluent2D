import datetime
from CLI.lib.run import obtain_data, convert_data, write_data
import os
import errno


def file_check(cwd: str = "."):
    file_paths = [
                f"{cwd}/constant/polyMesh/points",
                f"{cwd}/constant/polyMesh/boundary",
                f"{cwd}/constant/polyMesh/faces",
                f"{cwd}/constant/polyMesh/neighbour",
                f"{cwd}/constant/polyMesh/owner"
            ]
    for file_path in file_paths:
        if os.path.isfile(file_path):
            continue
        else:
            print(file_path)
            return 1
    return 0

def foam_to_fluent_2D(current_working_directory: str = "."):
    if file_check(current_working_directory):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), " ")
        return None

    start = datetime.datetime.now()
    # print(start)
    [header_info, points_data, face_data, boundary_data, boundary_info] = obtain_data(current_working_directory)
    # print_header("Polymesh Data Gathered")
    # print(datetime.datetime.now()-start)
    n_boundaries = len(boundary_info)-1
    [points_df, face_df, boundary_df, header_info] = convert_data(points_data,
                                                                  face_data,
                                                                  boundary_data, 
                                                                  n_boundaries,
                                                                  header_info)
    # print("\nData Converted to 2D\n")
    # print(datetime.datetime.now()-start)
    if not os.path.exists(f"{current_working_directory}/fluentInterface"):
        os.mkdir(f"{current_working_directory}/fluentInterface")
    write_data(points_df,
               face_df,
               boundary_df,
               header_info,
               f"{current_working_directory}/fluentInterface/fluent_converted.msh",
               n_boundaries)
    minutes, seconds = divmod((datetime.datetime.now() - start).total_seconds(), 60)
    print(f"Mesh created and converted to 2D in (MM:SS): {int(minutes):02}:{seconds:04.1f}")
