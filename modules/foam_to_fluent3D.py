import datetime
import modules.helper as ch
import pandas as pd
import modules.writer as cw
import modules.reader as cr

def obtain_data():
    print("\nENTERING DATA GATHERING PHASE!\n")
    [header, points_data] = cr.get_points()
    face_header, footer, all_faces_data, owner_data, face_data = cr.get_faces()
    boundary_info = cr.get_boundary_info()
    n_nodes = cr.get_n_nodes()
    print(f"Number of nodes: {n_nodes}")

    [boundary_header, footer, boundary_data] = cr.get_boundary_data(all_faces_data, owner_data, boundary_info, footer)

    header.append(f"(12 (0 1 {hex(n_nodes).split('x')[-1]} 0 0))\n")
    header.append(f"(13 (0 1 {hex(len(all_faces_data)).split('x')[-1]} 0 0))\n\n")
    header.append(f"(10 (1 1 {hex(len(points_data)).split('x')[-1]} 1 3)\n(\n")

    node_header = [f"(12 (1 1 {hex(n_nodes).split('x')[-1]} 1 0)(\n"]

    print("\nI am done Data retrieval!\n\n")

    header_info = {
            'header':header,
            'face_header':face_header,
            'boundary_header':boundary_header,
            'node_header':node_header,
            'footer':footer
            }


    return [header_info,
            points_data,
            face_data,
            boundary_data, 
            boundary_info]

def write_3D_data(points_df, face_df, boundary_df, header_info, output_file, n_boundaries):
    cw.write_3D_points(points_df, output_file, header_info)
    cw.write_3D_faces(face_df, boundary_df, output_file, n_boundaries, header_info)
    cw.write_3D_others(output_file, header_info)


def main():
    ch.log_start()
    start = datetime.datetime.now()
    print(start)
    [header_info, points_data, face_data, boundary_data, boundary_info] = obtain_data()
    print("\nData Gathered\n")
    print(datetime.datetime.now()-start)
    n_boundaries = len(boundary_info)-1
    write_3D_data(points_data,
               face_data,
               boundary_data,
               header_info,
               "./mesh_ground/fluentInterface/mesh_ground_3D.msh",
               n_boundaries)
    print("\nDONE\n")
    print(datetime.datetime.now()-start)

if __name__ == "__main__":
    main()
