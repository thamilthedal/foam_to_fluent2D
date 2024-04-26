import modules.helper as ch
import pandas as pd
import numpy as np
import modules.converter as cc
import modules.writer as cw


def obtain_data(file_name, n_boundaries):
    ch.log_data("ENTERING DATA GATHERING PHASE!\n")

    header = ch.read_data(file_name, 0, 12)
    ch.save_header(header, "header")
    ch.log_data(header)

    # Reading Points Data
    point_skip = 12
    n_points = int(header[-2].split()[3], 16)
    ch.log_data(n_points)
    points_data = pd.DataFrame(np.genfromtxt(
        file_name,
        skip_header=point_skip,
        max_rows=n_points,
    ))
    points_data.to_csv('./data/points_data.csv', sep='\t')
    ch.log_data(points_data.head)

    # Reading Face Data
    face_header = ch.read_data(file_name,
                               point_skip + n_points + 2,
                               point_skip + n_points + 3)[0]
    ch.save_header(face_header, "face_header")
    ch.log_data(face_header)
    face_skip = point_skip + n_points + 4
    n_faces = int(face_header.split()[3], 16)
    ch.log_data(n_faces)
    n_all_faces = n_faces
    face_data = ch.get_face_data(file_name, face_skip, n_faces)
    face_data.to_csv('./data/face_data.csv', sep='\t')
    ch.log_data(face_data.head)

    # Reading Boundary Data
    boundary_skip = face_skip + n_faces + 3
    header_skip = face_skip + n_faces + 1
    boundary_data = []
    boundary_header = [0] * n_boundaries
    for n in range(n_boundaries):
        boundary_header[n] = ch.read_data(file_name,
                                          header_skip,
                                          header_skip + 1)[0]
        ch.save_header(boundary_header[n], f"boundary_header_{n + 1}")
        n_boundary_faces = (
                                   int(boundary_header[n].split()[3], 16) -
                                   int(boundary_header[n].split()[2], 16)) + 1
        header_skip += n_boundary_faces + 3
        boundary_data.append(ch.get_face_data(file_name,
                                              boundary_skip,
                                              n_boundary_faces))
        boundary_data[n].to_csv(f'./data/boundary_data_{n + 1}.csv', sep='\t')
        boundary_skip += n_boundary_faces + 3
        n_all_faces += n_boundary_faces
        ch.log_data(boundary_header[n])
        ch.log_data(boundary_data[n].head)

    # Reading Node Header
    node_skip = boundary_skip + 1 + (int(header[-4].split()[3], 16) - n_all_faces)
    ch.log_data(node_skip)
    node_header = ch.read_data(file_name,
                               node_skip,
                               node_skip + 1)[0]
    ch.save_header(node_header, "node_header")
    ch.log_data(node_header)

    # Reading Footer
    footer_skip = node_skip + 2
    footer = ch.read_data(file_name, footer_skip, -1)
    ch.log_data(footer)
    ch.save_header(footer, "footer")
    ch.log_data("I am done Data retrieval!\n\n")


def convert_data(n_boundaries):
    cc.point_convert()
    cc.face_convert()
    cc.boundary_convert(n_boundaries)
    cc.header_edits(n_boundaries)


def write_data(output_file, n_boundaries):
    cw.write_points(output_file)
    cw.write_faces(output_file, n_boundaries)
    cw.write_others(output_file)
