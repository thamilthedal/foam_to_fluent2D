import datetime
import CLI.lib.helper as ch
import pandas as pd
import CLI.lib.converter as cc
import CLI.lib.writer as cw
import CLI.lib.reader as cr

def obtain_data(CWD: str):
    # print("\nENTERING DATA GATHERING PHASE!\n")
    [header, points_data] = cr.get_points(CWD)
    face_header, footer, all_faces_data, owner_data, face_data = cr.get_faces(CWD)
    boundary_info = cr.get_boundary_info(CWD)
    n_nodes = cr.get_n_nodes(CWD)
    # print(f"Number of nodes: {n_nodes}")

    [boundary_header, footer, boundary_data] = cr.get_boundary_data(all_faces_data, owner_data, boundary_info, footer)

    header.append(f"(12 (0 1 {hex(n_nodes).split('x')[-1]} 0 0))\n")
    header.append(f"(13 (0 1 {hex(len(all_faces_data)).split('x')[-1]} 0 0))\n\n")
    header.append(f"(10 (1 1 {hex(len(points_data)).split('x')[-1]} 1 3)\n(\n")
    node_header = [f"(12 (1 1 {hex(n_nodes).split('x')[-1]} 1 0)(\n"]

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

def convert_data(points_data, face_data, boundary_data, n_boundaries, header_info):
    points_df = cc.point_convert(points_data)
    face_df = cc.face_convert(face_data, points_df)
    boundary_df = cc.boundary_convert(boundary_data, n_boundaries, points_df)
    header_info = cc.header_edits(points_df, n_boundaries, header_info)
    return [points_df, face_data, boundary_data, header_info]

def write_data(points_df, face_df, boundary_df, header_info, output_file, n_boundaries):
    cw.write_points(points_df, output_file, header_info)
    cw.write_faces(face_df, boundary_df, output_file, n_boundaries, header_info)
    cw.write_others(output_file, header_info)

