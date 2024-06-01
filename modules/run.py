import modules.helper as ch
import pandas as pd
import numpy as np
import modules.converter as cc
import modules.writer as cw
import modules.reader as cr

def obtain_data():
    ch.log_data("ENTERING DATA GATHERING PHASE!\n")
    points_data = cr.get_points()
    all_faces_data, owner_data, face_data = cr.get_faces()
    boundary_info = cr.get_boundary_info()
    n_nodes = cr.get_n_nodes()
    cr.get_boundary_data(all_faces_data, owner_data, boundary_info)

    with open("./data/header.txt", "a") as f:
        f.write(f"(12 (0 1 {hex(n_nodes).split('x')[-1]} 0 0))\n")
        f.write(f"(13 (0 1 {hex(len(all_faces_data)).split('x')[-1]} 0 0))\n\n")
        f.write(f"(10 (1 1 {hex(len(points_data)).split('x')[-1]} 1 3)\n(\n")

    with open("./data/node_header.txt", "w") as f:
        f.write(f"(12 (1 1 {hex(n_nodes).split('x')[-1]} 1 0)(\n")

    ch.log_data("I am done Data retrieval!\n\n")

    return len(boundary_info)-1

def convert_data(n_boundaries):
    cc.point_convert()
    point_df = pd.read_csv('./data/points_data.csv', sep='\t')
    point_df = point_df.astype({"ID": 'int', "new_ID": 'int'})
    cc.face_convert(point_df)
    cc.boundary_convert(n_boundaries, point_df)
    cc.header_edits(n_boundaries)


def write_data(output_file, n_boundaries):
    cw.write_points(output_file)
    cw.write_faces(output_file, n_boundaries)
    cw.write_others(output_file)
